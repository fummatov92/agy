import json
import re
import os

TASKS = [
    {
        "article_path": "/home/fayzillo/Downloads/brains/grouped-md/05-id-string-db-majburiy/telegram-id-string-db-architecture.md",
        "cluster_name": "05-id-string-db-majburiy",
        "source": "bot_post_using/docs/telegram-id-string-db-architecture.md",
        "topic": "id-string-db-majburiy",
        "jsonl_path": "/home/fayzillo/Downloads/brains/rag-ready/05-id-string-db-majburiy/chunks.jsonl",
        "output_chunks_file": "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_05.jsonl",
    },
    {
        "article_path": "/home/fayzillo/Downloads/brains/grouped-md/23-prisma-id-string-va/prisma-telegram-bot-schema-and-id-types.md",
        "cluster_name": "23-prisma-id-string-va",
        "source": "bot_post_using/docs/prisma-telegram-bot-schema-and-id-types.md",
        "topic": "prisma-id-string-va",
        "jsonl_path": "/home/fayzillo/Downloads/brains/rag-ready/23-prisma-id-string-va/chunks.jsonl",
        "output_chunks_file": "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_23.jsonl",
    },
    {
        "article_path": "/home/fayzillo/Downloads/brains/grouped-md/04-md-va-bo-bu/telegraf-bot-architecture-and-ux-rules.md",
        "cluster_name": "04-md-va-bo-bu",
        "source": "bot_post_using/docs/telegraf-bot-architecture-and-ux-rules.md",
        "topic": "md-va-bo-bu",
        "jsonl_path": "/home/fayzillo/Downloads/brains/rag-ready/04-md-va-bo-bu/chunks.jsonl",
        "output_chunks_file": "/home/fayzillo/Downloads/brains/.agents/worker_1/chunks_04.jsonl",
    },
]

def make_slug20(source: str) -> str:
    # keep only alphanumeric characters, lowercase, first 20 chars
    clean = re.sub(r'[^a-zA-Z0-9]', '', source).lower()
    return clean[:20]

def chunk_text(text: str, max_chars: int = 1000, step: int = 850):
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + max_chars, text_len)
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= text_len:
            break
        start += step
    return chunks

def process():
    for task in TASKS:
        with open(task["article_path"], "r", encoding="utf-8") as f:
            content = f.read()

        slug20 = make_slug20(task["source"])
        chunks = chunk_text(content, max_chars=1000, step=850)
        
        lines = []
        for idx, ch in enumerate(chunks):
            chunk_id = f"{task['cluster_name']}__{slug20}__{idx}"
            record = {
                "id": chunk_id,
                "source": task["source"],
                "topic": task["topic"],
                "text": ch
            }
            # Verify record has exact 4 keys
            assert list(record.keys()) == ["id", "source", "topic", "text"]
            assert len(ch) <= 1000
            json_line = json.dumps(record, ensure_ascii=False)
            lines.append(json_line)
        
        with open(task["output_chunks_file"], "w", encoding="utf-8") as out:
            for l in lines:
                out.write(l + "\n")
                
        print(f"Cluster {task['cluster_name']}: Generated {len(lines)} chunks. Slug: {slug20}")

if __name__ == "__main__":
    process()
