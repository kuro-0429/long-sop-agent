# 超长 SOP 场景下的 Agent 上下文动态路由与多模态质检系统 —— 完整实施手册

---

## 一、前置知识学习路线（建议在正式开发前用 3-5 天集中突破）

### 1.1 RAG（检索增强生成）—— 从零到能用

**核心概念（2小时）：**

- RAG 的本质：不是让模型"记住"所有内容，而是在调用模型前，先从外部知识库里检索出最相关的片段，塞进 prompt 里一起发给模型
- 流程：文档 → 切分成小块（chunking） → 每块转成向量（embedding） → 存进向量数据库 → 用户提问时，先把问题转成向量 → 在数据库里找最相似的块 → 把这些块和问题一起发给 LLM

**必看资料（按优先级）：**

1. LangChain 官方 RAG 教程：https://python.langchain.com/docs/tutorials/rag/（跟着跑一遍，2-3小时）
2. 吴恩达 × LangChain 短课：https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/（免费，3小时视频）
3. ChromaDB 官方 Getting Started：https://docs.trychroma.com/getting-started（30分钟）

**动手练习（3-4小时）：**

- 用 LangChain 的 `RecursiveCharacterTextSplitter` 把一个 markdown 文件切块
- 用 `sentence-transformers` 的 `bge-large-zh-v1.5` 做 embedding
- 存入 ChromaDB，写一个检索 query，看返回结果是否合理
- 试不同的 chunk_size（256/512/1024）和 chunk_overlap（50/100），观察检索质量差异

### 1.2 LangGraph —— 状态机编排

**核心概念（1.5小时）：**

- LangGraph 是 LangChain 团队做的 Agent 编排框架，核心思想是把 Agent 的工作流建模为一个**有向图**（Graph）
- 图里有**节点**（Node，每个节点是一个函数，比如"意图识别"、"RAG检索"、"生成"）和**边**（Edge，决定节点之间的流转逻辑）
- **State** 是贯穿整个图的共享数据结构，每个节点读取 state、处理、写回 state
- 条件边（Conditional Edge）：根据当前 state 决定下一步走哪个节点（这就是你的"路由"）

**必看资料：**

1. LangGraph 官方教程（必看前3个）：https://langchain-ai.github.io/langgraph/tutorials/
2. LangChain 的 context_engineering 仓库（你项目的直接参考）：https://github.com/langchain-ai/context_engineering
3. LangGraph 的 `StateGraph` API 文档：重点看 `add_node`、`add_edge`、`add_conditional_edges`

**动手练习（3-4小时）：**

- 搭一个最简单的 3 节点图：input → classify_intent → (条件分支) → node_A 或 node_B
- State 用 TypedDict 定义，包含 `query: str`、`intent: str`、`result: str`
- 条件边根据 intent 字段路由到不同节点

### 1.3 Embedding 与向量检索 —— 理解原理

**核心概念（1小时）：**

- Embedding：把文本映射成一个固定长度的浮点数向量（比如 1024维），语义相近的文本向量距离近
- 向量数据库（ChromaDB/FAISS）：专门做向量相似度搜索的数据库，核心操作是 `add`（存入）和 `query`（检索 top-k 最相似的）
- Reranker：第一轮检索用向量搜索（快但粗糙），第二轮用交叉编码器（Cross-Encoder）对候选结果精排（慢但准），这就是 BGE-Reranker 的作用

**必看资料：**

1. MTEB Leaderboard（选 embedding 模型的参考）：https://huggingface.co/spaces/mteb/leaderboard
2. BGE 系列模型文档：https://huggingface.co/BAAI/bge-large-zh-v1.5
3. BGE-Reranker 使用方法：https://huggingface.co/BAAI/bge-reranker-v2-m3

### 1.4 Function Calling —— 工具调用基础

**核心概念（1小时）：**

- Function Calling 是让 LLM 输出结构化的"函数调用指令"而非纯文本
- 你定义好函数的 name、description、parameters（JSON Schema），LLM 决定什么时候调用、传什么参数
- LangChain 里用 `@tool` 装饰器或 `StructuredTool` 定义工具，LangGraph 里用 `ToolNode` 处理工具调用

**必看资料：**

- LangChain Tools 文档：https://python.langchain.com/docs/concepts/tools/
- OpenAI Function Calling 文档（原理相通）：https://platform.openai.com/docs/guides/function-calling

### 1.5 SFT + DPO —— 微调基础

**核心概念（2小时）：**

- SFT（Supervised Fine-Tuning）：用"问题→标准答案"的数据对模型做监督微调，让它学会特定任务的输出格式和决策模式
- DPO（Direct Preference Optimization）：用"同一问题的好答案 vs 坏答案"偏好对来对齐模型行为，不需要训练 reward model，比 RLHF 简单很多
- TRL 库：HuggingFace 的训练库，封装了 SFT/DPO/PPO，几十行代码就能跑通

**必看资料：**

1. TRL 官方 SFT 教程：https://huggingface.co/docs/trl/sft_trainer
2. TRL 官方 DPO 教程：https://huggingface.co/docs/trl/dpo_trainer
3. Qwen2.5 微调指南：https://qwen.readthedocs.io/en/latest/training/SFT/llama_factory.html

---

## 二、算力与环境要求

### 2.1 开发环境（全程必备）

| 项目     | 最低要求         | 推荐配置     |
| -------- | ---------------- | ------------ |
| CPU      | 4核              | 8核+         |
| 内存     | 16GB             | 32GB         |
| 硬盘     | 50GB 可用空间    | 100GB SSD    |
| Python   | 3.10+            | 3.11         |
| 操作系统 | Linux/macOS/WSL2 | Ubuntu 22.04 |

### 2.2 各模块算力需求

