---
name: wenzi-xiaoyuzhou-transcribe
description: >
  播客/小宇宙 → 下载 → 转录 → 存为 Markdown 的完整工作流。
  支持 RSS 批量下载、单集链接转录。
metadata:
  category: "media"
  triggers: "[\"用户发送小宇宙/播客链接\", \"帮我转录这个播客\", \"下载播客\", \"批量转录播客\"]"
  version: "1.3.0"
  tags: "[\"media\", \"audio\", \"podcast\", \"transcription\", \"xiaoyuzhou\"]"
---

# 播客转录 Skill

将播客音频下载并转录为 Markdown。支持小宇宙、喜马拉雅、直接音频地址、本地音频和 RSS 批量流程。用户提供单集链接后，默认直接交付一份简体、无时间戳、分段清晰、适合阅读的完整文字稿。

## 默认用户体验

单集链接任务默认端到端完成，不把下载、提取音频、模型运行、去时间戳、纠错、繁简转换和排版拆成多个需要用户确认的步骤。除非遇到阻塞、需要付费或需要向第三方上传音频，否则后台连续完成。

最终回复只呈现：

- 已完成；
- 最终可读版 Markdown 文件的可点击路径；
- 确有必要时，用一句话提示仍可能存在需回听核验的专名或数字。

不要默认展示命令、模型参数、音频大小、分段数量、处理耗时、中间文件、核验稿路径或逐步修改过程。用户主动询问过程、诊断或原始时间戳时再提供。

默认在本地使用 `faster-whisper` 的快速档，先得到可检索、可选题的完整逐字稿。Atlas Cloud、MuAPI 是用户明确选择后才启用的 **experimental** 云端后端；音频会发送至第三方服务并可能计费，本版本尚未完成真实付费服务验收。

## 环境要求

以下命令在本 skill 目录运行，建议使用 Python 3.11 或更新版本：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install faster-whisper
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

本地模型首次使用时需要下载。仅使用云端后端不需要 `faster-whisper`；Atlas 容器转换仍可能需要 `ffmpeg`。云端密钥通过安全环境配置，不能写入命令参数、转录稿或版本库。

## 单集与批量

```bash
python3 scripts/transcribe.py "https://www.xiaoyuzhoufm.com/episode/xxxxx" ./output \
  --provider local --preset fast
python3 scripts/transcribe.py "/你的音频目录/episode.mp3" ./output \
  --provider local --preset balanced --language zh
python3 scripts/batch_transcribe.py --rss-url "替换为实际 RSS 地址" \
  --output ./output --count 10 --provider local
```

将示例地址替换为实际来源。单集页面会尝试提取音频链接，提取失败时改用直接音频地址或本地文件。标准输出最后一行是成功生成的 Markdown 路径。

## 本地速度档位

| 档位 | 默认模型 | 用途 |
|---|---|---|
| `fast` | `base`，单束解码 | 默认。尽快获得完整逐字稿，用于检索、摘要和选题 |
| `balanced` | `small` | 选题确定后，需要更稳的正文理解或少量引用 |
| `accurate` | `small`，更完整解码 | 重点段落复核；仍不能代替对原音频的事实核验 |

`--model` 可以覆盖档位的默认模型，但仍保留该档位的解码策略。除非用户明确需要更高精度，不要一开始就用高成本档位把整期做满。逐字稿完成后先交付或报告路径；内容分析和社媒创作由后续 Skill 分阶段处理。

自动下载仅接受公网 HTTP(S) 直连地址，禁用代理和重定向，拒绝本地/私网地址。需要跳转或代理的来源，请先自行下载音频，再传入本地文件路径。

## 单集交付：核验稿与可读稿

单集转录在内部区分两种产物，避免阅读体验和来源核验互相冲突；对用户默认只展示可读稿：

1. **核验稿（内部）**：保留转录后端、时间戳、原始分段和来源，用于回听、引用核验及后续选题定位。它是后台工作产物，不在默认回复中展示。
2. **可读稿（最终交付）**：面向用户阅读和存档。默认从核验稿整理，不覆盖唯一一份原始稿。

可读稿遵循以下规则：

