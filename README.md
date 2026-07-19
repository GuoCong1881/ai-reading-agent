# AI 时代阅读助手(社会趋势 + 教育哲学)

每天自动生成两篇材料,发到本仓库的 GitHub Issue 里:

- **社会趋势**(`social-trends.yml`):经典社会/经济理论 + AI时代是否依然成立 + 当下有分歧的真实专家观点 + 对你个人决策的启发
- **教育哲学**(`education-philosophy.yml`):经典教育理论 + AI时代下是否需要修正 + 当下有分歧的真实专家观点 + 如果你要教书意味着什么

两个方向各自维护一份"已讲过理论"清单(`state/` 目录),自动去重,不会重复讲同一个理论。

## 一、准备工作

1. **建一个新的 GitHub 仓库**(私有的就行,内容是你自己的阅读材料,没必要公开),把这个文件夹里的所有文件(保留目录结构)推上去,包括:
   ```
   .github/workflows/social-trends.yml
   .github/workflows/education-philosophy.yml
   state/social-trends-seen.md
   state/education-philosophy-seen.md
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

6. **(可选)配置 Google Calendar 自动同步**:每天生成的 Issue 会额外同步成一条全天日历事件。如果不需要这个功能,跳过这一步即可——脚本检测不到对应 Secret 会自动跳过,不影响 Issue 正常生成。
   1. 去 [Google Cloud Console](https://console.cloud.google.com/) 建一个新项目(或用现有的),启用 **Google Calendar API**。
   2. 左侧菜单 IAM 与管理 → 服务账号 → 创建服务账号 → 创建完成后进入该账号 → "密钥" 标签页 → 添加密钥 → JSON,下载生成的 JSON 文件。
   3. 打开你自己的 Google Calendar 网页版 → 设置 → 左侧选中要同步的日历 → "与特定人员共享" → 把服务账号的邮箱(JSON 文件里的 `client_email` 字段,形如 `xxx@xxx.iam.gserviceaccount.com`)添加进去,权限选 **"对活动进行更改"**。
   4. 在同一个日历的设置页面里找到 "Calendar ID"(个人主日历通常就是你的 Gmail 地址;如果是新建的次级日历,会是类似 `xxxx@group.calendar.google.com` 的字符串)。
   5. 仓库 → Settings → Secrets and variables → Actions,新增两个 Secret:
      - `GOOGLE_SERVICE_ACCOUNT_KEY`:粘贴整个 JSON 文件的内容
      - `GOOGLE_CALENDAR_ID`:粘贴上一步拿到的 Calendar ID
   6. 完成后,每天的 Issue 都会额外在这个日历上生成一条全天事件,标题和 Issue 一致,描述里带 Issue 链接。

## 二、检查/调整时间

工作流里的 `cron` 是 **UTC 时间**,已经按你在柏林(欧洲中部时间)的假设换算好了:

- 社会趋势:`cron: "0 5 * * *"` → 柏林夏令时(CEST, UTC+2)早上 7:00
- 教育哲学:`cron: "20 5 * * *"` → 柏林夏令时(CEST, UTC+2)早上 7:20

柏林每年 3 月最后一个周日到 10 月最后一个周日用夏令时(CEST, UTC+2),其余时间是冬令时(CET, UTC+1)。GitHub Actions 的 cron 本身不会跟着夏令时切换,所以每年 10 月底切回冬令时后,实际触发时间会变成柏林时间早上 8:00 / 8:20;如果介意这 1 小时偏差,到时候把两处 `cron` 分别改成 `"0 6 * * *"` 和 `"20 6 * * *"`,等次年 3 月底切回夏令时再改回 `5`。

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

- 每天材料会变成一条新的 Issue,标题类似 `社会趋势 · 2026-07-20 · 熊彼特创造性破坏`。
- 建议在仓库页面右上角点 **Watch → All Activity**,这样每次新 Issue 会推邮件通知,配合 GitHub 手机 App 也能收到手机推送,人不在电脑边也能看到。
- 如果配置了 Google Calendar 同步,同一天还会在你指定的日历上多一条全天事件,点进去能看到 Issue 链接。
- 两个 `state/*.md` 文件是给 Claude 自己看的"已读记录",你一般不用管;如果想让某个理论被重新讲一次,手动删掉那一行就行。

## 五、以后想加什么

这套东西是你自己的仓库,想改随时能改,比如:

- 想要更长的历史存档:Issue 本身就是永久记录,搜索关键词就能翻出以前讲过的理论。
- 想换个每天两条为一条,或者调整讨论深度、字数:直接改对应 `prompt:` 字段里的文字描述就行,不需要动其他部分。
