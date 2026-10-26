# Synthetic (fake) axial T2-style brain slices. Not real patient data.
import numpy as np, sys
from PIL import Image, ImageFilter, ImageDraw
N, S = 256, 20
OUT = sys.argv[1]
yy, xx = np.mgrid[-1:1:N*1j, -1:1:N*1j]  # y grows downward: top of image = front of head
rng = np.random.default_rng(7)

def ell(cx, cy, rx, ry): return ((xx-cx)/rx)**2 + ((yy-cy)/ry)**2 <= 1

def slice_img(z, kind):
    s = np.sqrt(max(0.02, 1 - (2*z-1)**2 * 0.85))      # head shrinks toward top/bottom
    img = np.zeros((N, N))
    img[ell(0, 0, .78*s, .92*s)] = .25                   # scalp / skull ring (dark-ish)
    brain = ell(0, 0, .70*s, .84*s)
    img[brain] = .50                                    # grey matter
    img[ell(0, 0, .58*s, .72*s)] = .36                  # white matter
    mid = 0.25 < z < 0.75
    k = 2.6 if kind == 'hydro' else 1.0
    if mid:
        v = s * (1 - abs(2*z-1)*1.2) * k
        for sx in (-1, 1):
            img[ell(sx*.13*k**.5, -.05, .09*v+.001, .30*v+.001)] = .92   # lateral ventricles (CSF = bright on T2)
    if kind == 'tumour':   # right frontal (image left, top), z 0.40-0.75
        zc, r = 0.57, 0.18
        d = abs(z-zc)/r
        if d < 1:
            rr = np.sqrt(1-d*d)
            img[ell(-.30, -.38, .26*rr+.001, .26*rr+.001)] = .62     # oedema
            img[ell(-.30, -.38, .13*rr+.001, .13*rr+.001)] = .97     # lesion core
    if kind == 'stroke':   # left MCA-territory wedge (image right), z 0.35-0.7
        if 0.33 < z < 0.72:
            r = np.hypot(xx, yy); a = np.degrees(np.arctan2(yy, xx))
            wedge = brain & (r > .40*s) & (a > -20) & (a < 28) & (xx > 0)
            img[wedge] = .95
    img += rng.normal(0, .025, img.shape)
    im = Image.fromarray((np.clip(img, 0, 1)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.4))
    d = ImageDraw.Draw(im); d.text((6, 6), "MOCK - NOT REAL", fill=170); d.text((6, 18), f"slice {int(z*(S-1))+1}/{S}", fill=170)
    d.text((6, 242), "R", fill=170); d.text((244, 242), "L", fill=170)
    return im

for kind in ('tumour', 'stroke', 'hydro'):
    for i in range(S):
        slice_img(i/(S-1), kind).save(f"{OUT}/mock-mri-{kind}-{i+1:02d}.png")
# one montage for eyeballing
m = Image.new('L', (N*5, N*3))
for r, kind in enumerate(('tumour', 'stroke', 'hydro')):
    for c, i in enumerate((4, 8, 10, 12, 15)): m.paste(Image.open(f"{OUT}/mock-mri-{kind}-{i+1:02d}.png"), (c*N, r*N))
m.resize((N*5//2, N*3//2)).save(sys.argv[2])
