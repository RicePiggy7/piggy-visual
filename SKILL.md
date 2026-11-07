---
name: piggy-visual
description: "制作统一墨线排线风格的解释图与透明插画素材，可单独绘制小人「我」、英短蓝白猫「元仔」、两者组合，或同风格的物件与装饰元素。当用户需要概念、机制、流程、对比的完整解释画面，或可复用的排版插图时使用；不用于普通代码图表、照片处理或无关品牌视觉。"
---

# Piggy Visual

Create raster visuals in one shared ink-and-hatching language. Choose one output mode before generating; do not mix the two production paths.

## Choose the output mode

### Mode A — explanatory image

Use when the image must explain a concept, mechanism, workflow, comparison, or tradeoff by itself.

- Deliver a complete PNG or WebP with a finished off-white scene.
- Generate every essential title and label directly inside the bitmap.
- Make the relation visible through objects, paths, states, or repeated materials; labels identify the evidence but do not replace it.
- Do not generate an unlabeled base and add essential words in a separate rendering step.

### Mode B — transparent illustration

Use when a character, object, or decorative illustration will be composed into a hero, document, card, slide, or other layout.

- Request a genuinely transparent PNG when the selected generator supports native alpha. Otherwise use a perfectly uniform chroma-key background that does not occur in the artwork. Default to `#00FF00`; use `#FF00FF` when the subject contains green.
- Do not include explanatory labels unless the user explicitly requests text inside the illustration.
- Preserve native alpha when it is clean. For a chroma-key source, remove the background with the bundled `scripts/cutout.py`. Deliver a transparent PNG in either case.
- Keep the transparent artwork as a reusable visual asset; the surrounding layout supplies the title and explanatory copy.

If the destination is unclear, choose Mode A when the image itself must communicate the idea and Mode B when another layout will carry the explanation.

## Recurring characters

Two optional characters exist. Treat them as optional subjects, not a required pair. Select a character only when requested or when it visibly helps explain the claim; never add one merely to signal the style. When a character is selected, attach its reference image to the generation prompt — the references are canonical for proportions, face, hatching zones, and clothing.

- `assets/references/wo.png` — canonical design of 我.
- `assets/references/yuanzai-sit.png` — 元仔, front sitting pose.
- `assets/references/yuanzai-stand.png` — 元仔, side standing pose.

### 我 — the person

Minimalist line-drawn young man, about 6 heads tall and thin, drawn as clean black outlines of near-uniform weight on white, coloring-book style:

- Round soft face; tiny solid dot eyes; short thick rounded eyebrows; a small L-shaped single-line nose; a faint short horizontal smile.
- Signature details: dense tiny stubble dots sprinkled over jaw and cheeks (never a full beard), and messy short black hair with a few flyaway strands sticking up on the crown, the hair rendered in dense black hatching.
- Large round ears; loose crew-neck T-shirt; loose straight trousers; bare feet, toes as short arcs.
- Calm, slightly blank everyday expression. No glasses, no accessories.

### 元仔 — the pet

Chubby chibi British Shorthair bicolor cat, about 2 heads tall with a low, pear-shaped body:

- Round big head; small triangle ears; solid black inverted-triangle nose; tiny ω mouth; three whiskers per side; four stubby legs with small toe lines; short fat curled tail.
- Signature detail: deadpan half-lidded eyes with a tiny highlight — never fully round, alert eyes.
- Blue-gray zones: crown and forehead with a white blaze running down the muzzle, round cheek patches, a large saddle patch along the back and sides, and the whole tail. White zones: muzzle and chin, chest, belly, all four paws.
- In colored scenes render the blue-gray zones in muted blue-gray (about `#8A94A3`). In pure black-and-white artwork render them as 45° hatching bounded by ink contour lines, exactly as in the references.

## Shared visual language

- Draw confident black ink outlines with varied line weight. Use 45° parallel hatching for gray areas and shadows; never circular halftone dots, never soft gradients.
- Keep the recurring characters secondary to the subject's evidence or action unless the character itself is the requested subject.
- For object-only artwork, carry the same style through clear silhouettes, varied ink line weight, restrained hatching, and simple material details. Do not add a person, cat, or face to make an object feel on-brand.
- Use black, white, and hatching gray as the base. 元仔's muted blue-gray is the signature character color; without the cat it may appear as a small light patch or not at all.
- Add at most two muted semantic colors. Common mapping: blue = input/content, orange = action/warning/cost, purple = process, green = successful result. When a semantic blue is needed, pick a hue clearly brighter than 元仔's gray-blue so character color and semantic color never read as the same thing.
- Avoid 3D, glossy gradients, photorealism, wobbly sketch lines, generic card grids, dashboards, unrelated clutter, and watermarks. Deliberately requested decorative elements are valid subjects.

## Mode A workflow — explanatory image

### 1. Write the visual brief

