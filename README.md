# AI 时代阅读助手(社会趋势 + 人类学习观察站)

每天自动生成两篇材料,发到本仓库的 GitHub Issue 里。每篇材料以**一条最近真实发生的新闻/研究/政策/产品动作**为切入点,深度拆解它的证据、方法、数据和结论,经典理论只在真正有解释力时作为"透镜"引入,不是每天必须讲的主线。

- **社会趋势**(`social-trends.yml`):AI时代社会/经济结构变化相关的新闻深度拆解 + (如适用)理论透镜 + 当下有分歧的真实观点 + 对你个人决策的启发
- **AI时代人类学习观察站**(`education-philosophy.yml`):一个长期运行的 Research Agent / Intellectual Observatory。它不是教育新闻 Agent,也不是论文摘要 Agent;每天的新闻只是观察窗口,真正要持续回答的是: **AI时代,人类应该学习什么?教育应该培养什么样的人?AI在其中承担什么角色?**

教育/学习观察站的搜索范围已经扩大到教育、AI、认知科学、心理学、学习科学、劳动经济学、社会学、政治经济学、政府政策、高等教育、Future of Work、AI产品、机器人、HCI 等。OpenAI 发布 Agent、WEF 发布 Future of Jobs、Anthropic 的 alignment 研究、新的 AI Literacy 政策、新的学习科学论文,都可能成为合格的每日切入点,只要它能帮助理解"人未来应该学习什么"。

系统维护的不只是日报:

- `state/education-philosophy-seen.md`:已深度讲过的事件,用于去重。
- `state/education-philosophy-signals.md`:长期趋势层,记录哪些 Signal 正在增强、减弱或制度化。
- `state/questions.md`:长期问题库,维护开放问题、矛盾证据、反例、定义变化和研究缺口。
- `state/social-trends-seen.md`:社会趋势方向已深度讲过的事件。

长期下来,教育/学习观察站希望积累的不是 365 篇孤立日报,而是几十个越来越成熟的问题、一组持续校准的趋势信号,以及一套不断演化的个人教育哲学。

## 一、准备工作

1. **建一个新的 GitHub 仓库**(私有的就行,内容是你自己的阅读材料,没必要公开),把这个文件夹里的所有文件(保留目录结构)推上去,包括:
   ```
   .github/workflows/social-trends.yml
   .github/workflows/education-philosophy.yml
   state/social-trends-seen.md
   state/education-philosophy-seen.md
   state/education-philosophy-signals.md
   state/questions.md
   README.md
   ```

