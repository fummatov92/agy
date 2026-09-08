import json
import glob

files = [
    "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_05.jsonl",
    "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_23.jsonl",
    "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_04.jsonl",
]

total_lines = 0
for fpath in files:
    print(f"Checking {fpath}...")
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    assert len(lines) > 0, "Empty file!"
    for i, line in enumerate(lines):
        line = line.strip()
        assert line, f"Line {i} is empty"
        obj = json.loads(line)
        keys = list(obj.keys())
        assert keys == ["id", "source", "topic", "text"], f"Invalid keys: {keys}"
        assert len(obj["text"]) <= 1000, f"Text length > 1000: {len(obj['text'])}"
        assert obj["id"].endswith(f"__{i}"), f"Index mismatch: {obj['id']} vs {i}"
        total_lines += 1
    print(f"  OK: {len(lines)} valid chunks.")

print(f"ALL CHUNKS VALID! Total chunks across 3 files: {total_lines}")
