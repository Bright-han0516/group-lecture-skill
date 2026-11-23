# 集团版讲义 Skill（中文说明）

把「一个考局的一个主题」做成两本 PDF：**学生版**（留空、练习）和**答案版**（答案 +
中文解析）。视觉版式固定在 LaTeX 模板里，AI 只负责填内容，不负责“设计”。

这个仓库是可直接分发的版本：模板、字体、`rsfs`、占位素材、QA 脚本和一个能跑的
demo 都在里面；构建时不联网。

## 不会用终端？直接把下面的话发给 AI

如果你使用的是能访问本地文件、执行命令的 AI 编程助手（例如 Codex 或 Claude Code），可以直接复制这段话，无需自己输入安装命令：

```text
请帮我安装一个用于制作多学科课程讲义的 AI Skill。

GitHub 仓库：
https://github.com/Bright-han0516/group-lecture-skill

请按以下步骤操作：
1. 访问仓库并阅读 README.zh-CN.md、SKILL.md 和 docs/installation.md。不要只凭仓库名称推断功能。
2. 检查当前操作系统、AI 工具及其权限，确认能否访问本地文件、执行命令和安装用户级 Skill。
3. 如果兼容，按官方说明将 Skill 注册到当前 AI 工具的用户级 Skill 目录，使它在其他项目和新对话中也能被调用；不得擅自覆盖已有 Skill。
4. 检查 Git、Python、PyMuPDF、XeLaTeX 和相关依赖。缺少依赖时说明如何修复；涉及管理员权限、大型软件下载或覆盖文件，先征得我的同意。
5. 运行仓库的 bootstrap.sh、Demo PDF 构建和 QA。真实报告执行结果；不要把“注册成功”当作“PDF 环境验证通过”。
6. 重新启动或打开新的 AI 会话，测试能否在其他项目识别 group-lecture-builder，并告诉我如何调用。
7. 如果当前工具没有本地执行能力，请说明限制，改为提供可行的安装方案，不要声称已安装成功。

请尽量替我完成可以安全执行的安装操作。我不熟悉终端，希望你优先自动操作，而不是仅返回命令。
```

**注意：** 该 Skill 当前以国际课程、理科类讲义工作流为主要设计和测试场景，其他学科可以尝试，但尚未经过系统验证。学科内容、练习形式和评分标准必须根据用户提供的对应考纲和真实题目调整，不能机械套用物理公式、计算题或 IB 的考试规范。最低素材仍为考纲与有授权的真题；教材与官方评分标准可提高质量。

纯聊天型 AI 如果无法运行本地命令，可以帮助阅读、审稿和设计内容，但不能保证安装或编译 PDF。

## 一条命令安装成全局 Skill（Codex / Claude Code）

macOS / Linux / Windows WSL 可运行（也可以让具备本地执行能力的 AI 代为运行）：

```bash
git clone https://github.com/Bright-han0516/group-lecture-skill.git "$HOME/.local/share/group-lecture-builder" && bash "$HOME/.local/share/group-lecture-builder/install.sh" --hosts all
```

注册后在任意项目的新 AI 会话中说明“使用 group-lecture-builder 制作讲义”。安装器不会静默安装大型 TeX 发行版；安装后执行 `cd "$HOME/.local/share/group-lecture-builder" && ./bootstrap.sh` 检查 PDF 构建环境。参见 [详细安装说明](docs/installation.md)。

## 旧版环境验证

旧版方式：使用 GitHub CLI（`gh`）克隆后验证运行环境；不负责全局 Skill 注册。

```bash
gh repo clone Bright-han0516/group-lecture-skill ~/group-lecture-skill && \
  cd ~/group-lecture-skill && ./bootstrap.sh
```

这只是“先跑通”。如果要装成 skill，把 clone 目标换成宿主扫描的目录：

| 宿主 | clone 目标 | 入口文件 |
|---|---|---|
| DSH | `~/.dsh/skills/group-lecture-builder` | `SKILL.md` |
| Claude Code | `~/.claude/skills/group-lecture-builder` | `SKILL.md` |
| Codex / Cursor / Kimi Code | 任意目录，例如 `~/group-lecture-skill` | `AGENTS.md` / `CLAUDE.md` |
| WorkBuddy / 豆包办公 | 不 clone，用 ZIP 或粘贴 `PROMPT.md` | `PROMPT.md` |

目录名只对会扫描 skills 目录的宿主重要：`group-lecture-builder` 要和 `SKILL.md` 的
`name` 一致。Codex 这类 coding agent 不要求目录名，它读仓库根的 `AGENTS.md`。

`bootstrap.sh` 会自动做三件事：

1. 检查 XeLaTeX、宏包、字体、`rsfs`、PyMuPDF；
2. 构建 `examples/demo` 的学生版和答案版；
3. 跑结构 QA（空白页、缺图、路径泄漏、字体嵌入、学生版中文字符）。

全部通过会打印 `READY`，并提醒你准备哪些素材；失败会停在第一个错误，不会假装通过。

### 让 AI 自己执行

把下面这段直接发给 Codex / Kimi Code / Claude Code / DSH 这类能跑命令的 agent：

```text
请在终端执行下面这一条命令，然后把最后 30 行输出贴给我：

gh repo clone Bright-han0516/group-lecture-skill ~/group-lecture-skill && \
  cd ~/group-lecture-skill && ./bootstrap.sh

如果 bootstrap 失败，停下来，把 FAIL 行和 fix 建议贴给我，不要继续写讲义。
成功后读 SKILL.md，并按 MATERIALS.md 向我要素材。
```

如果宿主会扫描 skills 目录，把 `~/group-lecture-skill` 换成上表中的对应路径即可。

## 不是所有 agent 都能“出片”

