# piggy-visual

用同一套墨线排线风格，制作两类可直接使用的图片：一类是带短标签、能独立讲清概念或流程的完整解释图；另一类是可放进演示稿、文章或卡片的透明插画素材。

透明素材可以只画小人「我」、英短蓝白猫「元仔」、两者组合，也可以只画文件夹、工具等物件。角色按画面需要出现，物件不必靠加一个人或一只猫来维持风格。

## 配图风格

- 用粗细分明的黑色墨线画轮廓和细节。
- 用 45° 平行排线表现灰面和阴影，不用半调网点，也不用柔和渐变。
- 小人「我」（六头身瘦削、凌乱黑发呆毛、下巴胡茬点、白T长裤赤脚）和胖胖的英短蓝白猫「元仔」（二头身梨形、死鱼眼半睁、蓝灰披毛）是可选角色，可以单独出现、一起出现，或都不出现。
- 角色登场时附上 `assets/references/` 里的参考图，保证比例、脸和排线分区不走样。
- 物件与装饰元素沿用同一套轮廓、墨线、排线和克制配色，不自动添加角色。
- 完整解释图使用米白色纸张质感，只保留少量真正帮助理解的环境物件；独立插画交付透明背景。
- 元仔出现时使用低饱和蓝灰色；没有元仔时，蓝灰可作为少量点缀，也可以不用。每张图最多再使用两种语义色。
- 图片需要文字时，使用短而准确的无衬线标签，并直接放在对应物体上。

## 示例

用新 skill 生成的示例图之后补充到 `examples/`（解释图 + 透明素材各若干张）。

## 安装

本 skill 安装在 `~/.agents/skills/piggy-visual/`，任何项目可直接点名使用：

```text
Use $piggy-visual to explain how the main Agent assigns work to subagents.
Use short, exact Chinese labels inside the image.
```

```text
Use $piggy-visual to draw 我 reviewing a blueprint,
with 元仔 sitting beside the desk.
```

```text
用 piggy-visual 画一个单独拿着铅笔的「我」，透明背景，不要猫。
用 piggy-visual 画一只单独坐着的「元仔」，透明背景，不要人物。
用 piggy-visual 画一个同风格的文件夹和几张散开的纸，透明背景，不要角色。
用 piggy-visual 画几颗同风格的星芒装饰元素，透明背景，不要角色。
```

完整规则、提示词结构和交付检查都写在 [`SKILL.md`](./SKILL.md) 里。

## License

[MIT](./LICENSE)

本项目基于 [oil-oil/oil-visual](https://github.com/oil-oil/oil-visual)（MIT）改造：保留其双模式架构、提示词模板与交付检查，将角色与视觉语言替换为「我」与「元仔」的墨线排线体系。

## 配置、依赖与使用边界

宿主没有原生生图能力时，用 `scripts/generate.py` 走 OpenAI 兼容接口，读取环境变量 `IMAGE_API_BASE` / `IMAGE_API_KEY`，模型统一为 `gpt-image-2.6-sunburst`（单次可用 `--model`、全局可用 `PIGGY_IMAGE_MODEL` 覆盖；中转站另提供 gpt-image-2 及 2.5/2.6 的 flare、sunburst 等变体）。两条已验证的后端事实：请求必须经 curl 发送（中转站 WAF 会掐断 Python 的 TLS 指纹）；后端不返回原生透明通道——透明素材一律走纯色背景 + `cutout.py` 抠图，该路径需要 Python 和 Pillow。

提示词与参考图会交给所选生图工具。交付前应检查图片中的短标签和透明边缘；密集正文、可编辑图表应使用确定性排版工具。
