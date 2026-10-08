# 提示词工程 × RAG 课堂实验台

面向 8–10 分钟课堂汇报的离线教学 Demo：四轮提示词、评分公式、逐项核对、简化 RAG。

## 直接运行

下载项目后双击 `index.html`。无需安装、注册或 API Key，不上传输入文本。
也可以在项目目录运行 `python -m http.server 8000` 后打开 http://localhost:8000 。

## 界面与操作

1. `scoring.html`：论文评分公式与课堂核对表。修改离散评分，查看频率与加权均值。
2. `rounds.html`：上方切换四轮；左侧要求、中间样例、右侧核对结果。点击运行后汇总分数；下方可修改人工判断。
3. `rag.html`：输入查询→检索证据→组装增强提示词→查看匹配的生成记录。改为无关查询时没有证据，不生成提示词。

## 关键源码

- `core.js`：实际被界面调用的关键词检索和十项评分函数。
- `rounds.js`：样例、操作状态与评分显示。
- `scoring.js`：G-Eval 加权计算的构造数据演示及人工核对记录。
- `rag.js`：知识库、增强提示词组装和生成记录回放。
- `knowledge-base.json`：知识库副本，供阅读与测试；浏览器使用 rag.js 内嵌数据以支持直接双击打开。

## 测试

安装 Node.js 后运行 `node core.test.cjs`。浏览器端无需 Node.js。

## 材料与限制

四轮文本是教学样例；20、40、80、100 分是人工核对记录加总，不是平台重复实验或模型自动质量评分。十项百分制是课堂自定清单，不是 G-Eval 论文原量表。

RAG 使用四条人工核验的中文摘要片段、关键词匹配 Top-3，不是完整论文解析、向量检索或原始 RAG 模型复现。查询和提示词组装真实执行；生成记录由 AI 在对话中依据证据撰写，按钮只回放。没有在线 LLM 服务。RAG 不保证事实正确，仍需人工核验来源与引用支持。

## 文献

- Liu et al. (2023), G-Eval. https://aclanthology.org/2023.emnlp-main.153/
- McMahan et al. (2017), Communication-Efficient Learning of Deep Networks from Decentralized Data. https://proceedings.mlr.press/v54/mcmahan17a.html
- Lewis et al. (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. https://arxiv.org/abs/2005.11401

## 许可

原创程序代码采用 MIT 许可；第三方论文、引文与相关材料不因本仓库许可改变其原有权利。项目不附带论文全文。

## 开源地址

https://github.com/RH-coder-version/prompt-engineering-rag-demo

## Windows 风格界面

采用 Windows Fluent 风格的侧栏、工具栏、明显的文本输入框和蓝色焦点状态。提示词与待评文本均可编辑；修改待评文本会清空旧勾选和分数，必须重新人工核验。支持恢复本轮样例、保留各轮临时草稿、导出 JSON。浏览器刷新会重置草稿。

`windows.css` 为共用样式；`legacy-windows.css` 统一评分与RAG页。设计参考：https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/text-box
