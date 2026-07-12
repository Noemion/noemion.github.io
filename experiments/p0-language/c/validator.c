#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HEADER_SIZE ((size_t)64)
#define ENTRY_SIZE ((size_t)48)
#define MAX_ARTIFACT_BYTES ((size_t)(16U * 1024U * 1024U))
#define MAX_RECORD_COUNT ((size_t)64)

typedef struct {
    uint16_t kind;
    uint32_t id;
    size_t start;
    size_t end;
} Entry;

static uint16_t read_u16le(const uint8_t *data, size_t offset) {
    return (uint16_t)((uint16_t)data[offset] | ((uint16_t)data[offset + 1U] << 8U));
}

static uint32_t read_u32le(const uint8_t *data, size_t offset) {
    return (uint32_t)data[offset]
        | ((uint32_t)data[offset + 1U] << 8U)
        | ((uint32_t)data[offset + 2U] << 16U)
        | ((uint32_t)data[offset + 3U] << 24U);
}

static uint64_t read_u64le(const uint8_t *data, size_t offset) {
    uint64_t value = 0U;
    unsigned shift;
    for (shift = 0U; shift < 64U; shift += 8U) {
        value |= (uint64_t)data[offset + (size_t)(shift / 8U)] << shift;
    }
    return value;
}

static int checked_add_size(size_t left, size_t right, size_t *result) {
    if (right > SIZE_MAX - left) {
        return 0;
    }
    *result = left + right;
    return 1;
}

static int checked_mul_size(size_t left, size_t right, size_t *result) {
    if (left != 0U && right > SIZE_MAX / left) {
        return 0;
    }
    *result = left * right;
    return 1;
}

static const char *validate_bytes(const uint8_t *data, size_t size) {
    static const uint8_t magic[8] = {'E', 'N', 'D', 'E', 'M', 0U, '\r', '\n'};
    Entry entries[MAX_RECORD_COUNT];
    Entry ranges[MAX_RECORD_COUNT];
    uint32_t ids[MAX_RECORD_COUNT];
    size_t record_count;
    size_t directory_offset;
    size_t directory_bytes;
    size_t directory_end;
    size_t index;
    size_t previous_end;
    uint16_t prior_kind = 0U;
    uint32_t prior_id = 0U;
    int has_prior = 0;

    if (size < HEADER_SIZE) {
        return "endem.wire.header.truncated";
    }
    if (memcmp(data, magic, sizeof(magic)) != 0) {
        return "endem.wire.header.magic";
    }
    if (read_u16le(data, 8U) != 0U || read_u16le(data, 10U) != 1U) {
        return "endem.wire.header.version";
    }
    if (read_u16le(data, 12U) != 64U || read_u16le(data, 14U) != 48U || data[16] != 1U) {
        return "endem.wire.header.layout";
    }
    if (read_u64le(data, 32U) != (uint64_t)size) {
        return "endem.wire.header.size";
    }
    if (data[19] != 0U) {
        return "endem.wire.header.reserved";
    }
    for (index = 40U; index < 64U; ++index) {
        if (data[index] != 0U) {
            return "endem.wire.header.reserved";
        }
    }

    record_count = (size_t)read_u32le(data, 20U);
    if (read_u64le(data, 24U) > (uint64_t)SIZE_MAX) {
        return "endem.wire.directory.out_of_bounds";
    }
    directory_offset = (size_t)read_u64le(data, 24U);
    if (!checked_mul_size(record_count, ENTRY_SIZE, &directory_bytes)
        || !checked_add_size(directory_offset, directory_bytes, &directory_end)
        || directory_offset != HEADER_SIZE
        || directory_end > size) {
        return "endem.wire.directory.out_of_bounds";
    }
    if (data[17] != 1U) {
        return "endem.wire.profile.unknown";
    }
    if (size > MAX_ARTIFACT_BYTES || record_count > MAX_RECORD_COUNT) {
        return "endem.wire.profile.limit";
    }
    if (data[18] != 0U) {
        return "endem.wire.profile.feature";
    }

    for (index = 0U; index < record_count; ++index) {
        const size_t offset = directory_offset + index * ENTRY_SIZE;
        const uint16_t kind = read_u16le(data, offset);
        const uint16_t flags = read_u16le(data, offset + 2U);
        const uint32_t id = read_u32le(data, offset + 4U);
        const uint64_t start_u64 = read_u64le(data, offset + 8U);
        const uint64_t stored_u64 = read_u64le(data, offset + 16U);
        const uint64_t logical_u64 = read_u64le(data, offset + 24U);
        const uint32_t alignment = read_u32le(data, offset + 32U);
        size_t prior_index;
        size_t end;

        if (has_prior != 0 && (kind < prior_kind || (kind == prior_kind && id <= prior_id))) {
            return "endem.wire.directory.order";
        }
        prior_kind = kind;
        prior_id = id;
        has_prior = 1;
        if (id == 0U) {
            return "endem.wire.record.id";
        }
        for (prior_index = 0U; prior_index < index; ++prior_index) {
            if (ids[prior_index] == id) {
                return "endem.wire.record.id";
            }
        }
        ids[index] = id;
        if (flags != 1U) {
            return "endem.wire.record.flags";
        }
        if (kind < 1U || kind > 6U) {
            return "endem.wire.record.unknown_kind";
        }
        if (start_u64 > (uint64_t)SIZE_MAX || stored_u64 > (uint64_t)SIZE_MAX) {
            return "endem.wire.record.range";
        }
        if (alignment != 8U || ((size_t)start_u64 % 8U) != 0U) {
            return "endem.wire.record.alignment";
        }
        if (!checked_add_size((size_t)start_u64, (size_t)stored_u64, &end)
            || (size_t)start_u64 < directory_end
            || end > size) {
            return "endem.wire.record.range";
        }
        if (stored_u64 != logical_u64
            || read_u32le(data, offset + 36U) != 0U
            || read_u32le(data, offset + 40U) != 0U
            || read_u32le(data, offset + 44U) != 0U) {
            return "endem.wire.profile.feature";
        }
        entries[index].kind = kind;
        entries[index].id = id;
        entries[index].start = (size_t)start_u64;
        entries[index].end = end;
        ranges[index] = entries[index];
    }
    if (record_count != 6U) {
        return "endem.wire.facet.cardinality";
    }
    for (index = 0U; index < 6U; ++index) {
        if (entries[index].kind != (uint16_t)(index + 1U)) {
            return "endem.wire.facet.cardinality";
        }
    }

    for (index = 1U; index < record_count; ++index) {
        Entry current = ranges[index];
        size_t cursor = index;
        while (cursor > 0U && (current.start < ranges[cursor - 1U].start
            || (current.start == ranges[cursor - 1U].start && current.end < ranges[cursor - 1U].end))) {
            ranges[cursor] = ranges[cursor - 1U];
            --cursor;
        }
        ranges[cursor] = current;
    }
    previous_end = directory_end;
    for (index = 0U; index < record_count; ++index) {
        size_t padding;
        if (ranges[index].start < previous_end) {
            return "endem.wire.record.overlap";
        }
        for (padding = previous_end; padding < ranges[index].start; ++padding) {
            if (data[padding] != 0U) {
                return "endem.wire.record.padding";
            }
        }
        previous_end = ranges[index].end;
    }
    if (previous_end != size) {
        return "endem.wire.record.padding";
    }
    for (index = 0U; index < record_count; ++index) {
        const size_t length = entries[index].end - entries[index].start;
        const uint8_t initial = length == 0U ? 0U : data[entries[index].start];
        if (length == 0U) {
            return "endem.wire.payload.cbor";
        }
        if ((initial >> 5U) != 5U) {
            return "endem.wire.payload.not_map";
        }
        if (length != 1U || initial != 0xa0U) {
            return "endem.wire.payload.cbor";
        }
    }
    return "accept";
}