| 模块                       | GPU 需求                 | 可替代方案                                                   |
| -------------------------- | ------------------------ | ------------------------------------------------------------ |
| RAG + LangGraph（第1-2周） | **不需要 GPU**           | 纯 CPU 即可，embedding 用 CPU 跑 bge-large-zh 也很快（几百条文档几分钟） |
| ChromaDB 向量检索          | **不需要 GPU**           | 纯 CPU                                                       |
| BGE-Reranker 重排序        | **不需要 GPU**（推荐有） | CPU 可跑但慢一些，有 GPU 会快 10x                            |
| LLM 调用（意图分类/生成）  | **不需要本地 GPU**       | 调 API：通义千问 qwen-plus / DeepSeek API / Claude API       |
| VLM 视觉质检（第3周）      | **不需要本地 GPU**       | 调 API：通义千问 VL（qwen-vl-max）免费额度够用               |
| Playwright 截图            | **不需要 GPU**           | 纯 CPU                                                       |
| SFT + DPO 训练（第4周）    | **需要 GPU**             | 见下方详细说明                                               |

### 2.3 SFT + DPO 训练的具体算力要求

**目标模型：Qwen2.5-1.5B（推荐）或 Qwen2.5-3B**

| 模型大小     | 训练方式 | 最低 GPU            | 显存需求 | 单次训练时间            |
| ------------ | -------- | ------------------- | -------- | ----------------------- |
| Qwen2.5-1.5B | LoRA SFT | T4 16GB             | ~12GB    | 30-60分钟（几百条数据） |
| Qwen2.5-1.5B | LoRA DPO | T4 16GB             | ~14GB    | 30-60分钟               |
| Qwen2.5-3B   | LoRA SFT | A10 24GB / RTX 3090 | ~18GB    | 1-2小时                 |
| Qwen2.5-3B   | LoRA DPO | A10 24GB / RTX 3090 | ~20GB    | 1-2小时                 |
| Qwen2.5-7B   | LoRA SFT | A100 40GB           | ~30GB    | 2-4小时                 |

**免费/低成本 GPU 获取方式：**

1. **Google Colab Pro**（推荐）：~70元/月，T4/A100 按需分配，跑 1.5B 绰绰有余
2. **Kaggle Notebooks**：免费，每周 30 小时 T4 GPU
3. **AutoDL**：~2元/小时 RTX 3090，按量付费，跑完就关
4. **实验室服务器**：如果有的话优先用

**推荐策略：前3周完全不需要GPU，第4周用Colab/Kaggle/AutoDL跑2-3天即可。总GPU成本预估：50-100元。**

### 2.4 API 费用估算

| API                  | 用途               | 预估调用量         | 费用               |
| -------------------- | ------------------ | ------------------ | ------------------ |
| 通义千问 qwen-plus   | 意图分类、代码生成 | ~2000次            | 免费额度内 / ~20元 |
| 通义千问 qwen-vl-max | VLM 视觉质检       | ~500次（截图评估） | 免费额度内 / ~15元 |
| DeepSeek API（备选） | 意图分类、生成     | ~2000次            | ~10元              |

**总预算：GPU 50-100元 + API 0-50元 = 50-150元**

---

## 三、Python 环境与依赖安装

```bash
# 创建虚拟环境
conda create -n agent-router python=3.11 -y
conda activate agent-router

# 核心依赖（第1周就全装好）
pip install langchain langgraph langchain-community langchain-openai
pip install chromadb sentence-transformers
pip install FlagEmbedding  # BGE embedding + reranker
pip install dashscope  # 通义千问 API
pip install openai  # 备用 API 调用

# 评测与工具（第2-3周）
pip install playwright pytest
playwright install chromium
pip install Pillow requests

# 微调（第4周）
pip install transformers datasets trl peft accelerate bitsandbytes
pip install torch  # 如果 GPU 环境需要单独装

# 可选
pip install pandas matplotlib  # 数据分析和画图
```

---

## 四、项目目录结构

```
agent-sop-router/
├── README.md
├── requirements.txt
├── configs/                     # 你的 SOP 配置文件（从字节项目拷贝过来）
│   ├── techniques/              # 技法库 T-01 ~ T-80
│   ├── workflows/               # 流程节点定义
│   └── constraints/             # 约束规则
├── src/
│   ├── chunking/                # 文档切分模块
│   │   ├── __init__.py
│   │   ├── fixed_window.py      # 固定窗口切分
│   │   ├── semantic_boundary.py # 语义边界切分
│   │   └── structured_tag.py    # 结构化标签切分
│   ├── indexing/                 # 向量索引模块
│   │   ├── __init__.py
│   │   ├── embedder.py          # embedding 封装
│   │   ├── chroma_store.py      # ChromaDB 操作
│   │   └── reranker.py          # BGE-Reranker 重排序
│   ├── graph/                   # LangGraph 状态机
│   │   ├── __init__.py
│   │   ├── state.py             # State 定义
│   │   ├── nodes.py             # 各节点实现
│   │   ├── router.py            # 条件路由逻辑
│   │   └── pipeline.py          # 完整 Graph 组装
│   ├── tools/                   # Function Calling 工具定义
│   │   ├── __init__.py
│   │   ├── technique_selector.py
│   │   ├── subprocess_trigger.py
│   │   └── constraint_checker.py
│   ├── vlm/                     # VLM 视觉质检
│   │   ├── __init__.py
│   │   ├── screenshot.py        # Playwright 截图
│   │   └── vlm_judge.py         # VLM 评分逻辑
│   └── evaluation/              # 评测框架
│       ├── __init__.py
│       ├── rule_validators.py   # 可机检规则验证器
│       ├── vlm_scorer.py        # VLM 评分
│       └── metrics.py           # 指标计算（按位置/类型分维度）
├── training/                    # SFT + DPO 微调
│   ├── data/
│   │   ├── prepare_sft_data.py  # 构造 SFT 训练数据
│   │   └── prepare_dpo_data.py  # 构造 DPO 偏好对
│   ├── train_sft.py
│   ├── train_dpo.py
│   └── eval_model.py            # 微调前后对比评测
├── experiments/                  # 实验记录
│   ├── baseline_full_context/   # 全量 12 万 token 基线
│   ├── dynamic_routing/         # 动态路由实验
│   ├── chunking_comparison/     # 分块策略对比
│   └── medical_transfer/        # 医疗场景迁移验证
├── scripts/
│   ├── build_index.py           # 一键构建向量索引
│   ├── run_pipeline.py          # 运行完整 pipeline
│   ├── run_evaluation.py        # 运行评测
│   └── run_baseline.py          # 运行全量 baseline
└── notebooks/
    ├── 01_chunking_exploration.ipynb
    ├── 02_retrieval_quality.ipynb
    └── 03_results_visualization.ipynb
```

