# Group Lecture Builder｜AI 讲义制作 Skill

[English](README.md) · [安装细节](docs/installation.md) · [素材清单](MATERIALS.md) · [示例说明](examples/README.md)

把考纲和真实题目交给 AI，按统一模板制作**学生版讲义**与**答案版讲义**。本项目提供讲义工作流、LaTeX 模板、构建脚本和检查规范；AI 负责读取素材、规划章节、编写内容并调用工具生成 PDF。

> **适合谁？** 希望让 AI 辅助制作国际课程专题讲义的教师。当前主要按**物理及其他理科讲义**设计并测试；其他学科可以试用，但其题型、讲解方式和审核标准尚未系统适配，**不要将物理规则原样套用到所有学科**。

**讲义默认怎么呈现？** 正文少堆文字，用有助理解的图、表或流程突出关键关系，把核心定义和公式单独框出。答案版默认在解析后附可读的官方评分细则原图（须有对应原件及使用权限）；自编题标注作者评分要点，没有官方原件就不声称已核对。学生版不显示这些答案内容。

已建好的课包通常有自己的 `_模板/` 副本。更新 Skill 不会自动改写旧 PDF；只有准备使用新命令时，才同步该课包的模板（保留自定义改动），再重编两版。

## 先看这里：3 步开始使用

| 步骤 | 你需要做什么 | AI 负责什么 |
|---|---|---|
| **1. 安装** | 把下方安装提示词复制给支持本地操作的 AI | 获取仓库、注册为全局 Skill、检查环境并运行示例 |
| **2. 提供素材** | 准备对应考纲与有授权的真题 | 确认考纲版本、题目来源与缺失资料 |
| **3. 开始制作** | 说明学科、考局、主题与课时 | 规划章节、制作双版本 PDF、提交检查记录供教师审核 |

**无需先学习 Git 或终端。** 但你使用的 AI 必须能够读写本地文件、执行命令。仅能聊天或浏览网页的 AI，无法保证替你安装 Skill 或在电脑上编译 PDF。

## 1. 一段话，让 AI 协助安装（推荐）

将下面整段复制到 **Codex、Claude Code 等具备本地文件和终端执行能力的 AI 助手**中：

```text
请帮我安装一个用于制作课程讲义的 AI Skill。

GitHub 仓库：https://github.com/Bright-han0516/group-lecture-skill

我不熟悉终端操作，请在你具有权限的范围内尽量直接完成安装，不要只返回一串命令。

要求：
1. 先阅读仓库的 README.zh-CN.md、SKILL.md、docs/installation.md 和 install.sh，确认实际支持的安装方式。
2. 检查我的操作系统、当前 AI 工具、文件读写和终端执行权限。如果当前环境不支持，请明确说明限制，不要声称已安装。
3. 如果兼容，请把 Skill 安装到当前工具的用户级 Skill 目录，确保它能在不同项目、新对话中被发现。若已有安装，请先检查并说明如何安全更新；不要覆盖或删除现有文件。
4. 检查 Git、Python、PyMuPDF、XeLaTeX 等依赖。小范围只读检查可以直接进行；涉及系统软件安装、管理员权限、大型下载、覆盖文件或修改系统配置时，请先征得我的同意。
5. 安装后运行 bootstrap.sh，报告环境检测、Demo 的学生版和答案版 PDF 构建、结构 QA 的真实输出。区分“Skill 注册成功”和“PDF 构建环境就绪”。
6. 在新的项目目录或新会话中验证能否调用 group-lecture-builder；若不能验证，注明尚未验证。
7. 最后告诉我安装状态、仍需处理的问题，以及如何用自然语言制作第一份讲义。

不要自行编造测试结果，也不要把示例构建通过当成正式讲义的学科质量已通过。
```

**安装成功应看到什么？** AI 能在新项目中找到 `group-lecture-builder`；运行 `bootstrap.sh` 时如果环境完备，会显示 `READY`，并生成 Demo 的两份 PDF。前者说明 Skill 被注册，后者说明当前机器可以运行示例构建，**都不代表真实讲义已经通过学科审核**。