```text
viewer_question: what should be understood in 10 seconds?
concrete_claim: one-sentence conclusion
real_objects: visible objects, interfaces, documents, tools, or states
relation: comparison, transformation, causality, sequence, hierarchy, feedback, tradeoff, or pipeline
visual_evidence: what must remain understandable when labels are ignored?
scene: believable setting and 2–4 useful environmental cues
semantic_colors: what each accent color means
labels: exact short strings plus the evidence surface for each label
```

Show the input, action or relation, and result. Keep one dominant focal action and no more than three major visual regions. For multiple steps, use a simple left-to-right or top-to-bottom sequence.

### 2. Design the labels

- Prefer 2–6 labels. Use more only when the explanation truly needs them.
- Keep each label short and concrete: role, action, state, or outcome.
- Place every label on or immediately beside its evidence surface, such as a desk nameplate, task sheet, folder tab, machine, meter, lane, or result document.
- Use modern Chinese sans-serif typography, medium or bold, large enough to read at the intended display size.
- Do not turn body copy, commands, tables, or long paragraphs into image text. Use a deterministic layout method when dense or editable text is required.

Add this block to the generation prompt:

```text
Text (verbatim): Render these exact labels as part of the bitmap illustration:
"<label 1>", "<label 2>", "<label 3>".
Use each phrase exactly once. Do not translate, paraphrase, misspell, repeat,
or add any other text. Use modern sans-serif medium/bold typography, large
and readable. Place "<label 1>" on <evidence surface>; place "<label 2>" on
<evidence surface>; place "<label 3>" on <evidence surface>.
```

### 3. Build the prompt

Use this order:

1. State the concrete claim and shared task.
2. Describe the real setting, selected subjects, and any action. Include 我 or 元仔 only when requested or when they visibly help explain the claim; attach the matching reference image when a character appears.
3. Describe the evidence objects and their geometry: aligned, nested, connected, split, transformed, repeated, or converging.
4. Assign semantic colors.
5. Quote the exact labels and specify each placement.
6. Add the Mode A style anchor.
7. End with exclusions.

Mode A style anchor:

```text
Professional editorial ink illustration, minimalist line-art style. Clean
confident black ink outlines with varied line weights, expressive but
controlled. Use 45° parallel hatching for gray and shadow areas — no halftone
dots, no soft gradients. Characters must match the attached reference images.
Render only the selected characters and objects; do not add 我 or 元仔
automatically. Use an off-white lightly textured real environment, not a
blank white canvas. Typography is modern sans-serif, medium or bold, large
and readable. Color is restrained: black, white, hatching gray, the cat's
muted blue-gray when 元仔 is present, plus at most two muted semantic accent
colors. No 3D, no glossy gradients, no photorealism, no generic card grid,
no dashboard, no unrelated clutter, no tiny text, no long paragraphs, no
watermark.
```

### 4. Inspect and retry

1. Inspect the output at original resolution.
2. Compare every label with the brief character by character. Confirm that each appears exactly once and that no stray text was added.
3. Reject missing, duplicated, invented, or misspelled labels. Also check character fidelity against the references: 我 must keep the stubble dots, flyaway hair strands, and bare feet; 元仔 must keep the half-lidded eyes, whiskers, and curled tail.
4. Regenerate with one targeted correction while repeating all scene and style invariants. Do not conceal an error with a separate text layer.

Use this retry instruction:

```text
Keep the scene, composition, characters, objects, colors, and all correct labels unchanged.
Change only the incorrect text "<wrong>" to the exact text "<right>".
Do not add, remove, translate, or repeat any other text.
```

## Mode B workflow — transparent illustration asset

### 1. Select the subject

Identify exactly which subjects are requested: 我 alone, 元仔 alone, both together, or an object or decorative element without characters. When 元仔 alone is requested, pick or let the user pick the pose: front sitting (`yuanzai-sit.png`) or side standing (`yuanzai-stand.png`). Describe one clear action when an action is needed, and include only the props needed to establish it. For a standalone object, describe its shape, material, and distinguishing details instead. Leave generous padding around the artwork so the cutout can be composed safely.

### 2. Build the prompt

Describe the selected subjects first, quoting the character spec details that generators most often miss (stubble dots and flyaway strands for 我; half-lidded eyes and hatching zones for 元仔). State explicitly that no unrequested person, cat, face, or prop should appear. Then append the fixed style anchor and one background rule below.

```text
Style: professional ink illustration, minimalist line-art style. Clean
confident ink outlines with varying line weights, thick for contours and thin
for details, not wobbly or sketchy. Use 45° parallel hatching for gray and
shadow areas — no halftone dots, no soft gradients. Characters must match the
attached reference images. Give characters and objects the same clear
silhouette and ink language. Color usage is extremely restrained: mostly
black, white, and hatching gray; muted blue-gray on 元仔 when present, or as
an optional small light patch when the cat is absent. Use no more than two
muted semantic accent colors. Render only the requested subjects.
Do not let hatching, ink, props, or the subject touch the image border. Keep
generous padding. No text, no watermark. PNG format.
```