---

## 五、四周详细执行计划

---

### 第一周：LangGraph + RAG 核心管线（~40小时）

> **本周目标：跑通端到端 pipeline，能演示"全量 12 万 token vs. 动态路由 5000 token"的对比**

#### Day 1-2（10h）：学习 + 环境搭建

**Day 1（5h）：**

- [ ] 2h：通读 LangChain RAG 教程，跟着跑通官方示例
- [ ] 2h：通读 LangGraph 教程前3个（Introduction / Quick Start / Chatbot）
- [ ] 1h：安装所有依赖，确认环境可用，通义千问 API key 配好

**Day 2（5h）：**

- [ ] 2h：学习 ChromaDB 基本操作（add / query / delete），用一个小文档测试
- [ ] 2h：学习 sentence-transformers 的 bge-large-zh-v1.5，跑一个 embedding 示例
- [ ] 1h：把你的 SOP 配置文件（configs/）整理好，确认文件结构清晰

#### Day 3-4（10h）：文档切分与向量索引

**Day 3（5h）：**

- [ ] 3h：实现三种切分策略

  - `fixed_window.py`：RecursiveCharacterTextSplitter，chunk_size=512, overlap=100
  - `semantic_boundary.py`：按你 SOP 文件的 markdown 标题（## / ###）切分
  - `structured_tag.py`：按技法条目（T-01 ~ T-80 各为一个 chunk）、流程节点、约束规则做结构化切分（这是最适合你场景的方式）

- [ ] 2h：实现 `embedder.py` 和 `chroma_store.py`

  ```python
  # embedder.py 核心逻辑
  from sentence_transformers import SentenceTransformer
  model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
  embeddings = model.encode(chunks, normalize_embeddings=True)
  
  # chroma_store.py 核心逻辑
  import chromadb
  client = chromadb.PersistentClient(path="./chroma_db")
  collection = client.get_or_create_collection("sop_chunks")
  collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)
  ```

**Day 4（5h）：**

- [ ] 2h：跑 `build_index.py`，用三种切分策略分别建索引

- [ ] 2h：写检索测试——手动准备 10 个 query（比如"Glassmorphism 技法要求"、"响应式适配的强制规则"），对比三种策略的 top-5 检索结果质量

- [ ] 1h：实现 `reranker.py`

  ```python
  # reranker.py 核心逻辑
  from FlagEmbedding import FlagReranker
  reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)
  scores = reranker.compute_score([[query, doc] for doc in candidates])
  # 按分数重排序
  ```

#### Day 5-6（10h）：LangGraph 状态机

**Day 5（5h）：**

- [ ] 3h：定义 State 和基础节点

  ```python
  # state.py
  from typing import TypedDict, Literal
  
  class AgentState(TypedDict):
      user_query: str                    # 用户输入的设计 brief
      intent: str                        # 意图分类结果
      retrieved_chunks: list[str]        # RAG 检索到的片段
      context: str                       # 拼接后注入的 context
      generation_result: str             # 生成结果
      quality_check: dict                # 质检结果
      
  # nodes.py
  def classify_intent(state: AgentState) -> AgentState:
      """调用 LLM 对 user_query 做意图分类"""
      # 意图类型：technique_selection / main_generation / quality_check / subprocess_trigger
      prompt = f"请对以下设计需求进行意图分类...\n{state['user_query']}"
      response = call_llm(prompt)  # 调通义千问 API
      return {"intent": response}
  
  def retrieve_context(state: AgentState) -> AgentState:
      """根据意图 + query 检索相关 SOP 片段"""
      # 根据 intent 决定检索哪些 collection 或用什么过滤条件
      results = collection.query(query_texts=[state['user_query']], n_results=10)
      # rerank
      reranked = reranker.rerank(state['user_query'], results)
      return {"retrieved_chunks": reranked[:5], "context": "\n".join(reranked[:5])}
  
  def generate(state: AgentState) -> AgentState:
      """用检索到的 context + query 调用 LLM 生成"""
      prompt = f"基于以下设计规范：\n{state['context']}\n\n请完成：{state['user_query']}"
      result = call_llm(prompt)
      return {"generation_result": result}
  ```

- [ ] 2h：组装 Graph

  ```python
  # pipeline.py
  from langgraph.graph import StateGraph, END
  
  workflow = StateGraph(AgentState)
  workflow.add_node("classify", classify_intent)
  workflow.add_node("retrieve", retrieve_context)
  workflow.add_node("generate", generate)
  workflow.add_node("check", quality_check)
  
  workflow.set_entry_point("classify")
  workflow.add_edge("classify", "retrieve")
  workflow.add_edge("retrieve", "generate")
  workflow.add_edge("generate", "check")
  
  # 条件边：质检通过 → END，不通过 → 回到 retrieve 重试
  workflow.add_conditional_edges("check", route_after_check, {"pass": END, "retry": "retrieve"})
  
  app = workflow.compile()
  ```

**Day 6（5h）：**

- [ ] 3h：调试整个 pipeline，用 3 个真实的设计 brief 跑通端到端
- [ ] 2h：跑 baseline 对比——同样的 3 个 brief，分别用全量 12 万 token 和动态路由，记录：实际注入的 token 数、生成结果质量（人工看）、规则遵循情况

#### Day 7（10h）：打磨 + 基线数据

- [ ] 3h：修复前6天发现的 bug，优化检索质量（调整 top-k、reranker 阈值）
- [ ] 3h：扩大测试——用 10-15 个不同类型的设计 brief 跑 pipeline，开始积累轨迹数据（后面 SFT 要用）
- [ ] 2h：记录关键指标——平均注入 token 数、检索 recall（人工标注 10 个 query 的 ground truth）
- [ ] 2h：整理代码，写 README，确保可复现

**第一周交付物：**

- ✅ 可运行的 LangGraph + RAG pipeline
- ✅ 三种分块策略的检索质量对比数据
- ✅ 全量 vs. 动态路由的初步对比（token 数 + 人工评估）
- ✅ 10-15 条 pipeline 运行轨迹（用于后续训练数据）