关键不是模型品牌，而是两条能力：**能不能拿到仓库文件**、**能不能执行 shell + XeLaTeX**。

| Agent | 读仓库 | 跑构建 | 建议 |
|---|---|---|---|
| Codex | ✅ 读 `AGENTS.md` | ✅ 有 shell；Windows 用 WSL | 全流程 |
| Kimi Code | ⚠️ 看它读哪个入口 | ✅ 如果是 CLI/IDE 形态 | 先跑 `bootstrap.sh` 验证 |
| Claude Code / DSH | ✅ `SKILL.md` + `AGENTS.md` | ✅ | 装成 skill，全流程 |
| WorkBuddy | ⚠️ 通常只能读粘贴/文件 | ❌ 一般没有本地 TeX | 评审、改文字 |
| 豆包办公 | ⚠️ 文档型 | ❌ 基本不能编译 | 评审、润色、列缺口 |
| 纯聊天 AI | ✅ 能读网页 | ❌ | 只能审稿 |

判断方法只有一条：让它跑 `./bootstrap.sh`。三条全过 → 能生产；第一条就挂 → 缺
TeX；连命令都跑不了 → 只能评审。详见 [docs/hosts.md](docs/hosts.md)。

> 仓库目前公开，可直接访问；但能阅读 GitHub 页面并不等于能访问本地文件或运行 XeLaTeX。无法本地执行的 AI 只能参与内容规划与审稿。

## 开始前要准备的素材

**先读 [MATERIALS.md](MATERIALS.md)。** 最少要给 AI 这些：

1. 考局 + 主题代码 + 英文标题；
2. 级别（SL / HL / SL+HL）和课时；
3. 考纲文件路径 + 对应 section；
4. 教材 PDF 路径 + 版次 +「PDF 页 = 印刷页 + 偏移」；
5. 允许使用的真题文件夹 + 年份/场次/卷别范围；
6. 官方 MS（mark scheme）文件夹；
7. 课程根目录（放 `_模板/` 和 `<Code>_<Name>/` 的绝对路径）；
8. 输出要求：章节数、页数目标、是否含 HL、题量、中文解析要求。

缺考纲或真题时，agent 必须停下来要材料，不能编年份、卷号、题号。`bootstrap.sh`
结束时会自动打印这份清单。

## 做一个主题

```bash
python3 scripts/scaffold_topic.py --root "/你的课程根目录" \
  A.3 Energy "Work, energy and power"

cd "/你的课程根目录/A3_Energy/src"
./build.sh
python3 ../../_模板/check_topic.py ..
```

产出：

```
dist/IB_A3_Energy_GroupLecture_Student.pdf
dist/IB_A3_Energy_GroupLecture_Key.pdf
```

正文和练习可以由两个 agent 并行写，但**只有 lead 跑 build**；两个 agent 同时构建
会抢 `qa/build/`。具体分工和 prompt 在 [references/pipeline.md](references/pipeline.md)。

## 目录结构

```
SKILL.md                  给 agent 的入口卡
AGENTS.md                 仓库级硬规则（Codex 等会自动读）
README.md / README.zh-CN.md
MATERIALS.md              开始前要提供的素材
PROMPT.md                 复制给 AI 的构建/评审/安装提示词
bootstrap.sh              一条命令做初步调试
docs/hosts.md             各家 agent 的兼容性说明
scripts/                  preflight / scaffold / build / check
template/                 模板、字体、logo、占位图
vendor/texmf/             rsfs（不装 TeX 也能找到）
examples/demo/            能跑的三章 demo
references/               流程、版式、选题、QA、坑
```

## QA 门禁

`check_topic.py` 对每本 PDF 检查：

- `blank_pages = []`：无空白页；
- `path_leaks = []`：无内部路径泄漏；
- `missing_images = 0`：无缺图；
- `not_embedded_fonts = []`：字体全嵌入；
- 学生版 `chinese = 0`：中文只在答案版解析里。

脚本失败会返回 1，可直接接 CI。结构检查不等于“好看”，封面、节末双框、练习块、
答案页仍要人眼看一遍。

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| `Unable to find TFM file "rsfs10"` | 没走 `build.sh`，或 `TEXMFHOME` 不对 | 用 `build.sh`；它会指向 `vendor/texmf` |
| `Font ... not found` | 字体路径不对 | 用 `build.sh`；它传 `\JTFONTDIR` |
| `No module named 'fitz'` | Python 没装 PyMuPDF | `pip install -r requirements.txt`，或换 `/usr/bin/python3` |
| 答案版中文变方框 | 没有中文字体 | macOS 用 Songti SC；TeX Live 装 `fandol` |
| `File '' not found` | `\jtlogo` 传了空路径 | 传 `logo.png`，或删掉该行 |
| Windows 不能跑 `build.sh` | 需要 Bash | 用 WSL 或 Git Bash；原生 PowerShell 未支持 |

## 版权与许可

- 模板是对常见集团讲义风格的独立复刻，**与 CIE / IB / Hodder 无隶属关系**。
- 仓库不含教材图、真题、官方 MS、学校 logo、学生数据。
- 代码和文档 MIT；字体是 GUST 许可；`rsfs` 按原作者要求署名。见 `NOTICE`。
- PyMuPDF 是 AGPL/商业双许可，未打包；分发整套环境前请自行确认许可。

## 相关文件

- [README.md](README.md)（English）
- [docs/hosts.md](docs/hosts.md)（各宿主怎么用）
- [PROMPT.md](PROMPT.md)（复制给 AI 的提示词）
- [MATERIALS.md](MATERIALS.md)（素材清单）
- [v0.2.0 Release](https://github.com/Bright-han0516/group-lecture-skill/releases/tag/v0.2.0)