### 我的 AI 能直接安装吗？

| 使用环境 | 推荐方式 |
|---|---|
| **Codex / Claude Code**（可执行本地命令的桌面或 CLI 环境） | 使用上面的对话提示词，优先安装到全局 Skill 目录 |
| Cursor、Kimi Code 或其他编程 Agent | 先让 AI 检查自身的 Skill 发现机制与终端权限；不能直接照搬 Codex/Claude 的安装目录 |
| 普通 ChatGPT / 豆包 / Kimi 等聊天窗口 | 可帮忙分析素材、规划章节或审核草稿；如果没有本地命令权限，就不能直接完成本地安装与 PDF 构建 |

这里说的是**工具能力**而非模型名称。某款产品是否支持，最终以实际运行和验证结果为准。

## 2. 安装后，制作第一份讲义

先把这些信息告诉 AI；**不用一次填写所有字段，缺什么由 AI 追问**：

| 项目 | 说明 | 必要性 |
|---|---|---|
| 学科、考局、考纲版本 | 例如物理、CIE 9702、对应考试年度及版本 | 必需 |
| 主题与范围 | 例如 Motion、指定考点或 section | 必需 |
| **考纲** | PDF 文件或 AI 能读取的本地文件路径 | **必需** |
| **真实题目** | 有权使用的真题文件及允许的年份、试卷范围 | **必需** |
| 级别、课时与输出要求 | 如 AS/A2、SL/HL、4 课时、题量和篇幅 | 需说明或确认 |
| **教材** | PDF、版次及相关章节；有助于补充例子和图示 | 推荐 |
| **官方评分标准（MS）** | 与题目对应的 Mark Scheme；用于核实给分点 | 推荐 |
| 课程输出文件夹 | 存放生成的源文件、PDF 和审核记录 | 可由 AI 协助确定 |

> **底线：没有考纲或真实题目，不进入正式生产。** 不能虚构考题年份、卷号、题号或评分标准。没有教材仍可制作；没有 MS 时可独立求解，但要标注“未经官方 MS 核实”并交教师核查。具体见 [MATERIALS.md](MATERIALS.md)。

安装后可以直接这样告诉 AI：

```text
请调用 group-lecture-builder，制作一份 CIE 9702 AS 的 Motion 专题讲义。
我会提供对应版本的考纲和允许使用的真题，教材及 MS 如有也会提供。
先核对素材并给出章节规划，再制作学生版与答案版 PDF。
请提供考纲覆盖、题目来源及答案核验记录；不要编造真题来源。
```

想尝试数学、化学、生物等其他学科时，可以要求 AI **先检查该学科题型是否适合当前模板**，明确哪些物理专用规范需要调整；首次试用建议选一个较小主题，并由任课教师重点审阅。

## 3. 最后会得到什么？

当前工作流的主要交付物：

- **学生版 PDF**：英文知识讲解、填空、例题和练习（当前模板默认英文正文）。
- **答案版 PDF**：与学生版基于同一份 LaTeX 源文件生成，包含答案和中文解析。
- **源文件与素材目录**：可修改的 `.tex` 文件、图片及构建脚本。
- **检查记录**：PDF 技术检查结果、考纲覆盖、真题来源及学科审核记录（`qa/academic_review.md`）。

AI 可以辅助核查公式、计算、来源和题目答案；**学科审核仍需要老师最终确认**。视觉表现、教学安排、解释是否充分、是否适合当前学生，也由教师决定。

## 4. 更习惯自己操作？手动安装

下面命令适用于 **macOS、Linux 或 Windows WSL**，其中 `git` 需要已安装。它把仓库下载到固定位置，并分别注册到 Codex 与 Claude Code 的**用户级 Skill 目录**：

```bash
git clone https://github.com/Bright-han0516/group-lecture-skill.git "$HOME/.local/share/group-lecture-builder" && bash "$HOME/.local/share/group-lecture-builder/install.sh" --hosts all
```

然后验证 PDF 构建环境：

