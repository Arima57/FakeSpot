import random
import httpx
import colorsys
from io import BytesIO
from PIL import Image
from fastapi.responses import StreamingResponse
from app.core.seeding import get_identity_seed
from app.core.resources import assets 
from app.services.composer import ImageComposer

composer = ImageComposer()

def get_aesthetic_color(rng: random.Random) -> tuple:
    """Generates a vibrant, design-friendly solid color using HSL."""
    # Hue: Full spectrum (0-1)
    # Saturation: 0.5 - 0.8 (Vibrant but not eye-searing)
    # Lightness: 0.4 - 0.7 (Good for text contrast)
    h = rng.random()
    s = rng.uniform(0.5, 0.8)
    l = rng.uniform(0.4, 0.7)
    
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))

async def fetch_picsum_image(url: str) -> Image.Image:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGBA")

async def generator(seed: str, index: int, title: str, artist: str, locale: str):
    ident_seed = get_identity_seed(f"{seed}_{locale}", index)
    rng = random.Random(ident_seed)

    # 1. Select Font
    locale_fonts = assets.fonts.get(locale, assets.fonts.get("en"))
    selected_font_path = rng.choice(locale_fonts)

    # 2. Backdrop Logic (The 10% Solid Color Rule)
    backdrop = None
    if rng.random() < 0.10:
        # 10% Chance: Solid aesthetic color
        color = get_aesthetic_color(rng)
        backdrop = Image.new("RGBA", (600, 600), color + (255,))
    else:
        # 90% Chance: Image-based (Picsum vs Pre-downloaded)
        use_picsum = True
        if locale == "ja" and rng.random() > 0.60:
            use_picsum = False

        if use_picsum:
            url = f"https://picsum.photos/seed/{ident_seed}/600/600"
            backdrop = await fetch_picsum_image(url)
        else:
            backdrop = rng.choice(assets.backdrops)

    # 3. Props Selection (Weighted)
    num_props = rng.choices([0, 1, 2, 3], weights=[20, 40, 10, 30], k=1)[0]
    selected_props = rng.sample(assets.props, min(num_props, len(assets.props)))

    # 4. Halftone Selection (20%)
    selected_halftone = None
    if rng.random() < 0.20 and assets.halftones:
        selected_halftone = rng.choice(assets.halftones)

    # 5. Composer Hand-off
    final_img = composer.compose(
        seed=ident_seed,
        backdrop=backdrop,
        props=selected_props,
        halftone=selected_halftone,
        font_path=selected_font_path,
        title=title,
        artist=artist
    )

    buf = BytesIO()
    final_img.save(buf, format="JPEG", quality=100)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/jpeg")