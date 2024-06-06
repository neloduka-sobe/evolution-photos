from PIL import Image
import numpy as np

def shift_hue(image, hue_shift):
    # Convert image to numpy array and normalize to range [0, 1]
    img = np.array(image.convert('RGBA')).astype(float) / 255.0

    # Extract the RGB channels and alpha channel
    r, g, b, a = img[:,:,0], img[:,:,1], img[:,:,2], img[:,:,3]

    # Convert RGB to HSV
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    v = maxc
    s = (maxc - minc) / maxc
    s[maxc == 0] = 0
    rc = (maxc - r) / (maxc - minc)
    gc = (maxc - g) / (maxc - minc)
    bc = (maxc - b) / (maxc - minc)
    h = np.zeros_like(r)
    h[maxc == r] = bc[maxc == r] - gc[maxc == r]
    h[maxc == g] = 2.0 + rc[maxc == g] - bc[maxc == g]
    h[maxc == b] = 4.0 + gc[maxc == b] - rc[maxc == b]
    h[minc == maxc] = 0
    h = (h / 6.0) % 1.0

    # Shift hue
    h = (h + hue_shift / 360.0) % 1.0

    # Convert HSV back to RGB
    i = (h * 6.0).astype(int)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    r = np.choose(i % 6, [v, q, p, p, t, v])
    g = np.choose(i % 6, [t, v, v, q, p, p])
    b = np.choose(i % 6, [p, p, t, v, v, q])

    # Combine back into an RGBA image
    shifted_img = np.stack([r, g, b, a], axis=-1)
    shifted_img = (shifted_img * 255).astype(np.uint8)
    shifted_img = Image.fromarray(shifted_img, 'RGBA')

    return shifted_img

# Load the image
sprite_image = Image.open('sprite.png')

# Shift the hue by 100 degrees
for i in range(0, 361, 10):
    shifted_image = shift_hue(sprite_image, i)
    shifted_image.show()
