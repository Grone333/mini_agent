# W8 · LangGraph 单 Agent + 网页界面

年报问答 Agent 的 LangGraph 版：把「检索 → 回答」做成显式状态图，并套上 Gradio 网页界面。
复用 W7_RAG 的向量库（Chroma，1316 个文本块）、重排与 DeepSeek 封装。

## 运行

```powershell
cd E:\mini_agent\W8_LangGraph
python app.py
```

## 状态流转图

```mermaid
flowchart LR
    START([START]) --> R[retrieve 节点<br/>向量召回 20 → Rerank 精排 5]
    R --> G[generate 节点<br/>检索结果 + 历史 + 问题 → DeepSeek]
    G --> END([END])

    subgraph MEM[Checkpoint 记忆 · MemorySaver + thread_id]
        CP[("State 快照<br/>history / context / answer")]
    end
    G -. 每轮结束保存快照 .-> CP
    CP -. 下一轮同会话恢复 .-> G
```

## 系统架构图

```mermaid
flowchart TB
    UI["Gradio 网页界面<br/>app.py"] --> APP["LangGraph 状态图<br/>graph.py"]
    APP --> RN["检索节点<br/>nodes.py"]
    APP --> GN["生成节点<br/>nodes.py"]
    RN --> VS[("Chroma 向量库<br/>W7 构建 · 1316 块")]
    RN --> RR["Rerank<br/>bge-reranker-v2-m3（硅基流动）"]
    GN --> LLM["DeepSeek v4-flash"]
    APP --> CP[("Checkpoint<br/>MemorySaver 多轮记忆")]
```

## 演示截图

（待补充）
