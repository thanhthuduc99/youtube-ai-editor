# Thumbnail: <tên video>

Luật, khuôn bố cục và ví dụ đã duyệt: `~/.claude/skills/youtube/references/thumbnail.md`.
Sửa prompt ở đây, rồi chạy `python thumbnail/scripts/build_prompts.py` để ra `prompts/<tên>.txt`.

## Khối dùng chung

Dán khối này vào cuối mọi prompt có mặt người. Phần `[...]` thay theo từng thumbnail.

```
PERSON (identity is the top priority):
- The attached reference photos show the real man. Use them as the only source for his identity. Keep his exact face shape, eyes, eyelids, eyebrows, nose, lips, jawline, ears, skin tone and short black hairstyle. He must be instantly recognizable as the same person.
- His real features, keep them: round face with full cheeks, soft rounded jawline (not angular, not chiseled), youthful boyish look, eyes with low eyelid creases, short black hair with a side-swept fringe over the forehead. Do not make him look like a model or an older man.
- Light professional retouch only: even skin tone, less shine, softer under-eye shadows, tidy hair. Keep real skin texture and pores. No beauty filter, no face slimming, no bigger eyes, no plastic or airbrushed look.
- Expression: [expression].
- Wardrobe: [wardrobe].
- Photo style: real studio portrait, soft key light from front-left, subtle warm rim light on hair and shoulders, 85mm lens, slight film grain. He is cut out cleanly and blended into the background with matching light.

STYLE:
- Premium tech-creator YouTube thumbnail. Maximum 3 elements: the man, the headline, one graphic.
- Headline font: very heavy geometric sans-serif (like Montserrat Black), all caps, tight line spacing, soft dark drop shadow.
- Colors: [palette].
- Real assets: every logo and UI in the image comes from the attached asset images. Show them as real crisp app icons and real screenshots, with their original colors, shapes and layout. Never invent a logo. Never redraw UI as a flat illustration or a 3D cartoon.
- Large and readable at phone size. Keep the bottom-right corner free of text and key graphics.
- Do not add any graphic, card, icon or UI that is not described in LAYOUT.

TEXT RULES:
- The only new text in the image is [exact text]. Spell it exactly, with correct Vietnamese diacritics.
- Text that already exists inside an attached UI screenshot stays as it is. No other text, letters, numbers, logos or watermarks anywhere.
```

Khối cho mẫu không có người (đánh dấu `[khối không người, với:]`):

```
STYLE:
- Premium tech-creator YouTube thumbnail. No people.
- Headline font: very heavy geometric sans-serif (like Montserrat Black), all caps, tight line spacing, soft dark drop shadow.
- Colors: [palette].
- Real assets: every logo and UI in the image comes from the attached asset images. Show them as real crisp app icons and real screenshots, with their original colors, shapes and layout. Never invent a logo. Never redraw UI as a flat illustration or a 3D cartoon.
- Large and readable at phone size. Keep the bottom-right corner free of text and key graphics.
- Do not add any graphic, card, icon or UI that is not described in LAYOUT.

TEXT RULES:
- The only new text in the image is [exact text]. Spell it exactly, with correct Vietnamese diacritics.
- Text that already exists inside an attached UI screenshot or logo stays as it is. No other text, letters, numbers, logos or watermarks anywhere.
```

## Prompt

Mỗi mẫu 1 mục `### tN, khuôn X: <ý>`, gồm 2 khối code: lệnh `gen_thumb.py`, rồi prompt (LAYOUT + `[khối ..., với:]`).