---

### 第二周：Function Calling + 评测框架（~35小时）

> **本周目标：给 pipeline 加上 Function Calling 工具链，搭建自动化评测框架**

#### Day 8-9（10h）：Function Calling 工具定义

**Day 8（5h）：**

- [ ] 3h：设计并实现 3 个核心工具

  ```python
  # technique_selector.py
  from langchain.tools import tool
  
  @tool
  def search_techniques(brief: str, style: str, count: int = 5) -> str:
      """根据设计 brief 和风格从技法库中检索推荐技法组合。
      Args:
          brief: 设计需求描述
          style: 目标风格（Dark Mode / Glassmorphism / Bento Grid 等）
          count: 推荐技法数量
      Returns:
          推荐的技法列表，包含技法 ID、名称、适用条件、与其他技法的冲突关系
      """
      # 调用 RAG 检索技法库
      results = technique_collection.query(query_texts=[f"{brief} {style}"], n_results=count*2)
      # rerank + 冲突检测
      ...
  
  # subprocess_trigger.py
  @tool
  def check_subprocess_trigger(current_stage: str, completed_steps: list[str]) -> str:
      """判断当前阶段是否需要触发子流程（响应式适配/交互验收等）。
      Args:
          current_stage: 当前所处阶段
          completed_steps: 已完成的步骤列表
      Returns:
          需要触发的子流程列表及其优先级
      """
      ...
  
  # constraint_checker.py
  @tool
  def validate_constraints(generation: str, required_techniques: list[str]) -> str:
      """检查生成结果是否满足硬性约束规则。
      Args:
          generation: 生成的 HTML 代码
          required_techniques: 要求使用的技法列表
      Returns:
          违反的规则列表及修复建议
      """
      ...
  ```

- [ ] 2h：将工具集成到 LangGraph pipeline，在 generate 节点前加入工具调用

**Day 9（5h）：**

- [ ] 3h：测试 Function Calling 链路——确保 LLM 能正确决定何时调用哪个工具、传什么参数
- [ ] 2h：处理边缘情况——LLM 不调用工具、调用参数格式错误、工具返回异常

#### Day 10-11（10h）：自动化评测框架

**Day 10（5h）：**

- [ ] 4h：实现规则验证器

  ```python
  # rule_validators.py
  import re
  
  class RuleValidator:
      def check_technique_diversity(self, result: dict, min_count: int = 5) -> dict:
          """检查使用的技法种类是否 >= min_count"""
          used = result.get("techniques_used", [])
          return {"pass": len(set(used)) >= min_count, "actual": len(set(used)), "required": min_count}
      
      def check_interaction_types(self, html: str, min_types: int = 5) -> dict:
          """检查交互种类是否 >= 5（hover/click/scroll/input/animation 等）"""
          patterns = {
              "hover": r":hover|mouseenter|mouseover",
              "click": r"onclick|click|addEventListener.*click",
              "scroll": r"scroll|IntersectionObserver|parallax",
              "input": r"<input|<textarea|<select|contenteditable",
              "animation": r"@keyframes|animation:|transition:|requestAnimationFrame",
              "drag": r"drag|draggable|ondragstart",
              "resize": r"resize|ResizeObserver|@media",
          }
          found = [k for k, v in patterns.items() if re.search(v, html, re.I)]
          return {"pass": len(found) >= min_types, "actual": len(found), "types": found}
      
      def check_prompt_rounds(self, trajectory: list, min_rounds: int = 3) -> dict:
          """检查 Prompt 轮次是否 >= 3"""
          rounds = len([t for t in trajectory if t["role"] == "user"])
          return {"pass": rounds >= min_rounds, "actual": rounds}
      
      def check_technique_position_distribution(self, techniques_used: list[str]) -> dict:
          """按技法位置（头部T-01~T-20/中部T-21~T-50/尾部T-51~T-80）分组统计调用率"""
          head = [t for t in techniques_used if 1 <= int(t.split("-")[1]) <= 20]
          mid = [t for t in techniques_used if 21 <= int(t.split("-")[1]) <= 50]
          tail = [t for t in techniques_used if 51 <= int(t.split("-")[1]) <= 80]
          return {"head": len(head), "mid": len(mid), "tail": len(tail)}
  ```

- [ ] 1h：用 pytest 封装成测试 suite

  ```python
  # test_evaluation.py
  def test_technique_diversity(pipeline_result):
      result = validator.check_technique_diversity(pipeline_result)
      assert result["pass"], f"技法多样性不足：{result['actual']}/{result['required']}"
  ```

**Day 11（5h）：**

- [ ] 3h：跑大批量实验——20-30 个设计 brief，分别用全量 baseline 和动态路由各跑一遍
- [ ] 2h：整理对比数据，按维度分组：
  - 按技法位置：头部/中部/尾部调用率对比
  - 按规则类型：硬约束（必须满足）vs 软偏好（建议满足）的遵循率
  - 整体：平均 token 压缩率、规则总遵循率

#### Day 12-14（15h）：数据积累 + 轨迹采集

- [ ] 每天跑 10-15 个 pipeline 任务，手动标注质量（通过/不通过/部分通过）
- [ ] 记录每条轨迹的完整信息：query → intent → 检索结果 → 工具调用 → 生成结果 → 质检结果
- [ ] 本周末应积累 **60-80 条带标注的轨迹数据**（第4周 SFT/DPO 的训练数据来源）
- [ ] 把医疗分诊 Skill 的 SOP 文档也切分建索引（为第三周跨场景验证做准备）

**第二周交付物：**

- ✅ 3 个 Function Calling 工具集成到 pipeline
- ✅ 自动化评测框架（规则验证器 + pytest suite）
- ✅ 全量 vs. 动态路由的分维度对比数据（20-30 条）
- ✅ 60-80 条带标注的 pipeline 运行轨迹

---

### 第三周：VLM 视觉质检 + 跨场景验证（~35小时）

> **本周目标：VLM 双通道质检跑通、医疗场景迁移验证完成**

#### Day 15-16（10h）：Playwright 截图 + VLM Judge