Use this background rule when the generator supports genuine transparency:

```text
Render on a genuinely transparent background with a clean alpha channel.
No backdrop, floor plane, cast shadow, or opaque pixels outside the artwork.
```

Otherwise replace `<KEY_COLOR>` with the selected hex color and use this rule:

```text
The background must be a perfectly uniform flat <KEY_COLOR> rectangle with zero
gradient, texture, noise, speckles, shadows, floor plane, or lighting variation.
```

### 3. Validate the source

- Inspect the image before removal.
- For native alpha, confirm the image is RGBA, all four corners have alpha `0`, and no opaque background or edge residue remains. Keep the alpha intact; do not run the cutout script.
- For a chroma-key source, confirm all four corners are uniform and visually match the chosen key color. Reject backgrounds with gradients, texture, shadows, speckles, or artwork touching the border.
- Preserve a chroma-key source alongside the transparent result until the output is approved.

### 4. Remove a chroma-key background only

Skip this step for clean native-alpha output. For a uniform chroma-key source, install Pillow if the active Python environment does not have it, then run:

```bash
python3 scripts/cutout.py source.png transparent.png
```

Optional tuning:

```bash
python3 scripts/cutout.py source.png transparent.png \
  --transparent-threshold 12 \
  --opaque-threshold 220
```

The script samples the image border, builds a soft alpha matte from color distance, and removes color spill from antialiased edges. It works with any uniform key color, so the key can be chosen to avoid the subject palette.

### 5. Validate the transparent result

- Confirm the output is RGBA and all four corners have alpha `0`.
- Confirm every requested subject remains complete. Check the stubble dots, flyaway hair strands, and bare feet for 我; the half-lidded eyes, whiskers, curled tail, and hatching zones for 元仔; narrow contours or small details for an object.
- Check for a gray fringe at 100% zoom.
- Confirm internal white and hatching areas were not erased.
- Regenerate the source instead of forcing the algorithm when the background is visibly uneven.

## Image backend

When the host has no native image generation, generate through the bundled script:

```bash
python3 scripts/generate.py "<full prompt>" -o out.png \
  [--ref assets/references/wo.png] \
  [--size 1024x1024] [--quality medium]
```

- Reads `IMAGE_API_BASE` and `IMAGE_API_KEY` from the environment. The model is unified on `gpt-image-2.6-sunburst`; override per call with `--model` or globally with `PIGGY_IMAGE_MODEL` (the relay also serves `gpt-image-2`, `gpt-image-2.5-flare`, `gpt-image-2.5-sunburst`, `gpt-image-2.6-flare`).
- The script ships requests with curl because the relay's WAF drops Python TLS fingerprints; curl must be on PATH.
- `--ref` attaches reference images through the edits endpoint. Always attach the character references when 我 or 元仔 appears; smoke testing with 元仔 reproduced every signature detail at 9/10 fidelity.
- The relay ignores `background: transparent` and returns opaque images with the background baked in (verified on both `gpt-image-2` and `gpt-image-2.6-sunburst`). Do not request native alpha from this backend. For Mode B use the chroma-key path: put the uniform-key background rule in the prompt (default `#00FF00`; the black-white-blue-gray palette never contains green), then run `scripts/cutout.py` on the result.
- Generation needs outbound access to `IMAGE_API_BASE`. Sandboxed runners block it — request an unsandboxed shell before calling the script.

When the host itself provides image generation, prefer the native tool and keep this script as the fallback.

## Output handling

- Save approved project assets inside the current project or output directory.
- Do not leave project-referenced images only in the generator's default storage.
- Use versioned filenames instead of overwriting an approved asset unless the user explicitly requests replacement.
- Report the final prompt, output mode, final image path, and the transparency path used. Include the reference images, the chroma-key source path, and any non-default cutout options when cutout was needed.

## Quality gate

For every output:

- The subject is recognizable in about 3 seconds.
- When the output explains something, the main action or relation is clear in about 10 seconds.
- Only requested characters appear; when present, they serve the subject rather than becoming generic decoration.
- Characters match their reference images; line work and hatching remain consistent; 元仔's blue-gray and semantic accents follow the selected subjects and meaning.

For Mode A:

- One claim, one focal action, and no more than three major visual regions.
- The visual evidence still shows the relation when labels are ignored.
- Every required label is exact, appears once, and is integrated into the correct evidence surface.
- All labels remain readable at the intended display size.

For Mode B:

- The output has real transparency, whether supplied natively or produced by clean background removal.
- Thin details and internal hatching regions remain intact.
- No source background, fringe, shadow, or border artifact remains.
