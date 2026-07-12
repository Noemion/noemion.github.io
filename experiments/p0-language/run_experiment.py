from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = Path(__file__).resolve().parent
MANIFEST = ROOT / "vectors" / "wire" / "manifest.json"


def run(command, **kwargs):
    return subprocess.run(command, check=True, text=True, capture_output=True, **kwargs)


def version(command):
    completed = run(command)
    return (completed.stdout or completed.stderr).splitlines()[0]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compile_readers(output_dir, clang, rustc):
    c_binary = output_dir / "c-reader"
    rust_binary = output_dir / "rust-reader"
    run([
        clang, "-std=c17", "-O2", "-Wall", "-Wextra", "-Werror",
        "-Wconversion", "-Wshadow", "-pedantic",
        str(EXPERIMENT / "c" / "validator.c"), "-o", str(c_binary),
    ])
    run([
        rustc, "--edition=2024", "-C", "opt-level=2", "-C", "overflow-checks=yes",
        "-D", "warnings", str(EXPERIMENT / "rust" / "main.rs"), "-o", str(rust_binary),
    ])
    return {"c": c_binary, "rust": rust_binary}


def reader_result(binary, path):
    completed = subprocess.run([str(binary), str(path)], text=True, capture_output=True)
    if completed.returncode not in (0, 2):
        raise RuntimeError(
            f"{binary.name} crashed for {path.name}: rc={completed.returncode} "
            f"stderr={completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def expected_result(vector):
    expected = vector["expect"]
    return "accept" if expected["result"] == "structural-accept" else expected["code"]


def deterministic_mutations(data):
    samples = []
    for length in (0, 1, 7, 8, 16, 32, 63, 64, 80, 160, 288, 351, 352, len(data) - 1):
        if 0 <= length < len(data):
            samples.append((f"truncate-{length}", data[:length]))
    offsets = sorted({(index * (len(data) - 1)) // 127 for index in range(128)})
    for offset in offsets:
        mutated = bytearray(data)
        mutated[offset] ^= 0x01
        samples.append((f"flip-{offset}", bytes(mutated)))
    samples.append(("append-zero", data + b"\x00"))
    samples.append(("append-nonzero", data + b"\xff"))
    return samples


def dynamic_dependencies(binary):
    if platform.system() == "Darwin" and shutil.which("otool"):
        lines = run(["otool", "-L", str(binary)]).stdout.splitlines()[1:]
        return [line.strip().split(" (", 1)[0] for line in lines if line.strip()]
    if shutil.which("ldd"):
        return [line.strip() for line in run(["ldd", str(binary)]).stdout.splitlines()]
    return []


def main():
    require_libfuzzer = "--require-libfuzzer" in sys.argv[1:]
    clang = os.environ.get("CLANG") or shutil.which("clang")
    rustc = os.environ.get("RUSTC") or shutil.which("rustc")
    if not clang or not rustc:
        print("P0-LANG-001 requires both clang and rustc", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST.read_text())
    vectors = manifest["vectors"]
    with TemporaryDirectory(prefix="noemion-language-") as temporary:
        temp = Path(temporary)
        inputs = temp / "inputs"
        inputs.mkdir()
        input_paths = {}
        for vector in vectors:
            raw = bytes.fromhex((ROOT / vector["hex"]).read_text())
            path = inputs / f'{vector["id"]}.endem'
            path.write_bytes(raw)
            input_paths[vector["id"]] = path

        builds = []
        for build_index in (1, 2):
            output_dir = temp / f"build-{build_index}"
            output_dir.mkdir()
            builds.append(compile_readers(output_dir, clang, rustc))

        vector_results = {}
        for vector in vectors:
            path = input_paths[vector["id"]]
            expected = expected_result(vector)
            actual = {language: reader_result(binary, path) for language, binary in builds[0].items()}
            vector_results[vector["id"]] = {"expected": expected, "actual": actual}
            if any(result != expected for result in actual.values()):
                raise RuntimeError(f"vector disagreement: {vector['id']}: {actual} != {expected}")

        valid = bytes.fromhex((ROOT / "vectors" / "wire" / "minimal-structural.hex").read_text())
        mutation_dir = temp / "mutations"
        mutation_dir.mkdir()
        mutation_count = 0
        for name, mutation in deterministic_mutations(valid):
            path = mutation_dir / f"{name}.endem"
            path.write_bytes(mutation)
            actual = {language: reader_result(binary, path) for language, binary in builds[0].items()}
            if len(set(actual.values())) != 1:
                raise RuntimeError(f"differential disagreement for {name}: {actual}")
            mutation_count += 1

        sanitizer_binary = temp / "c-reader-sanitized"
        run([
            clang, "-std=c17", "-O1", "-g", "-fno-omit-frame-pointer",
            "-fsanitize=address,undefined", str(EXPERIMENT / "c" / "validator.c"),
            "-o", str(sanitizer_binary),
        ])
        for path in [*input_paths.values(), *mutation_dir.glob("*.endem")]:
            reader_result(sanitizer_binary, path)

        corpus = temp / "corpus"
        corpus.mkdir()
        for vector_id, path in input_paths.items():
            shutil.copy2(path, corpus / vector_id)
        fuzzer_binary = temp / "c-reader-fuzzer"
        libfuzzer_available = True
        libfuzzer_pass = False
        libfuzzer_note = ""
        try:
            run([
                clang, "-std=c17", "-O1", "-g", "-DENDEM_FUZZING",
                "-fsanitize=fuzzer,address,undefined", str(EXPERIMENT / "c" / "validator.c"),
                "-o", str(fuzzer_binary),
            ])
            fuzz = run([
                str(fuzzer_binary), str(corpus), "-runs=10000", "-max_len=512",
                "-seed=213", "-timeout=2", "-rss_limit_mb=256",
            ])
            libfuzzer_pass = "DONE" in fuzz.stderr or "DONE" in fuzz.stdout
        except subprocess.CalledProcessError as error:
            libfuzzer_available = False
            error_lines = (error.stderr or error.stdout or str(error)).strip().splitlines()
            libfuzzer_note = " | ".join(error_lines[-2:])
            if require_libfuzzer:
                raise RuntimeError(f"required libFuzzer run unavailable: {libfuzzer_note}") from error

        artifacts = {}
        for language in ("c", "rust"):
            first = builds[0][language]
            second = builds[1][language]
            first_hash = sha256(first)
            second_hash = sha256(second)
            artifacts[language] = {
                "source_nonblank_lines": sum(
                    1 for line in (EXPERIMENT / language / ("validator.c" if language == "c" else "main.rs")).read_text().splitlines()
                    if line.strip()
                ),
                "binary_bytes": first.stat().st_size,
                "binary_sha256": first_hash,
                "repeated_binary_sha256_match": first_hash == second_hash,
                "dynamic_dependencies": dynamic_dependencies(first),
            }

        report = {
            "experiment": "P0-LANG-001",
            "format": "END-FMT 0.1.0-draft",
            "profile": "END-P0 0.1.0-draft",
            "environment": {
                "platform": platform.platform(),
                "clang": version([clang, "--version"]),
                "rustc": version([rustc, "--version"]),
            },
            "all_vectors_match": True,
            "vector_count": len(vectors),
            "vector_results": vector_results,
            "differential_mutations_match": True,
            "differential_mutation_count": mutation_count,
            "c_sanitizers_pass": True,
            "c_libfuzzer_available": libfuzzer_available,
            "c_libfuzzer_runs": 10000 if libfuzzer_available else 0,
            "c_libfuzzer_pass": libfuzzer_pass,
            "c_libfuzzer_note": libfuzzer_note,
            "artifacts": artifacts,
            "limits": [
                "Structural END-P0 slice only; full deterministic CBOR and END-CORE semantics are not implemented.",
                "Repeated binary equality is same-host evidence, not cross-platform reproducibility.",
                "Fuzzing and sanitizers reduce evidence gaps but do not prove absence of defects.",
            ],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
