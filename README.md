# 语义搜索 — Embedding + ChromaDB

极简语义搜索项目，30 行核心逻辑，跑通「文本 → 向量 → 检索」全流程。

## 它做了什么

1. 读取 `docs.txt` 里的文本（一行一条）
2. 调用 OpenAI Embedding API 把每条文本转成向量
3. 向量存入 ChromaDB（本地持久化）
4. 输入任意问题，找出语义最相似的 3 条文档

## 为什么有用

这是 RAG 系统的心脏——从知识库中检索相关内容。没有这一步，RAG 无从谈起。

## 核心概念

| 概念 | 一句话 |
|------|--------|
| Embedding | 把文字变成一串数字，语义近的数字也近 |
| 向量数据库 | 专门存向量、做相似度搜索的数据库 |
| ChromaDB | 轻量开源向量数据库，Python 原生，零配置 |
| Cosine Distance | 两个向量之间的夹角，越小越相似 |

## 安装

```bash
pip install chromadb openai
```

## 配置

设置 OpenAI API Key：

```bash
export OPENAI_API_KEY="sk-xxx"
```

或者在项目目录下创建 `.env` 文件：

```
OPENAI_API_KEY=sk-xxx
```

## 运行

**单次查询：**

```bash
python semantic-search.py "如何部署Python应用"
```

**交互模式（不加参数）：**

```bash
python semantic-search.py
```

输出示例：

```
📖 读取 10 条文档，生成 embedding...
✅ 索引完成，10 条文档已写入 ChromaDB。

🔍 问题：如何部署Python应用

  #1 [相似度 0.622]
     Docker 是一个容器化平台，可以将应用及其依赖打包成镜像，实现环境一致性部署。

  #2 [相似度 0.518]
     Flask 是一个轻量级的 Python Web 框架，适合快速构建 API 和后端服务。

  #3 [相似度 0.408]
     Python 是一种解释型、面向对象的高级编程语言，广泛应用于数据科学、Web 开发和自动化脚本。
```

## 文件结构

```
semantic-search/
├── semantic-search.py   # 主程序
├── docs.txt             # 语料库（替换成你自己的数据）
├── README.md            # 本文件
└── chroma_data/         # ChromaDB 持久化目录，自动生成
```

## 下一步

搞定这个之后，把 `docs.txt` 替换成真实数据（PDF、网页、API 文档），加上分块策略，就是 RAG 的检索模块了。
