"""
语义搜索 — Embedding + ChromaDB 极简实现
=========================================
把文本片段转成向量存进 ChromaDB，输入问题后找到最相似的几条。

运行前：
  pip install chromadb openai
  export OPENAI_API_KEY="sk-xxx"    # 或用 .env 文件

用法：
  python semantic-search.py "如何部署Python应用"
"""

import os
import sys
import chromadb
from openai import OpenAI

# ── 配置 ────────────────────────────────────────────
COLLECTION_NAME = "docs"
EMBEDDING_MODEL = "text-embedding-3-small"  # 便宜、效果不错
DATA_FILE = os.path.join(os.path.dirname(__file__), "docs.txt")  # 语料文件

# ── 初始化 ──────────────────────────────────────────
client = OpenAI()  # 自动读 OPENAI_API_KEY 环境变量
chroma_client = chromadb.PersistentClient(path="./chroma_data")


def embed(texts: list[str]) -> list[list[float]]:
    """把文本列表转成 embedding 向量列表"""
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def build_index():
    """读取语料 → 生成向量 → 写入 ChromaDB"""
    if not os.path.exists(DATA_FILE):
        print(f"❌ 找不到语料文件: {DATA_FILE}")
        print("   请创建该文件，每行一条文本。")
        sys.exit(1)

    with open(DATA_FILE, encoding="utf-8") as f:
        docs = [line.strip() for line in f if line.strip()]

    if not docs:
        print("❌ 语料文件为空。")
        sys.exit(1)

    print(f"📖 读取 {len(docs)} 条文档，生成 embedding...")

    # 删掉旧 collection 重建
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = chroma_client.create_collection(name=COLLECTION_NAME)
    vectors = embed(docs)

    collection.add(
        ids=[str(i) for i in range(len(docs))],
        embeddings=vectors,
        documents=docs,
    )

    print(f"✅ 索引完成，{len(docs)} 条文档已写入 ChromaDB。")
    return collection


def search(query: str, collection, top_k: int = 3):
    """输入问题，返回最相关的 top_k 条文档"""
    query_vec = embed([query])[0]

    results = collection.query(
        query_embeddings=[query_vec],
        n_results=top_k,
        include=["documents", "distances"],
    )

    print(f"\n🔍 问题：{query}\n")
    for i, (doc, dist) in enumerate(
        zip(results["documents"][0], results["distances"][0])
    ):
        # distance 越小越相似（cosine distance）
        similarity = 1 - dist
        print(f"  #{i+1} [相似度 {similarity:.3f}]")
        print(f"     {doc}\n")


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else None
    collection = build_index()

    if query:
        search(query, collection)
        return

    # 交互模式
    print("\n💬 交互模式，输入问题回车搜索，输入 exit 退出。")
    while True:
        q = input("\n> ").strip()
        if q.lower() in ("exit", "quit", "q"):
            break
        if not q:
            continue
        search(q, collection)


if __name__ == "__main__":
    main()