- 保留完整口述内容，不改写成摘要，不因重复或口语化而擅自删减；
- 删除逐段时间标注、模型名称、耗时等转录技术信息；
- 根据实际内容变化添加少量主题标题，并把碎片化语音合并为长度适中的自然段；
- 中文统一转换为简体；可使用 `scripts/to_simplified.py` 做确定性转换；
- 直接修正语境明确的同音词、专名和常见识别错误，不默认使用“原词（建议：新词）”的大量行内标记；
- 无法可靠判断的内容保持原样，或集中放入简短的“待核验”清单，不凭空补写原话；
- 文件顶部只保留标题、播客或创作者名称、主播和来源链接，以及必要的核验提示；
- 交付前检查内容顺序与覆盖范围，确保所有原始语音片段仍在可读稿中有所对应。

用户指定保存目录时，把可读稿保存到该目录。文件名默认使用：

```text
节目标题（去掉纯集数前缀）｜播客或创作者名称.md
```

例如原始标题为 `40. 有方法地成长`、播客名为 `有序生活`，文件名使用 `有方法地成长｜有序生活.md`。如果用户明确要求保留集数或使用其他命名，以用户要求为准。

完成基础工具阶段时，只交付可读稿路径和必要的简短质量提示，然后停止。不要自动进入选题或社媒创作。

## 可选云端转录

| 后端 | 凭据环境变量 | 默认模型 |
|---|---|---|
| `local` | 无 | `base`（`fast` 档） |
| `atlas` | `ATLAS_API_KEY`，兼容 `ATLAS_CLOUD_API_KEY` | `bytedance/seed-asr-2.0` |
| `muapi` | `MUAPI_API_KEY`，兼容 `MU_API_KEY` | `openai-whisper` |

配置所选服务凭据后：

```bash
python3 scripts/transcribe.py "/你的音频目录/episode.mp3" ./output \
  --provider atlas --cloud-timeout 1800 \
  --state-dir "$HOME/.local/state/chubbyskills/podcast"
python3 scripts/transcribe.py "/你的音频目录/episode.mp3" ./output \
  --provider muapi --cloud-timeout 1800 \
  --state-dir "$HOME/.local/state/chubbyskills/podcast"
```

`--provider` 优先于 `PODCAST_TRANSCRIBE_PROVIDER`，都未指定时使用 `local`。批量入口支持同样的 provider、模型、语言、等待和状态目录参数，并把最终选项显式传给单集进程。

MuAPI 音频必须小于 25 MiB，超限在上传前拒绝。Atlas 对不支持的容器先在本机转换为 MP3，再提交音频。

## 云端任务恢复

默认状态目录为 `~/.local/state/chubbyskills/podcast`；设置了 `XDG_STATE_HOME` 时使用其中的 `chubbyskills/podcast`。还可用 `CHUBBY_PODCAST_STATE_DIR` 或 `--state-dir` 指定。目录包含任务与转录内容，应按音频内容的隐私要求保存。

相同音频、provider、模型、语言和服务地址再次运行时，已有任务继续查询；已完成结果可以重新导出。提交结果不明确或服务端报告失败时，不自动重新提交。普通网络重试保留状态目录并重跑原命令即可。

`--resubmit` 明确创建新任务，可能重复计费。不要用它解决单纯的轮询超时。删除状态目录或改变输入配置也可能失去复用条件。客户端超时不等于服务端取消，也不代表没有计费。

完整仓库使用说明、统一入库和验证范围见[云端转录说明](https://github.com/chubbyguan/chubbyskills/blob/main/docs/cloud-transcription.md)。

## 产物与限制

核验稿为带 frontmatter、来源和转录后端标记的 Markdown。后端返回可用分段时保留时间戳；没有时间信息时不编造时间轴。单集的用户交付稿按上面的“可读稿”规则另行整理。

- 本地 CPU 推理耗时受音频长度、模型和机器配置影响。
- `fast` 档用于选题级逐字稿，可能比 `balanced` 更容易出现专名、同音词和断句错误。
- 转录可能有专有名词、数字或断句错误，引用前核对原始音频。
- 云端真实可用性、账号权限、音频兼容性和费用尚需独立验收。
- 本 skill 不提供通用说话人分离保证。

## 贡献与参考

可选云端转录需求分别来自 [binyangzhu000-sudo 的 PR #3](https://github.com/chubbyguan/chubbyskills/pull/3) 和 [Anil-matcha 的 PR #5](https://github.com/chubbyguan/chubbyskills/pull/5)。本项目基于共同接口重新实现，保留贡献归属。

- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [OpenAI Whisper](https://github.com/openai/whisper)

## 合规声明

请遵守来源平台条款并尊重内容版权，控制请求频率。云端处理前确认自己有权向所选服务提交音频；下载和转录不会改变原内容的版权归属。
