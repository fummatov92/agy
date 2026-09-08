import os

TASKS = [
    {
        "cluster": "05-id-string-db-majburiy",
        "generated": "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_05.jsonl",
        "target": "/home/fayzillo/Downloads/brains/rag-ready/05-id-string-db-majburiy/chunks.jsonl",
    },
    {
        "cluster": "23-prisma-id-string-va",
        "generated": "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_23.jsonl",
        "target": "/home/fayzillo/Downloads/brains/rag-ready/23-prisma-id-string-va/chunks.jsonl",
    },
    {
        "cluster": "04-md-va-bo-bu",
        "generated": "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_04.jsonl",
        "target": "/home/fayzillo/Downloads/brains/rag-ready/04-md-va-bo-bu/chunks.jsonl",
    },
]

def append_chunks():
    for t in TASKS:
        with open(t["generated"], "r", encoding="utf-8") as f:
            new_lines = f.read()

        # Ensure newline at the end
        if not new_lines.endswith("\n"):
            new_lines += "\n"

        # Check existing target
        with open(t["target"], "r", encoding="utf-8") as f:
            target_content = f.read()

        # If target doesn't end with newline, add one
        prefix = ""
        if target_content and not target_content.endswith("\n"):
            prefix = "\n"

        with open(t["target"], "a", encoding="utf-8") as f:
            f.write(prefix + new_lines)

        print(f"Appended {t['generated']} to {t['target']}")

if __name__ == "__main__":
    append_chunks()