2. **安装 Claude Code GitHub App**:去 [https://github.com/apps/claude](https://github.com/apps/claude) 点 Install/Configure,授权范围选 "Only select repositories",勾选你刚建的这个仓库。这一步是走 GitHub 的 OAuth 授权确认,必须在浏览器里手动点,没装的话 workflow 会在 "Run Claude Code" 这一步直接报错 `Claude Code is not installed on this repository`。

3. **生成 Claude Code 的订阅授权 token**(用你的 Claude Pro 账号,不额外计费,走非交互式月度额度):
   在你本地电脑装好 [Claude Code](https://code.claude.com) 后,终端运行:
   ```
   claude setup-token
   ```
   会打开浏览器走一遍 OAuth 登录确认,完成后终端会打印一个长字符串 token,**只显示一次,记得复制**。

4. **把 token 存成仓库 Secret**:
   仓库页面 → Settings → Secrets and variables → Actions → New repository secret
   - Name: `CLAUDE_CODE_OAUTH_TOKEN`
   - Value: 粘贴上一步拿到的 token

5. **给 Actions 开权限**(让它能创建 Issue、提交代码):
   仓库页面 → Settings → Actions → General → 拉到 "Workflow permissions" → 选择 **Read and write permissions** → Save。
   （两个 workflow 文件里已经声明了 `contents: write` 和 `issues: write`,但仓库总开关也要打开,否则会被拦下来。）

6. **(可选)配置 Google Calendar 自动同步**:每天生成的 Issue 会额外同步成一条全天日历事件。如果不需要这个功能,跳过这一步即可——脚本检测不到对应 Secret 会自动跳过,不影响 Issue 正常生成。下面按你英文界面上实际会看到的按钮名字写。

   **A. 在 Google Cloud Console 建服务账号**(全程在 [console.cloud.google.com](https://console.cloud.google.com/))

   1. 顶部有个项目选择器(项目名 + 下拉箭头),没有项目的话先点它 → **New Project** 建一个,名字随便起。
   2. 顶部搜索框(放大镜图标)输入 `Google Calendar API` → 点搜索结果里的 "Google Calendar API" → 进详情页后点蓝色的 **Enable** 按钮。**这一步很容易漏——光搜到详情页不算数,必须真的点了 Enable 且按钮变成 "Manage"。** 如果后面同步失败报 `Google Calendar API has not been used in project ... or it is disabled`,就是这一步没做或者做在了别的项目上;确认方法:左上角三条杠菜单 → **APIs & Services → Enabled APIs & services**,列表里应该能看到 "Google Calendar API"。
   3. 左上角三条杠菜单(≡)→ **IAM & Admin → Service Accounts**。
   4. 页面顶部点 **+ CREATE SERVICE ACCOUNT**。
   5. 第1步(Service account details)随便填个名字,比如 `ai-reading-calendar` → 点 **CREATE AND CONTINUE**。
   6. 第2步(Grant this service account access to project)不用选任何角色,直接点 **CONTINUE**。
   7. 第3步(Grant users access)也不用填,直接点 **DONE**。
   8. 回到 Service Accounts 列表,点你刚建的这个账号(邮箱形如 `xxx@你的项目ID.iam.gserviceaccount.com`)→ **把这个邮箱地址复制下来,后面要用**。
   9. 进入账号详情页后,点顶部的 **KEYS** 标签页 → **ADD KEY → Create new key** → 弹窗里选 **JSON** → 点 **CREATE**。浏览器会自动下载一个 `.json` 文件,存好待用(这个文件只会在这一次下载,关掉弹窗就拿不回来了,如果没存到就得重新生成一次密钥)。

   **B. 在 Google Calendar 把日历共享给这个服务账号**(在 [calendar.google.com](https://calendar.google.com/))

   1. 页面左侧 "My calendars" 列表里,鼠标悬停在你想同步的那个日历上(用默认主日历的话就是你自己的名字那一项)→ 出现三个点(⋮)→ 点它 → **Settings and sharing**。
      (也可以走:右上角齿轮图标 → **Settings** → 左侧 "Settings for my calendars" 列表里点同一个日历名字,效果一样。)
   2. 进入该日历的设置页后往下滚,找到 **"Share with specific people or groups"** 这个区块 → 点 **+ Add people and groups**。
   3. 输入框里粘贴上面复制的服务账号邮箱地址。
   4. 右侧权限下拉框(默认是 "See only free/busy") → 改选 **"Make changes to events"**(这一步很关键,选低了会导致创建事件时报权限错误)。
   5. 点 **Send**。服务账号没有真实邮箱收信,这一步不会真的发邮件出去,只是用来触发授权,正常。

   **C. 拿到 Calendar ID,存成 GitHub Secret**

   1. 还在同一个日历设置页面,继续往下滚,找到 **"Integrate calendar"** 区块,里面的 **"Calendar ID"** 那一行就是你需要的值——点它旁边的复制图标就行。如果同步的是默认主日历,这个 ID 通常就是你的 Gmail 地址本身;如果是新建的次级日历,会是类似 `xxxxxxxx@group.calendar.google.com` 的一串字符。
   2. 回到 GitHub 仓库页面 → **Settings → Secrets and variables → Actions → New repository secret**,新增两个:
      - `GOOGLE_SERVICE_ACCOUNT_KEY`:用文本编辑器(不要用 Word 这类会自动加格式的软件)打开 A.9 下载的 `.json` 文件,把**完整内容**(包括最外层的花括号 `{ }`)全部粘进 Value 框
      - `GOOGLE_CALENDAR_ID`:粘贴 C.1 拿到的 Calendar ID
   3. 两个 Secret 都存好后,下次 workflow 跑的时候日历事件就会自动创建。想立刻验证的话,去仓库 Actions 页手动 Run workflow 一次,跑完去 Google Calendar 上看有没有多一条今天的全天事件。

   6. 完成后,每天的 Issue 都会额外在这个日历上生成一条全天事件,标题和 Issue 一致,描述里带 Issue 链接。如果配好了还是没同步成功,去对应 workflow 运行日志里搜 "日历事件创建失败",错误信息里通常会写清楚是权限不对还是 ID 不对。

## 二、检查/调整时间

工作流里的 `cron` 是 **UTC 时间**,已经按你在柏林(欧洲中部时间)的假设换算好了:

- 社会趋势:`cron: "9 5 * * *"` → 柏林夏令时(CEST, UTC+2)早上 7:09
- 教育哲学:`cron: "41 5 * * *"` → 柏林夏令时(CEST, UTC+2)早上 7:41

分钟数特意没设成整点或整5分钟——[GitHub 官方文档](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule)写明 "The schedule event can be delayed during periods of high loads of GitHub Actions workflow runs. High load times include the start of every hour",并建议 "schedule your workflow to run at a different time of the hour" 来避开排队。错开几分钟能大幅降低被明显延迟的概率,但 GitHub 不保证 schedule 触发绝对准时,极端情况下还是可能晚个几分钟到十几分钟,这是平台本身的限制,配置上无法完全消除。

柏林每年 3 月最后一个周日到 10 月最后一个周日用夏令时(CEST, UTC+2),其余时间是冬令时(CET, UTC+1)。GitHub Actions 的 cron 本身不会跟着夏令时切换,所以每年 10 月底切回冬令时后,实际触发时间会变成柏林时间早上 8:09 / 8:41;如果介意这 1 小时偏差,到时候把两处 `cron` 分别改成 `"9 6 * * *"` 和 `"41 6 * * *"`,等次年 3 月底切回夏令时再改回 `5`。

如果你不在柏林,换算方式是:`UTC小时 = 你想要的本地时间 - 你的UTC偏移`。改完记得保存后重新推送。

> 注意:GitHub Actions 的 schedule 触发**不保证分秒不差**,官方说明高峰期可能延迟几分钟到十几分钟,属于正常现象。

## 三、先手动跑一次测试

不用等到明天早上,现在就可以测:仓库页面 → Actions → 左侧选 "社会趋势阅读 - 每日生成" 或 "教育哲学阅读 - 每日生成" → 右边 "Run workflow" 按钮 → 点击运行。

等个一两分钟,去仓库的 Issues 页面看有没有新生成的 Issue。如果失败了,点进那次运行看日志,常见问题:
- Token 没配对 → 检查 Secret 名字是不是完全等于 `CLAUDE_CODE_OAUTH_TOKEN`
- 权限不够,`gh issue create` 报 403 → 回去检查第四步的 Workflow permissions 有没有设成 Read and write
- push 失败 → 确认仓库没有开分支保护规则挡住 Actions 直接 push 到默认分支
- 日历事件没出现 → 这一步失败不会让整个任务失败,去运行日志里找 "日历事件创建失败" 或 "跳过日历同步" 的输出;常见原因是 Secret 没配对,或者共享日历时给服务账号的权限选错了(要选"对活动进行更改",不是"查看")

## 四、平时怎么看

- 每天材料会变成一条新的 Issue,标题类似 `社会趋势 · 2026-07-20 · OECD最新报告:AI暴露度最高行业招聘不降反升` 或 `学习观察站 · 2026-07-20 · 英国推进中小学AI Literacy课程`。
- 建议在仓库页面右上角点 **Watch → All Activity**,这样每次新 Issue 会推邮件通知,配合 GitHub 手机 App 也能收到手机推送,人不在电脑边也能看到。
- 如果配置了 Google Calendar 同步,同一天还会在你指定的日历上多一条全天事件,点进去能看到 Issue 链接。
- `state/*.md` 文件是给 Claude 自己看的长期记忆。`*-seen.md` 用于避免重复讲同一事件;`education-philosophy-signals.md` 和 `questions.md` 用于维护长期趋势与开放问题。你一般不用管;如果想让某条新闻被重新深挖一次,手动删掉对应 seen 文件里的那一行就行。

## 五、以后想加什么

这套东西是你自己的仓库,想改随时能改,比如:

- 想要更长的历史存档:Issue 本身就是永久记录,搜索关键词就能翻出以前讲过的新闻/事件。
- 想调整讨论深度、切入角度:直接改对应 `prompt:` 字段里的文字描述就行,不需要动其他部分。
- 想调整长期研究方向:编辑 `state/questions.md` 里的核心问题,或在 `state/education-philosophy-signals.md` 里增加/合并 Signal。
