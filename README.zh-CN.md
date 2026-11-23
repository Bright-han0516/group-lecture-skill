# 集团版讲义 Skill（中文说明）

把「一个考局的一个主题」做成两本 PDF：**学生版**（留空、练习）和**答案版**（答案 +
中文解析）。视觉版式固定在 LaTeX 模板里，AI 只负责填内容，不负责“设计”。

这个仓库是可直接分发的版本：模板、字体、`rsfs`、占位素材、QA 脚本和一个能跑的
demo 都在里面；构建时不联网。

## 一条命令开始

在终端执行（需要已登录 `gh`，并且账号有私有仓库权限）：

```bash
mkdir -p ~/.dsh/skills && gh repo clone Bright-han0516/group-lecture-skill \
  ~/.dsh/skills/group-lecture-builder && \
  cd ~/.dsh/skills/group-lecture-builder && ./bootstrap.sh
```

`bootstrap.sh` 会自动做三件事：

1. 检查 XeLaTeX、宏包、字体、`rsfs`、PyMuPDF；
2. 构建 `examples/demo` 的学生版和答案版；
3. 跑结构 QA（空白页、缺图、路径泄漏、字体嵌入、学生版中文字符）。

全部通过会打印 `READY`，并提醒你准备哪些素材；失败会停在第一个错误，不会假装通过。

### 让 AI 自己执行

把下面这段直接发给 Codex / Kimi Code / Claude Code / DSH 这类能跑命令的 agent：

```text
请在终端执行下面这一条命令，然后把最后 30 行输出贴给我：

mkdir -p ~/.dsh/skills && gh repo clone Bright-han0516/group-lecture-skill \
  ~/.dsh/skills/group-lecture-builder && \
  cd ~/.dsh/skills/group-lecture-builder && ./bootstrap.sh

如果 bootstrap 失败，停下来，把 FAIL 行和 fix 建议贴给我，不要继续写讲义。
成功后读 SKILL.md，并按 MATERIALS.md 向我要素材。
```

如果 `~/.dsh/skills` 不是你的宿主使用的目录，把路径换成该宿主的 skills 目录；
Codex 也可以 clone 到 `~/group-lecture-skill`，不一定要装成 skill。

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

> 私有仓库：Codex / Kimi Code 需要 GitHub 登录态或被加为 collaborator；
> WorkBuddy / 豆包办公通常拿不到私有仓库，请给它 v0.1.1 Release 里的源码 ZIP，
> 或让它只做评审。

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
- [v0.1.1 Release](https://github.com/Bright-han0516/group-lecture-skill/releases/tag/v0.1.1)
