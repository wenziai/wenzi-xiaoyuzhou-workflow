# 账号定位初始化

账号定位必须由账号本人定义并确认。可以帮助用户整理表达，但不能替用户决定身份、受众、立场或内容方向。没有确认定位时，停止播客处理流程。

## 首次使用：五个最小问题

用一组简短问题收集以下信息；用户可以自由回答，不要求使用 YAML：

1. **你是谁？** 哪些身份、经历或专业背景可以公开使用？
2. **你主要写给谁？** 他们正在面对什么问题？
3. **你长期想写什么？** 请列出 3–7 个内容板块，例如创业、AI、健康、亲子或消费。
4. **你希望别人因为什么记住你？** 分别说明想展示的能力，以及希望长期表达的观点或判断标准。
5. **哪些内容不能替你编造或公开？** 包括私人经历、商业信息、付费内容和禁用表达。

如果用户已经提供过其中一部分，只询问真正缺失且会改变结果的项目。不要重复询问。

## 确认步骤

根据回答先整理一份“定位摘要预览”，至少包含：一句话定位、目标受众、内容板块、能力信号、观点资产、可信度来源、表达特点和内容边界。清楚标记待补充项。

定位摘要必须由用户明确确认。用户修改后，更新预览并再次确认有变化的内容。不得把沉默视为同意，也不得在确认前继续转录、选题或创作。

## 核心字段

```yaml
profile_name: 账号或人物名称
identity: 身份与可信度来源
one_line_positioning: 一句话定位
target_audience: 主要受众
audience_problems: 受众正在面对的问题
content_pillars: 长期内容支柱
capabilities_to_show: 希望内容持续展示的能力
viewpoints_to_express: 希望长期积累的观点与判断标准
proof_assets: 支撑能力与观点的经历、案例、结果和现场
core_beliefs: 稳定立场与判断标准
unique_experience: 可公开使用的经历、案例和资源
voice:
  tone: 语气
  rhythm: 句子与段落节奏
  preferred_words: 常用表达
  avoid_words: 禁用词与陈词滥调
boundaries:
  private_topics: 不公开的生活或业务信息
  paid_content: 不免费完整披露的方法
  uncertain_claims: 必须本人确认的内容
goals: 建立信任、增长、讨论、转化或记录
call_to_action: 允许使用的互动或转化方式
platforms: 各平台账号的独立设置
```

## 平台字段

每个平台可覆盖通用定位：

```yaml
platforms:
  x:
    account_role:
    audience:
    preferred_formats: [短帖, 长帖, thread]
    length_preference:
    posting_goal:
  xiaohongshu:
    account_role:
    audience:
    preferred_formats: [图文, 清单, 经验复盘]
    visual_style:
    posting_goal:
  weibo:
    account_role:
    audience:
    preferred_formats: [短微博, 长微博, 热点评论]
    posting_goal:
  moments:
    relationship_context: 熟人、客户、同行或混合
    privacy_level:
    preferred_formats: [短感想, 生活观察, 工作复盘]
    posting_goal:
```

## 最小可用定位

没有完整档案时，以下五项足够开始：

1. 我是谁；
2. 我主要写给谁；
3. 我长期关注什么；
4. 我希望读者记住我的哪些能力和观点；
5. 哪些经历或说法不能替我编造。

如果这五项缺失，停在定位初始化阶段。不要生成平台中性的内容母稿，因为它会绕过个性化目标。

## 来源优先级

1. 用户本次明确说明；
2. 用户明确提供的账号定位文件；
3. 当前对话中已经确认的信息；
4. 用户认可的既有内容样本；
5. 推断，仅用于可随时修改的表达偏好，不用于身份、经历、数据或商业事实。

## 私有档案

用户明确同意保存时，建议写入：

```text
~/.codex/user-profiles/wenzi-xiaoyuzhou-content/<profile-name>.md
```

使用 [空白定位模板](profile-template.md)。私有档案不属于公开 Skill，不随 Skill 分享、打包或上传。