**Day 15（5h）：**

- [ ] 2h：实现 Playwright 自动截图

  ```python
  # screenshot.py
  from playwright.async_api import async_playwright
  import asyncio
  
  async def capture_screenshot(html_path: str, output_path: str, viewport=(1440, 900)):
      async with async_playwright() as p:
          browser = await p.chromium.launch()
          page = await browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
          await page.goto(f"file://{html_path}")
          await page.wait_for_timeout(2000)  # 等待动画/渲染
          await page.screenshot(path=output_path, full_page=True)
          await browser.close()
  ```

- [ ] 3h：实现 VLM Judge

  ```python
  # vlm_judge.py
  import dashscope
  
  def vlm_evaluate(screenshot_path: str) -> dict:
      """调用 Qwen-VL 对截图进行视觉质检"""
      with open(screenshot_path, "rb") as f:
          image_data = base64.b64encode(f.read()).decode()
      
      messages = [{"role": "user", "content": [
          {"image": f"data:image/png;base64,{image_data}"},
          {"text": """请作为专业的 Web Design 质检员，对这个网页截图进行评估。
          请严格按以下 JSON 格式输出评分（每项 1-10 分）：
          {
              "layout_rationality": <分数>,    // 布局合理性：元素对齐、间距一致性、视觉层次
              "color_consistency": <分数>,      // 配色一致性：色彩搭配协调、对比度合适
              "interaction_visibility": <分数>, // 交互元素可见性：按钮/链接/表单是否清晰可辨
              "text_readability": <分数>,       // 文字可读性：字号合适、无溢出截断
              "rendering_quality": <分数>,      // 渲染质量：无明显的 CSS 渲染缺陷
              "overall": <分数>,
              "defects": [<发现的具体缺陷列表>]
          }"""}
      ]}]
      
      response = dashscope.MultiModalConversation.call(
          model="qwen-vl-max", messages=messages
      )
      return json.loads(response.output.choices[0].message.content[0]["text"])
  ```

**Day 16（5h）：**

- [ ] 3h：对已有的 20-30 条生成结果全部跑截图 + VLM 评分
- [ ] 2h：对比 text-only 规则检查 vs. VLM 视觉评分——统计 VLM 多检出了哪些 text-only 漏掉的缺陷（重点关注：glassmorphism 渲染失败、clip-path 动画丢失、响应式布局断裂等）

#### Day 17-18（10h）：医疗分诊场景迁移验证

**Day 17（5h）：**

- [ ] 2h：整理医疗分诊 Skill 的 SOP 文档，按语义单元切分建索引
  - 危急筛查规则、药物相互作用检测规则、慢病随访规则、年龄分层规则等
- [ ] 3h：复用同一套 LangGraph pipeline，只替换 configs 和向量索引，在医疗场景下跑 10 个测试 case

**Day 18（5h）：**

- [ ] 3h：对比医疗场景下全量 vs. 动态路由的规则遵循率
- [ ] 2h：整理跨场景对比数据——Web Design 和医疗分诊的指标放在一起，证明框架通用性

#### Day 19-21（15h）：扩大数据积累 + 整理

- [ ] 继续跑 pipeline 积累轨迹，目标总计达到 **120-150 条**（含 Web Design + 医疗两个场景）
- [ ] 对每条轨迹标注：通过/不通过、失败原因分类
- [ ] 从中构造 DPO 偏好对初稿：
  - chosen：质检全通过的轨迹中的 intent → tool_call 决策序列
  - rejected：质检不通过的轨迹中的对应决策序列
  - 目标：50-80 对高质量偏好对
- [ ] 整理所有评测数据，画对比图表

**第三周交付物：**

- ✅ VLM 视觉质检模块（截图 + 评分 + 与 text-only 对比）
- ✅ 医疗分诊场景迁移验证数据
- ✅ 120-150 条带标注轨迹 + 50-80 对 DPO 偏好对
- ✅ 双场景对比报告草稿

---

### 第四周：SFT + DPO 微调 + 收尾（~40小时）

> **本周目标：跑通微调、填上所有 XX% 数据、简历定稿**

#### Day 22-23（10h）：SFT 数据构造与训练

**Day 22（5h）：**

- [ ] 3h：构造 SFT 训练数据

  ```python
  # prepare_sft_data.py
  # 从轨迹中提取：user_query → (intent, tool_calls) 的映射
  # 格式化为 instruction-following 格式：
  sft_data = []
  for trajectory in all_trajectories:
      sft_data.append({
          "instruction": f"你是一个 Agent 路由决策器。给定以下设计需求，请输出意图分类和推荐的工具调用。\n\n设计需求：{trajectory['query']}",
          "output": json.dumps({
              "intent": trajectory["intent"],
              "tool_calls": trajectory["tool_calls"],
              "techniques": trajectory["selected_techniques"]
          }, ensure_ascii=False)
      })
  # 保存为 jsonl
  ```

- [ ] 2h：在 Colab/AutoDL 上配置环境，下载 Qwen2.5-1.5B

**Day 23（5h）：**

- [ ] 4h：跑 SFT 训练

  ```python
  # train_sft.py
  from transformers import AutoModelForCausalLM, AutoTokenizer
  from trl import SFTTrainer, SFTConfig
  from peft import LoraConfig
  from datasets import load_dataset
  
  model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct", torch_dtype="auto")
  tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
  
  dataset = load_dataset("json", data_files="sft_data.jsonl")
  
  lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"], lora_dropout=0.05)
  
  training_args = SFTConfig(
      output_dir="./sft_output",
      num_train_epochs=3,
      per_device_train_batch_size=4,
      gradient_accumulation_steps=4,
      learning_rate=2e-4,
      logging_steps=10,
      save_steps=50,
  )
  
  trainer = SFTTrainer(model=model, args=training_args, train_dataset=dataset["train"], peft_config=lora_config)
  trainer.train()
  ```

- [ ] 1h：SFT 模型快速评估——在测试集上跑几个 case，检查输出格式是否正确

#### Day 24-25（10h）：DPO 训练

**Day 24（5h）：**

