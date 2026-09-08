import json
import os
import re

def test_jsonl_files():
    targets = [
        {
            "path": "/home/fayzillo/Downloads/brains/rag-ready/05-id-string-db-majburiy/chunks.jsonl",
            "expected_total_lines": 501,
            "new_source": "bot_post_using/docs/telegram-id-string-db-architecture.md",
            "new_count": 17,
            "topic": "id-string-db-majburiy"
        },
        {
            "path": "/home/fayzillo/Downloads/brains/rag-ready/23-prisma-id-string-va/chunks.jsonl",
            "expected_total_lines": 998,
            "new_source": "bot_post_using/docs/prisma-telegram-bot-schema-and-id-types.md",
            "new_count": 17,
            "topic": "prisma-id-string-va"
        },
        {
            "path": "/home/fayzillo/Downloads/brains/rag-ready/04-md-va-bo-bu/chunks.jsonl",
            "expected_total_lines": 163,
            "new_source": "bot_post_using/docs/telegraf-bot-architecture-and-ux-rules.md",
            "new_count": 19,
            "topic": "md-va-bo-bu"
        },
    ]

    for t in targets:
        fpath = t["path"]
        print(f"Testing {fpath}...")
        assert os.path.exists(fpath), f"File missing: {fpath}"
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == t["expected_total_lines"], f"Line count mismatch in {fpath}: {len(lines)} vs {t['expected_total_lines']}"

        new_chunks = []
        for line_num, line in enumerate(lines):
            line_str = line.strip()
            assert line_str, f"Empty line at {line_num} in {fpath}"
            data = json.loads(line_str)
            assert set(data.keys()) == {"id", "source", "topic", "text"}, f"Bad keys at line {line_num}: {data.keys()}"
            assert len(data["text"]) <= 1000, f"Chunk text > 1000 chars at line {line_num}: {len(data['text'])}"
            if data["source"] == t["new_source"]:
                new_chunks.append(data)

        assert len(new_chunks) == t["new_count"], f"Expected {t['new_count']} new chunks for {t['new_source']}, got {len(new_chunks)}"
        print(f"  -> {len(lines)} lines parsed perfectly. {len(new_chunks)} new chunks verified.")

def test_markdown_files():
    md_files = [
        "/home/fayzillo/Downloads/brains/grouped-md/05-id-string-db-majburiy/telegram-id-string-db-architecture.md",
        "/home/fayzillo/Downloads/brains/grouped-md/23-prisma-id-string-va/prisma-telegram-bot-schema-and-id-types.md",
        "/home/fayzillo/Downloads/brains/grouped-md/04-md-va-bo-bu/telegraf-bot-architecture-and-ux-rules.md",
    ]
    for md in md_files:
        assert os.path.exists(md), f"File missing: {md}"
        size = os.path.getsize(md)
        assert size > 5000, f"File too small ({size} bytes): {md}"
        print(f"Verified {md} (size: {size} bytes)")

def test_consolidated():
    checks = [
        ("/home/fayzillo/Downloads/brains/grouped-md/05-id-string-db-majburiy/consolidated.md", "## Manba: bot_post_using/docs/telegram-id-string-db-architecture.md"),
        ("/home/fayzillo/Downloads/brains/grouped-md/23-prisma-id-string-va/consolidated.md", "## Manba: bot_post_using/docs/prisma-telegram-bot-schema-and-id-types.md"),
        ("/home/fayzillo/Downloads/brains/grouped-md/04-md-va-bo-bu/consolidated.md", "## Manba: bot_post_using/docs/telegraf-bot-architecture-and-ux-rules.md"),
    ]
    for fpath, header in checks:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        assert header in content, f"Header '{header}' not found in {fpath}"
        print(f"Verified header in {fpath}")

def test_index():
    index_path = "/home/fayzillo/Downloads/brains/00-INDEX.md"
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "(`04-md-va-bo-bu`) — 38 ta hujjat" in content, "04 count mismatch in 00-INDEX.md"
    assert "(`05-id-string-db-majburiy`) — 38 ta hujjat" in content, "05 count mismatch in 00-INDEX.md"
    assert "(`23-prisma-id-string-va`) — 17 ta hujjat" in content, "23 count mismatch in 00-INDEX.md"
    print("Verified 00-INDEX.md counts: 04 -> 38, 05 -> 38, 23 -> 17")

if __name__ == "__main__":
    test_jsonl_files()
    test_markdown_files()
    test_consolidated()
    test_index()
    print("\n✅ ALL VERIFICATIONS PASSED SUCCESSFULLY!")
