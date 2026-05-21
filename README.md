# Semantic Search

> 基于 OpenAI Embedding + ChromaDB 的极简语义搜索引擎实现

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 概述

将文本通过 Embedding 模型转为向量，存入 ChromaDB 向量数据库，支持自然语言语义检索。本项目是 RAG（检索增强生成）系统检索模块的最小可行实现。

## 架构

```
docs.txt ──→ Embedding API ──→ ChromaDB
                                    ↑
用户输入 ──→ Embedding API ──→ 向量检索 ──→ 返回 Top-K 结果
```

## 前置依赖

| 依赖 | 用途 |
|------|------|
| Python 3.10+ | 运行环境 |
| openai | 调用 text-embedding-3-small 模型 |
| chromadb | 本地向量数据库，存储与检索 |

## 快速开始

### 1. 安装

```bash   ”“bash
pip install chromadb openaiPIP安装chromadb openai
```

### 2. 配置 API Key

```bash   ”“bash
export OPENAI_API_KEY="sk-***"
```

或在项目根目录创建 `.env` 文件：

```
OPENAI_API_KEY=sk-***
```

### 3. 准备语料

编辑 `docs.txt`，每行一条文档。仓库自带 10 条示例数据，可直接运行。

### 4. 运行

```bash   ”“bash
# 交互模式
python semantic-search.py

# 单次查询
python semantic-search.py "你的问题"
```

## 使用示例

```text
📖 读取 10 条文档，生成 embedding...
✅ 索引完成，10 条文档已写入 ChromaDB。

🔍 问题：如何部署Python应用

  #1 [相似度 0.622]
     Docker 是一个容器化平台，可以将应用及其依赖打包成镜像...

  #2 [相似度 0.518]
     Flask 是一个轻量级的 Python Web 框架，适合快速构建 API...

  #3 [相似度 0.408]
     Python 是一种解释型、面向对象的高级编程语言...
```

## 核心接口

### embed(texts) → list[list[float]]

将文本列表转为 embedding 向量列表。

```python
vectors = embed(["Python 是什么", "Docker 怎么用"])
# [[0.012, -0.034, ...], [0.045, 0.002, ...]]
```

### collection.query(query_embeddings, n_results)

在向量库中检索与查询向量最相似的文档。

```python
results = collection.query(
    query_embeddings=[query_vec],
    n_results=3,
)
```

## 关键概念

- **Embedding**：将非结构化文本映射为固定维度的稠密向量，语义相近的文本在向量空间中距离更近
- **ChromaDB**：轻量级开源向量数据库，Python 原生，支持内存/持久化两种模式
- **Cosine Distance**：两个向量夹角的余弦值，范围 [0, 2]，越小表示越相似

## 目录结构

```
semantic-search/   语义搜索/
├── semantic-search.py   # 主程序
├── docs.txt             # 语料库
├── README.md
└── chroma_data/         # ChromaDB 数据目录（自动生成）
```

## 后续路线

本项目 → [simple-rag](#) → [enterprise-rag](#) → [agent-demo](#)

学完本项目后，下一步是增加大模型生成环节，实现完整的 RAG 管线。

## License

MIT   用