- [ ] 3h：构造 DPO 偏好对数据

  ```python
  # prepare_dpo_data.py
  dpo_data = []
  # 相同 query 下，质检通过的轨迹 vs 不通过的轨迹
  for query_group in grouped_trajectories:
      chosen = [t for t in query_group if t["quality_check"]["pass"]]
      rejected = [t for t in query_group if not t["quality_check"]["pass"]]
      if chosen and rejected:
          dpo_data.append({
              "prompt": query_group[0]["query"],
              "chosen": json.dumps(chosen[0]["decisions"]),
              "rejected": json.dumps(rejected[0]["decisions"]),
          })
  ```

- [ ] 2h：跑 DPO 训练

  ```python
  # train_dpo.py
  from trl import DPOTrainer, DPOConfig
  
  dpo_config = DPOConfig(
      output_dir="./dpo_output",
      num_train_epochs=2,
      per_device_train_batch_size=2,
      gradient_accumulation_steps=8,
      learning_rate=5e-5,
      beta=0.1,  # DPO 的 KL 惩罚系数
  )
  
  trainer = DPOTrainer(
      model=sft_model,         # 从 SFT 模型继续训练
      args=dpo_config,
      train_dataset=dpo_dataset,
      peft_config=lora_config,
  )
  trainer.train()
  ```

**Day 25（5h）：**

- [ ] 5h：微调前后对比评测
  - Prompt-only baseline vs. SFT model vs. SFT+DPO model
  - 指标：意图分类准确率、工具调用决策准确率、技法多样性
  - 在测试集（留 20% 数据不训练）上跑

#### Day 26-28（20h）：收尾 + 简历打磨

**Day 26（6h）：**

- [ ] 4h：整理所有实验数据，填上简历中所有 XX% 占位符
  - 关键约束保留率
  - 中间段技法调用率偏差改善幅度
  - VLM 检出率提升幅度
  - SFT+DPO 工具调用准确率提升幅度
  - 跨场景（Web Design vs. 医疗）的对比指标
- [ ] 2h：画数据可视化图表（技法位置分布图、规则遵循率对比图等）

**Day 27（6h）：**

- [ ] 3h：写项目 README，整理 GitHub 仓库
- [ ] 3h：准备面试话术——对每个模块准备 3 个"可能被追问的问题"和回答：
  - RAG：为什么选 bge-large-zh？chunk_size 怎么定的？Reranker 带来多少提升？
  - LangGraph：为什么用 LangGraph 不用纯代码编排？状态机设计的取舍？
  - VLM：VLM 评分跟人工评分的一致性怎么样？hallucination 怎么处理？
  - DPO：数据量这么少效果靠谱吗？为什么不直接用 few-shot prompting？
  - 通用性：除了 Web Design 和医疗，还能用在什么场景？

**Day 28（8h）：**

- [ ] 3h：更新简历，填入所有数据
- [ ] 3h：全流程回归测试——从头到尾跑一遍 pipeline，确保可复现
- [ ] 2h：最终 review，push 到 GitHub

**第四周交付物：**

- ✅ SFT + DPO 微调完成，三组对比评测数据
- ✅ 简历所有 XX% 替换为实际数字
- ✅ GitHub 仓库整理完毕（含 README、实验数据、可视化）
- ✅ 面试话术准备完毕

---

## 六、关键风险与应对

| 风险                                   | 概率 | 影响 | 应对方案                                                     |
| -------------------------------------- | ---- | ---- | ------------------------------------------------------------ |
| RAG 检索质量差，top-5 里没有目标 chunk | 中   | 高   | 先用结构化标签切分（最适合你的 SOP），而非通用语义切分；加 Reranker；调大 top-k 到 15-20 再 rerank 到 5 |
| LLM 不按预期调用 Function Call         | 中   | 中   | 在 system prompt 里写清楚工具使用的 few-shot 示例；用 tool_choice="required" 强制调用 |
| VLM 评分不稳定 / 与人工判断差异大      | 中   | 中   | 对同一截图跑 3 次取平均；prompt 里给评分标准的具体示例；只把 VLM 作为"辅助通道"，不完全替代规则检查 |
| SFT/DPO 数据量不够导致过拟合           | 中   | 中   | 用 LoRA 降低参数量；epoch 不要超过 3；留 20% 测试集监控过拟合；如果效果不好就加 data augmentation |
| DPO 效果不如 few-shot prompting        | 低   | 高   | 如果真的出现这种情况，简历上改写为"对比了 SFT+DPO 与 few-shot prompting 两种策略，分析了小数据场景下微调的效果边界"——诚实地展示负面结果反而加分 |
| 通义千问 API 限流 / 额度用完           | 低   | 中   | 提前注册多个账号；备选 DeepSeek API（更便宜）；批量任务错峰跑 |
| 第一周超时导致后面连锁延误             | 中   | 高   | 第一周目标是"跑通"不是"做好"——哪怕检索质量一般也先往下走，第二周可以回头迭代 |

---

## 七、面试高频追问准备清单

### RAG 相关

1. **为什么选 bge-large-zh 而不是其他 embedding 模型？**
   → 在 MTEB 中文基准上排名靠前，1024维，支持 instruction-aware encoding，适合检索场景。可以提一嘴你对比过 m3e-base（效果略差）和 text-embedding-v3（API调用有延迟）。

2. **chunk_size 怎么选的？为什么不用更大/更小的？**
   → 你的 SOP 里技法条目平均长度约 300-500 字符，用结构化标签按条目切分最合理。固定窗口切分会把一个技法切成两半，语义完整性差。可以展示三种策略的 recall 对比数据。

3. **Reranker 带来多少提升？值得加吗？**
   → 展示加 Reranker 前后的 top-5 precision 对比。Cross-Encoder 慢但准，trade-off 是每次多 0.x 秒延迟换取 X% 的 precision 提升，在你的场景里每次只 rerank 15-20 条所以延迟可接受。

### LangGraph 相关

4. **为什么用 LangGraph 不用纯 Python 代码编排？**
   → 状态管理和条件路由写起来更清晰；内置 checkpoint 机制方便回溯调试；子图机制支持后续扩展（比如加新的子流程）；面试官如果追问"是不是杀鸡用牛刀"，就说实际跑起来确实只有 4-5 个节点，但 LangGraph 的价值在于状态可观测性和重试机制。