```bash
cd "$HOME/.local/share/group-lecture-builder"
./bootstrap.sh
```

- **注册成功 ≠ 环境准备完成**：`install.sh` 不会自动安装完整 TeX Live；`bootstrap.sh` 用于检查依赖、构建 Demo 和进行结构 QA。
- 安装目录已经存在时，`git clone` 会失败；**不要直接删除原目录**。请按 [更新说明](docs/installation.md#update-an-existing-installation)检查并更新。
- 安装器不会覆盖其他同名 Skill；全局 Skill 目录的具体规则以当前客户端为准。
- Windows 原生 PowerShell 不是目前验证过的构建路径；建议在 WSL 内运行。
- 若想先确认 Demo 构建能力，再开始制作真实讲义，务必先看到 `READY`。

完整安装说明：[docs/installation.md](docs/installation.md)。

## 5. 常见问题

| 遇到的问题 | 建议检查 |
|---|---|
| AI 说打不开 GitHub | 确认网络访问及工具的网页/仓库读取权限；仓库现已公开 |
| AI 只能给命令，无法替我安装 | 当前对话可能没有本地终端或文件操作权限；切换到具备这些权限的编程 Agent |
| 安装后在新项目里找不到 Skill | 核对用户级 Skill 目录、链接是否有效；重启或新建 AI 会话，验证是否支持自动发现 |
| 安装时提示目标文件夹已存在 | 不要覆盖；先使用已有仓库更新流程，或让 AI 检查现有安装 |
| `xelatex` / TeX 包缺失 | 需要安装适合系统的 TeX Live 组件；大型系统安装应先征得同意 |
| `No module named 'fitz'` | 检查当前 Python 是否安装 PyMuPDF，按 `bootstrap.sh` 的提示修复 |
| 中文解析显示方框 | 检查 Songti SC / Fandol 等中文字体 |
| Demo 通过，但正式讲义内容有错 | Demo 只验证环境和模板；根据 `academic_review.md` 核实考纲、题目来源、计算与答案 |

更详细的宿主和运行限制参见 [docs/installation.md](docs/installation.md) 与 [references/known-pitfalls.md](references/known-pitfalls.md)。

## 6. 给维护者：工作流程与文件入口

```text
SKILL.md                    AI 使用的技能入口
install.sh                  用户级 Skill 注册（Codex / Claude Code）
bootstrap.sh                环境检查 + Demo 构建 + 结构 QA
MATERIALS.md                学科素材清单与开工门槛
scripts/                    创建主题、编译、检查
template/                   LaTeX 模板、字体与中性素材
examples/demo/              可运行示例（非真实考题）
references/boards.md        考局命名与来源规范
references/pipeline.md      章节、正文、练习与整合流程
references/academic-qa.md   学科内容审核证据要求
docs/installation.md        安装、验证与更新细节
```

更多技术细节参见 [SKILL.md](SKILL.md)、[references/](references/)；自动测试见 [GitHub Actions](https://github.com/Bright-han0516/group-lecture-skill/actions)。

目前通过自动化验证的，是配置好的 Linux 环境中的示例构建及相关脚本测试；**各操作系统、各 AI 客户端及其他学科的完整端到端效果仍需实际验证**。

## 7. 版权、隐私和许可

- **只将公开适用的代码、原创示例与中性素材放在本仓库**。真题、教材截图、官方 MS、学校 Logo、学生作业和个人资料不要提交到公共 GitHub 仓库。
- 使用教材、真题和图片应符合相应版权或机构许可；制作完成的 PDF 也不应未经许可公开传播。
- 本项目不代表 CIE、IB、AQA、Edexcel、AP 或任何出版社的官方产品。
- 代码和文档采用 [MIT License](LICENSE)；打包字体保留其自身许可，详情见 [NOTICE](NOTICE)。PyMuPDF 为 AGPL/商业双许可，重新分发集成环境时需另行核对授权。

---

**使用入口：复制 [第 1 节的安装提示词](#1-一段话让-ai-协助安装推荐) 给具备本地执行能力的 AI → 准备考纲与真题 → 开始制作。**
