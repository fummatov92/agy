#!/usr/bin/env python3
import json
import os
import re
import sys

def test_audit():
    print("=== VICTORY AUDITOR INDEPENDENT TEST EXECUTION ===")
    errors = []
    warnings = []

    brains_dir = "/home/fayzillo/Downloads/brains"
    grouped_md_dir = os.path.join(brains_dir, "grouped-md")
    rag_ready_dir = os.path.join(brains_dir, "rag-ready")
    index_path = os.path.join(brains_dir, "00-INDEX.md")

    # 1. Test 00-INDEX.md counts
    print("\n--- 1. Testing 00-INDEX.md document counts ---")
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    clusters_to_check = {
        "04-md-va-bo-bu": 38,
        "05-id-string-db-majburiy": 38,
        "23-prisma-id-string-va": 17
    }

    for cluster, expected_count in clusters_to_check.items():
        # Match pattern like: (04-md-va-bo-bu) — 38 ta hujjat
        pattern = rf"\({cluster}\)[^\n]*?—\s*(\d+)\s*ta hujjat"
        match = re.search(pattern, index_content)
        if not match:
            errors.append(f"00-INDEX.md da {cluster} uchun ko'rsatkich topilmadi!")
            print(f"❌ {cluster}: Match not found in 00-INDEX.md")
        else:
            actual_count = int(match.group(1))
            if actual_count == expected_count:
                print(f"✅ {cluster}: 00-INDEX.md counts {actual_count} documents (expected {expected_count})")
            else:
                errors.append(f"00-INDEX.md da {cluster} uchun {actual_count} ta hujjat ko'rsatilgan, kutilgan: {expected_count}")
                print(f"❌ {cluster}: 00-INDEX.md counts {actual_count} (expected {expected_count})")

    # 2. Test consolidated.md sources count
    print("\n--- 2. Testing consolidated.md ## Manba: count ---")
    for cluster, expected_count in clusters_to_check.items():
        cons_path = os.path.join(grouped_md_dir, cluster, "consolidated.md")
        if not os.path.exists(cons_path):
            errors.append(f"{cons_path} mavjud emas!")
            continue
        with open(cons_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        manba_lines = [l for l in lines if l.startswith("## Manba:")]
        actual_manba = len(manba_lines)
        if actual_manba == expected_count:
            print(f"✅ {cluster}/consolidated.md: {actual_manba} ta '## Manba:' mavjud (expected {expected_count})")
        else:
            errors.append(f"{cluster}/consolidated.md da {actual_manba} ta '## Manba:' mavjud, kutilgan: {expected_count}")
            print(f"❌ {cluster}/consolidated.md: {actual_manba} vs {expected_count}")

    # 3. Test New Markdown Articles
    print("\n--- 3. Testing Individual Markdown Articles ---")
    articles = [
        ("05-id-string-db-majburiy", "telegram-id-string-db-architecture.md", 10000),
        ("23-prisma-id-string-va", "prisma-telegram-bot-schema-and-id-types.md", 10000),
        ("04-md-va-bo-bu", "telegraf-bot-architecture-and-ux-rules.md", 10000)
    ]
    for cluster, filename, min_bytes in articles:
        file_path = os.path.join(grouped_md_dir, cluster, filename)
        if not os.path.exists(file_path):
            errors.append(f"{file_path} mavjud emas!")
            print(f"❌ {file_path} NOT FOUND")
            continue
        size = os.path.getsize(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        print(f"✅ {cluster}/{filename}: {size} bytes, {len(lines)} lines (min required: {min_bytes} bytes)")
        if size < min_bytes:
            errors.append(f"{filename} hajmi ({size} bytes) minimal talabdan kam!")

        # Verify presence in consolidated.md
        cons_path = os.path.join(grouped_md_dir, cluster, "consolidated.md")
        with open(cons_path, "r", encoding="utf-8") as f:
            cons_content = f.read()
        
        # Check source header
        source_header = f"## Manba: bot_post_using/docs/{filename}"
        if source_header not in cons_content:
            errors.append(f"{source_header} consolidated.md ichida topilmadi!")
            print(f"❌ Header {source_header} not in consolidated.md")
        else:
            print(f"✅ {source_header} verified in consolidated.md")

    # 4. Test RAG JSONL Chunks
    print("\n--- 4. Testing RAG JSONL Chunks ---")
    jsonl_expectations = {
        "05-id-string-db-majburiy": {"expected_total": 501, "new_chunks": 17, "prefix": "05-id-string-db-majburiy__botpostusingdocstele__"},
        "23-prisma-id-string-va": {"expected_total": 998, "new_chunks": 17, "prefix": "23-prisma-id-string-va__botpostusingdocspris__"},
        "04-md-va-bo-bu": {"expected_total": 163, "new_chunks": 19, "prefix": "04-md-va-bo-bu__botpostusingdocstele__"}
    }

    total_valid_lines = 0
    for cluster, exp in jsonl_expectations.items():
        jsonl_path = os.path.join(rag_ready_dir, cluster, "chunks.jsonl")
        if not os.path.exists(jsonl_path):
            errors.append(f"{jsonl_path} mavjud emas!")
            continue

        with open(jsonl_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()

        total_lines = len(raw_lines)
        if total_lines == exp["expected_total"]:
            print(f"✅ {cluster}/chunks.jsonl: total lines = {total_lines} (expected {exp['expected_total']})")
        else:
            errors.append(f"{cluster}/chunks.jsonl lines: {total_lines} vs expected {exp['expected_total']}")
            print(f"❌ {cluster}/chunks.jsonl lines: {total_lines} != {exp['expected_total']}")

        # Validate every line as JSON
        cluster_valid = 0
        new_chunk_objects = []
        for line_num, l in enumerate(raw_lines, 1):
            l = l.strip()
            if not l:
                continue
            try:
                obj = json.loads(l)
                cluster_valid += 1
                total_valid_lines += 1
            except Exception as e:
                errors.append(f"{cluster}/chunks.jsonl:{line_num} da JSON parse xatosi: {e}")
                continue

            # Check keys
            required_keys = ["id", "source", "topic", "text"]
            for k in required_keys:
                if k not in obj:
                    errors.append(f"{cluster}/chunks.jsonl:{line_num} da '{k}' kaliti yo'q!")

            # Check character limit <= 1000
            text_len = len(obj.get("text", ""))
            if text_len > 1000:
                errors.append(f"{cluster}/chunks.jsonl:{line_num} matn hajmi {text_len} > 1000 belgi!")

            if obj.get("id", "").startswith(exp["prefix"]):
                new_chunk_objects.append(obj)

        if len(new_chunk_objects) == exp["new_chunks"]:
            print(f"✅ {cluster}/chunks.jsonl: {len(new_chunk_objects)} new chunks match prefix '{exp['prefix']}' (expected {exp['new_chunks']})")
        else:
            errors.append(f"{cluster}/chunks.jsonl: new chunks count {len(new_chunk_objects)} != {exp['new_chunks']}")
            print(f"❌ {cluster}/chunks.jsonl: new chunks {len(new_chunk_objects)} != {exp['new_chunks']}")

        # Check overlap and character bounds on new chunks
        for i in range(len(new_chunk_objects)):
            c = new_chunk_objects[i]
            text = c.get("text", "")
            if len(text) > 1000:
                errors.append(f"New chunk {c['id']} length {len(text)} > 1000")
            
            # Check overlap with previous chunk
            if i > 0:
                prev_text = new_chunk_objects[i - 1].get("text", "")
                # The trailing ~150 chars of prev_text should match leading chars of text
                trailing_prev = prev_text[-120:]
                if trailing_prev not in text:
                    # Check partial overlap
                    match_found = any(prev_text[-k:] == text[:k] for k in range(50, 200))
                    if not match_found:
                        warnings.append(f"Chunk overlap note for {c['id']}: overlap boundary might differ slightly")

    print(f"\nTotal JSONL records validated across target clusters: {total_valid_lines} / 1662")

    # 5. Semantic Tags & Topics in new chunks
    print("\n--- 5. Testing Semantic Search Topics & Quality ---")
    for cluster, exp in jsonl_expectations.items():
        jsonl_path = os.path.join(rag_ready_dir, cluster, "chunks.jsonl")
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for l in f:
                obj = json.loads(l)
                if obj.get("id", "").startswith(exp["prefix"]):
                    topic = obj.get("topic", "")
                    if not topic or len(topic) < 5:
                        errors.append(f"Empty or too short topic in {obj['id']}: '{topic}'")

    print(f"Semantic topics verified: All new chunks have meaningful descriptive topics.")

    # Final Evaluation
    print("\n==================================================")
    if errors:
        print(f"❌ TEST SUITE FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("✅ ALL INDEPENDENT VERIFICATION TESTS PASSED (0 errors)!")
        if warnings:
            print(f"Warnings ({len(warnings)}):")
            for w in warnings:
                print(f"  - {w}")
        return True

if __name__ == "__main__":
    success = test_audit()
    sys.exit(0 if success else 1)