### VLM 相关

5. **VLM 评分跟人工评分一致吗？**
   → 准备 20 张截图的人工评分 vs. VLM 评分的 Pearson/Spearman 相关系数。如果一致性不高，就诚实说"VLM 在XX类缺陷上检出率高但在YY类上不如人工"。

### DPO 相关

6. **几百条数据做 DPO，效果可信吗？**
   → 你的任务很窄（意图分类 + 工具选择，不是开放式生成），action space 有限，几百条 LoRA 微调是够的。展示 train/test split 的对比数据，说明没有严重过拟合。如果面试官继续追问，就说"小数据场景下 DPO 的效果确实有天花板，我在实验中也对比了 few-shot prompting 作为 baseline"。

### 通用性相关

7. **这个框架除了 Web Design 和医疗还能用在哪？**
   → 任何有超长 SOP 的 Agent 场景：法律合规审查（法规库 + 流程规则）、金融风控（风控规则库 + 审批流程）、客服知识库（产品FAQ + 话术规范）、代码 Agent（文档 + API reference）。核心是"SOP 文档按语义切分 + 意图路由 + 按需注入"这套方法论的迁移。

---

## 八、项目完成后简历中需要填入的具体数字清单

| 简历占位符                             | 来源                | 怎么测                                                       |
| -------------------------------------- | ------------------- | ------------------------------------------------------------ |
| 中间段技法调用率较头尾段低 XX%         | 第1周 baseline 实验 | 跑 30 条 brief，统计 T-20~T-50 vs T-01~T-20 / T-51~T-80 的调用频次 |
| 关键约束保留率 XX%                     | 第2周评测           | 人工标注 30 条 query 的 ground truth chunks，计算 recall@5   |
| 中间段调用率偏差从 XX% 降至 XX%        | 第2周评测           | 动态路由后重新统计三段调用率分布                             |
| CSS 渲染缺陷检出率从 XX% 提升至 XX%    | 第3周 VLM 实验      | 人工标注 30 个页面的视觉缺陷 ground truth，对比 text-only vs. text+VLM 的检出率 |
| 工具调用决策准确率较 baseline 提升 XX% | 第4周微调评测       | 测试集上 Prompt-only vs. SFT+DPO 的工具选择准确率            |
| 技法多样性指标提升 XX%                 | 第4周微调评测       | 测试集上生成结果的技法种类数对比                             |

---

## 九、当前实现后的优先级修订（2026-04-10）

> 这一节用于覆盖“理想路线图”和“当前真实系统状态”之间的差距，防止后续开发重新回到过早扩张的路线。

### 9.1 当前已完成的骨架

- 已具备 profile-driven 主链路：`classify -> retrieve -> build_prompt -> generate -> quality_check`
- 已具备基础 RAG：embedding 检索 + reranker 精排
- 已具备 LLM 压缩阶段：将长上下文压成 execution spec
- 已具备 web profile 的基础 validator 与 retry 闭环
- 已验证 `web_design` profile 可以在当前框架下生成通过校验的 HTML 样本

### 9.2 当前最关键的缺口

- chunking 仍偏 web 文档定制，尚未泛化到通用长 SOP / PDF / policy / checklist / YAML / JSON 等文档形态
- compression 仍主要依赖 prompt 约束，缺少结构化 schema、source traceability 和保真度可观测性
- evaluation 仍偏 web validator，缺少统一 benchmark harness、指标和实验记录入口
- profile 抽象已出现，但还没有形成完整的 ingestion / chunking / retrieval / compression / validator 配置规范

### 9.3 接下来真正的优先级顺序

1. 先把 compression 做成结构化 schema，而不是只依赖自由文本压缩。
2. 把 chunking 升级成通用分层策略：structured splitter + token-aware splitter + overlap + parent-child chunk。
3. 建立统一 evaluation 入口，记录 query、命中 chunk、压缩前后 token、validator 结果、失败类型。
4. 将 profile schema 产品化，明确每个 profile 的 ingestion / retrieval / compression / validation 配置边界。
5. 在以上四项稳定之后，再引入 memory layer、VLM 扩展和第二领域迁移验证。
6. SFT / DPO 放在更后阶段，只有在 benchmark 和压缩保真度稳定后才推进。

### 9.4 当前阶段的策略原则

- 先证明“单次任务内的知识保真和可验证执行”。
- 不要过早把主线切到 memory-first 或 fine-tuning-first。
- `web_design` 仍是第一标准 profile，但框架设计必须始终保持 domain-agnostic。
- 新增能力必须优先服务于“通用 agent 骨架”，而不是继续把系统做成 web 特化工程。

---

## 十、外部调研后的技术路线收敛（2026-04-10）

> 这一节用于回答“候选方案很多，到底选哪条主线”。结论不是把所有新论文都接进来，而是先选择最适配当前仓库、最容易验证收益、最能保持通用性的组合。

### 10.1 当前明确采用的主线

1. `通用文档接入 + 分层 chunking`
2. `parent-child retrieval + dense/BM25/hybrid retrieval + rerank`
3. `schema-first、source-grounded compression`
4. `统一 eval / tracing / benchmark harness`

这四层优先级高于 memory、VLM 扩展、第二领域迁移和 SFT/DPO。

### 10.2 Chunking：选“结构优先 + token 兜底”，不选纯固定窗口

- 首选方案：`structured splitter + token-aware fallback + overlap`
- 原因：最适合从当前 Markdown 文档逐步泛化到 PDF / DOCX / HTML / policy / checklist / JSON / YAML。
- 结构切块保留标题层级、列表、表格、代码块和 section path；超长块再按 token 上限二次切分。
- 每个 chunk 必须保存结构元信息：`doc_id`、`heading_path`、`chunk_level`、`source_type`、`priority`。
- 不建议继续只靠 `split_by_h2` 或固定窗口，因为它们都无法稳定保住“小规则埋在长段后半段”的细节。

推荐参考：
- Docling: https://docs.langchain.com/oss/python/integrations/providers/docling
- LangChain Retrieval: https://docs.langchain.com/oss/python/langchain/retrieval

