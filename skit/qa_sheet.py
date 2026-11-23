"""QA: contact sheet of frames from out/qa-v2 with safe-zone guides + first/last frame loop check."""
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat
Q = 'out/qa-v2'; ts = ['0', '1.2', '2.5', '4', '6.5', '8.5', '9.9']
W, H, pad, lab = 540, 960, 16, 56
sheet = Image.new('RGB', (pad + len(ts) * (W + pad), lab + H + pad), (20, 20, 24))
d = ImageDraw.Draw(sheet)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
for i, t in enumerate(ts):
    x = pad + i * (W + pad)
    sheet.paste(Image.open(f'{Q}/t{t}.png').convert('RGB').resize((W, H), Image.LANCZOS), (x, lab))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rectangle([0, 0, W - 1, 110], outline=(255, 60, 60, 220), width=2)          # top 220px
    od.rectangle([0, H - 170, W - 1, H - 1], outline=(255, 60, 60, 220), width=2)  # bottom 340px
    sheet.paste(ov, (x, lab), ov)
    d.text((x + 8, 12), f't = {t}s', fill=(255, 255, 255), font=f)
sheet.save(f'{Q}/contact-sheet.png')
a = Image.open(f'{Q}/t0.png').convert('L'); b = Image.open(f'{Q}/last.png').convert('L')
diff = ImageChops.difference(a, b)
print('first vs last frame: mean abs diff', round(ImageStat.Stat(diff).mean[0], 3), '/255, max', diff.getextrema()[1])