#if defined(ENDEM_FUZZING)
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    (void)validate_bytes(data, size);
    return 0;
}
#else
static uint8_t *read_file(const char *path, size_t *size_out) {
    FILE *stream = fopen(path, "rb");
    long length;
    uint8_t *data;
    if (stream == NULL) {
        return NULL;
    }
    if (fseek(stream, 0L, SEEK_END) != 0 || (length = ftell(stream)) < 0L
        || fseek(stream, 0L, SEEK_SET) != 0) {
        (void)fclose(stream);
        return NULL;
    }
    if ((uint64_t)length > (uint64_t)SIZE_MAX) {
        (void)fclose(stream);
        errno = EFBIG;
        return NULL;
    }
    *size_out = (size_t)length;
    data = malloc(*size_out == 0U ? 1U : *size_out);
    if (data == NULL) {
        (void)fclose(stream);
        return NULL;
    }
    if (*size_out != 0U && fread(data, 1U, *size_out, stream) != *size_out) {
        free(data);
        (void)fclose(stream);
        return NULL;
    }
    if (fclose(stream) != 0) {
        free(data);
        return NULL;
    }
    return data;
}

int main(int argc, char **argv) {
    uint8_t *data;
    size_t size = 0U;
    const char *result;
    if (argc != 2) {
        (void)fprintf(stderr, "usage: c-reader FILE\n");
        return 64;
    }
    data = read_file(argv[1], &size);
    if (data == NULL) {
        (void)fprintf(stderr, "read failed\n");
        return 66;
    }
    result = validate_bytes(data, size);
    (void)puts(result);
    free(data);
    return strcmp(result, "accept") == 0 ? 0 : 2;
}
#endif