### 10.3 Retrieval：选“小块召回，大块回填”，不再停留在单层 dense 检索

- 首选方案：`child retrieval -> parent expansion`
- child chunk 负责召回精度，parent chunk 负责回填上下文，避免召回时只命中局部句子、生成时丢失附近硬约束。
- 在当前 dense retrieval 基础上，补一条 `BM25 / exact-match` 检索支路，再做 merge + rerank。
- 这一步特别适合 SOP、编号规则、阈值、命名约定、字段名等对词面敏感的内容。
- reranker 继续保留，但不再让它单独承担“挽救粗 chunk”的职责。

推荐参考：
- ParentDocumentRetriever: https://api.python.langchain.com/en/latest/langchain/retrievers/langchain.retrievers.parent_document_retriever.ParentDocumentRetriever.html
- LlamaIndex Recursive Retriever / Small-to-Big: https://developers.llamaindex.ai/python/framework-api-reference/packs/recursive_retriever/
- Anthropic Contextual Retrieval: https://www.anthropic.com/research/contextual-retrieval

### 10.4 Compression：选“结构化规格编译”，不再只靠自由文本总结

- 首选方案：`schema-first structured outputs + source-grounded evidence extraction`
- `build_prompt` 的输出必须固定成 schema，而不是自由文本。
- 最低要求字段：
  - `task_summary`
  - `hard_constraints`
  - `optional_guidance`
  - `interaction_requirements`
  - `forbidden_items`
  - `acceptance_checks`
  - `repair_requirements`
  - `source_refs`
  - `unresolved_items`
- 每条 `hard_constraint` 都要能回溯到 `chunk_id / source_doc / evidence_span`。
- 如果检索证据不足，不要强行写进硬约束；应进入 `unresolved_items` 或直接 abstain。
- 推荐把当前 `retrieve -> build_prompt` 拆成：
  - `retrieve`
  - `extract_evidence_atoms`
  - `compile_execution_spec`
  - `generate`
  - `check`

推荐参考：
- OpenAI Structured Outputs: https://platform.openai.com/docs/guides/structured-outputs
- EXIT: https://aclanthology.org/2025.findings-acl.253/
- Attribute First, then Generate: https://arxiv.org/abs/2403.17104
- Attribute or Abstain: https://aclanthology.org/2024.emnlp-main.463/
- RECOMP: https://openreview.net/forum?id=mlJLVigNHp

### 10.5 Evaluation：先把“能不能稳定变好”测清楚，再谈更多模块

- 新增统一实验入口，至少记录：
  - `query`
  - `profile`
  - `retrieved_chunks`
  - `compression_input_tokens`
  - `compression_output_tokens`
  - `compression_retention_ratio`
  - `validator_issues`
  - `failure_type`
  - `retry_count`
- benchmark 不要求一开始就很大，但必须可重复、可比较。
- memory 相关 benchmark 可以参考 LongMemEval 的任务设计思路，但当前阶段先聚焦“单任务内的长规则保真”。

推荐参考：
- LongMemEval: https://arxiv.org/abs/2410.10813
- LangGraph Overview: https://docs.langchain.com/oss/python/langgraph/overview
- LangChain Context Engineering: https://docs.langchain.com/oss/python/langchain/context-engineering
- OpenAI Agent Evals: https://platform.openai.com/docs/guides/agent-evals
- OpenAI Trace Grading: https://platform.openai.com/docs/guides/trace-grading
- Phoenix: https://github.com/Arize-ai/phoenix
- Letta Evals: https://github.com/letta-ai/letta-evals

### 10.6 暂缓项

- `memory layer`：有价值，但属于跨任务经验层，不是当前主链瓶颈。
- `VLM`：等 rule-based eval 稳定后再接入。
- `第二领域 profile`：等通用 ingestion / retrieval / compression / eval 主链稳定后再迁移。
- `SFT / DPO`：等 benchmark 和压缩保真度稳定后再推进，避免把噪声模式学进去。

### 10.7 一句话结论

当前项目下一阶段的正确目标不是“继续堆网页技巧”，也不是“马上做长期 memory”，而是：

**把现有的 markdown-RAG + freeform compression，升级成通用 ingestion + parent-child / hybrid retrieval + source-grounded structured compression + benchmarked validation。**

### 10.8 Memory 与外部 Benchmark 的落位

- `LongMemEval` 应作为外部公共 benchmark 接入，但它是评测集，不是 memory 方案本身。
- 不建议只看 `LongMemEval`；至少要和一类“记忆用于执行”的 benchmark 配套使用，例如 `Mem2ActBench` 或 `AMA-Bench`。
- 当前最该先做的是本地 `benchmark harness + trace schema`，而不是先接重型 memory 平台。
- memory 在本项目中的正确位置是“增强层”：
  - 在 `quality_check` 后写入 episodic / procedural memory
  - 在下一次 `retrieve` 前检索相似失败、相似修复和历史成功 spec
- memory 首先存“经验”，而不是存“聊天偏好”：
  - 哪类 query 常漏哪类硬约束
  - 哪类 validator issue 用什么修复 prompt 最有效
  - 哪类 execution spec 过去最稳定
- 如果要先做轻量 memory，优先考虑与现有 LangGraph 栈兼容的方案，如 `LangGraph Store / LangMem`；`Mem0 graph memory`、`Letta shared memory` 等更适合第二阶段。
- 对 `mempal` 这类仓库，当前定位应是候选增强模块，而不是主链替代。只有在源码和数据结构被完整审查后，才考虑接入实验层。

推荐参考：
- LongMemEval: https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf
- MemBench: https://arxiv.org/abs/2506.21605
- Mem2ActBench: https://arxiv.org/abs/2601.19935
- AMA-Bench: https://arxiv.org/abs/2602.22769
- LangChain Long-term Memory: https://docs.langchain.com/oss/python/langchain/long-term-memory
- LangMem: https://langchain-ai.github.io/langmem/
- Mem0 Graph Memory: https://mem0.mintlify.app/open-source/features/graph-memory
- Letta Memory Blocks: https://docs.letta.com/guides/core-concepts/memory/memory-blocks
