#![forbid(unsafe_code)]

use std::env;
use std::fs;

const MAGIC: &[u8; 8] = b"ENDEM\0\r\n";
const HEADER_SIZE: usize = 64;
const ENTRY_SIZE: usize = 48;
const MAX_ARTIFACT_BYTES: usize = 16 * 1024 * 1024;
const MAX_RECORD_COUNT: usize = 64;

#[derive(Clone, Copy)]
struct Entry {
    kind: u16,
    id: u32,
    start: usize,
    end: usize,
}

fn u16le(data: &[u8], offset: usize) -> Option<u16> {
    let bytes: [u8; 2] = data.get(offset..offset.checked_add(2)?)?.try_into().ok()?;
    Some(u16::from_le_bytes(bytes))
}

fn u32le(data: &[u8], offset: usize) -> Option<u32> {
    let bytes: [u8; 4] = data.get(offset..offset.checked_add(4)?)?.try_into().ok()?;
    Some(u32::from_le_bytes(bytes))
}

fn u64le(data: &[u8], offset: usize) -> Option<u64> {
    let bytes: [u8; 8] = data.get(offset..offset.checked_add(8)?)?.try_into().ok()?;
    Some(u64::from_le_bytes(bytes))
}

fn validate(data: &[u8]) -> &'static str {
    if data.len() < HEADER_SIZE {
        return "endem.wire.header.truncated";
    }
    if data.get(..8) != Some(MAGIC.as_slice()) {
        return "endem.wire.header.magic";
    }

    let Some(major) = u16le(data, 8) else { return "endem.wire.header.truncated" };
    let Some(minor) = u16le(data, 10) else { return "endem.wire.header.truncated" };
    if (major, minor) != (0, 1) {
        return "endem.wire.header.version";
    }
    let Some(header_size) = u16le(data, 12) else { return "endem.wire.header.truncated" };
    let Some(entry_size) = u16le(data, 14) else { return "endem.wire.header.truncated" };
    if header_size != 64 || entry_size != 48 || data[16] != 1 {
        return "endem.wire.header.layout";
    }
    let Some(file_size) = u64le(data, 32) else { return "endem.wire.header.truncated" };
    if usize::try_from(file_size).ok() != Some(data.len()) {
        return "endem.wire.header.size";
    }
    if data[19] != 0 || data[40..64].iter().any(|byte| *byte != 0) {
        return "endem.wire.header.reserved";
    }

    let Some(record_count_u32) = u32le(data, 20) else { return "endem.wire.header.truncated" };
    let record_count = record_count_u32 as usize;
    let Some(directory_offset_u64) = u64le(data, 24) else { return "endem.wire.header.truncated" };
    let Ok(directory_offset) = usize::try_from(directory_offset_u64) else {
        return "endem.wire.directory.out_of_bounds";
    };
    let Some(directory_bytes) = record_count.checked_mul(ENTRY_SIZE) else {
        return "endem.wire.directory.out_of_bounds";
    };
    let Some(directory_end) = directory_offset.checked_add(directory_bytes) else {
        return "endem.wire.directory.out_of_bounds";
    };
    if directory_offset != HEADER_SIZE || directory_end > data.len() {
        return "endem.wire.directory.out_of_bounds";
    }
    if data[17] != 1 {
        return "endem.wire.profile.unknown";
    }
    if data.len() > MAX_ARTIFACT_BYTES || record_count > MAX_RECORD_COUNT {
        return "endem.wire.profile.limit";
    }
    if data[18] != 0 {
        return "endem.wire.profile.feature";
    }

    let mut entries = Vec::with_capacity(record_count);
    let mut prior_order: Option<(u16, u32)> = None;
    let mut ids = Vec::with_capacity(record_count);
    for index in 0..record_count {
        let offset = directory_offset + index * ENTRY_SIZE;
        let kind = u16le(data, offset).unwrap_or(0);
        let flags = u16le(data, offset + 2).unwrap_or(0);
        let id = u32le(data, offset + 4).unwrap_or(0);
        let order = (kind, id);
        if prior_order.is_some_and(|prior| order <= prior) {
            return "endem.wire.directory.order";
        }
        prior_order = Some(order);
        if id == 0 || ids.contains(&id) {
            return "endem.wire.record.id";
        }
        ids.push(id);
        if flags != 1 {
            return "endem.wire.record.flags";
        }
        if !(1..=6).contains(&kind) {
            return "endem.wire.record.unknown_kind";
        }
        let Some(start_u64) = u64le(data, offset + 8) else { return "endem.wire.record.range" };
        let Some(stored_u64) = u64le(data, offset + 16) else { return "endem.wire.record.range" };
        let Some(logical_u64) = u64le(data, offset + 24) else { return "endem.wire.record.range" };
        let Some(alignment) = u32le(data, offset + 32) else { return "endem.wire.record.alignment" };
        let Ok(start) = usize::try_from(start_u64) else { return "endem.wire.record.range" };
        let Ok(stored) = usize::try_from(stored_u64) else { return "endem.wire.record.range" };
        if alignment != 8 || start % 8 != 0 {
            return "endem.wire.record.alignment";
        }
        let Some(end) = start.checked_add(stored) else { return "endem.wire.record.range" };
        if start < directory_end || end > data.len() {
            return "endem.wire.record.range";
        }
        if stored_u64 != logical_u64
            || u32le(data, offset + 36) != Some(0)
            || u32le(data, offset + 40) != Some(0)
            || u32le(data, offset + 44) != Some(0)
        {
            return "endem.wire.profile.feature";
        }
        entries.push(Entry { kind, id, start, end });
    }
    if entries.iter().map(|entry| entry.kind).ne(1_u16..=6) {
        return "endem.wire.facet.cardinality";
    }

    let mut ranges = entries.clone();
    ranges.sort_by_key(|entry| (entry.start, entry.end, entry.id));
    let mut previous_end = directory_end;
    for entry in &ranges {
        if entry.start < previous_end {
            return "endem.wire.record.overlap";
        }
        if data[previous_end..entry.start].iter().any(|byte| *byte != 0) {
            return "endem.wire.record.padding";
        }
        previous_end = entry.end;
    }
    if previous_end != data.len() {
        return "endem.wire.record.padding";
    }
    for entry in &entries {
        let payload = &data[entry.start..entry.end];
        let Some(initial) = payload.first() else { return "endem.wire.payload.cbor" };
        if initial >> 5 != 5 {
            return "endem.wire.payload.not_map";
        }
        if payload != [0xa0] {
            return "endem.wire.payload.cbor";
        }
    }
    "accept"
}

fn main() {
    let Some(path) = env::args_os().nth(1) else {
        eprintln!("usage: rust-reader FILE");
        std::process::exit(64);
    };
    let data = match fs::read(path) {
        Ok(data) => data,
        Err(error) => {
            eprintln!("read failed: {error}");
            std::process::exit(66);
        }
    };
    let result = validate(&data);
    println!("{result}");
    if result != "accept" {
        std::process::exit(2);
    }
}
