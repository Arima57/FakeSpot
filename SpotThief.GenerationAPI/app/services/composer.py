import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat

class ImageComposer:
    def __init__(self):
        self.output_size = (600, 600)

    def compose(self, seed, backdrop, props, halftone, font_path, title, artist):
        rng = random.Random(seed)
        
        # 1. Background Sizing & Framing
        # 20% chance to frame a 500x500 image inside 600x600
        canvas, base_dominant = self._prepare_canvas(rng, backdrop)
        accent_color = self._get_accent_color(base_dominant)

        # 2. Halftone Strategy (Mutually Exclusive)
        ht_on_backdrop = rng.choice([True, False]) if halftone else False
        if ht_on_backdrop:
            canvas = self._apply_halftone(canvas, halftone, opacity=0.3)

        # 3. Handle Label & Dominant Prop
        on_prop = rng.random() < 0.80 if props else False
        # 25% chance for an empty rectangle instead of a prop image
        use_empty_rect = rng.random() < 0.25 if on_prop else False
        
        # Typography Scaling (80% music bigger)
        music_bigger = rng.random() < 0.80
        t_size, a_size = (60, 35) if music_bigger else (35, 60)

        label_img = self._generate_label(
            rng, title, artist, font_path, t_size, a_size, 
            accent_color, base_dominant, props, on_prop, use_empty_rect
        )

        # 4. Halftone on Props (If not on backdrop)
        processed_props = props
        if not ht_on_backdrop and halftone and props:
            processed_props = [self._apply_halftone(p, halftone, is_prop=True) for p in props]

        # 5. Assemble
        canvas = self._place_random_props(rng, canvas, processed_props)
        
        label_pos = rng.randint(0, 24)
        label_rot = self._get_weighted_rotation(rng)
        canvas = self._place_label(canvas, label_img, label_pos, label_rot)

        return canvas.convert("RGB")

    # --- NEW REFINED HELPERS ---

    def _prepare_canvas(self, rng, backdrop):
        """Handles resizing and the 20% framing logic."""
        dom = self._get_dominant_color(backdrop)
        
        if rng.random() < 0.20:
            # Create a 600x600 canvas with a 'pop' frame color
            pop_frame_color = self._get_accent_color(dom)
            canvas = Image.new("RGBA", self.output_size, pop_frame_color)
            
            # Center the backdrop at 500x500
            inner = backdrop.resize((500, 500), Image.Resampling.LANCZOS).convert("RGBA")
            canvas.paste(inner, (50, 50), inner)
            return canvas, dom
        else:
            return backdrop.resize(self.output_size, Image.Resampling.LANCZOS).convert("RGBA"), dom

    def _generate_label(self, rng, title, artist, font_path, t_size, a_size, 
                        accent, dom_color, props, on_prop, use_empty_rect):
        t_font = ImageFont.truetype(font_path, t_size)
        a_font = ImageFont.truetype(font_path, a_size)
        
        # Calculate bounds
        t_w, t_h = t_font.getbbox(title)[2:]
        a_w, a_h = a_font.getbbox(artist)[2:]
        w, h = max(t_w, a_w) + 60, (t_h + a_h) + 80
        
        label_canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(label_canvas)

        if on_prop:
            if use_empty_rect:
                # 25% Chance: Empty Rectangle with border
                draw.rectangle([0, 0, w, h], outline=accent, width=5)
                txt_color = accent
            else:
                # Stretch a dominant prop
                base_prop = rng.choice(props).resize((w, h))
                label_canvas.paste(base_prop, (0, 0), base_prop)
                txt_color = dom_color if rng.random() < 0.7 else "white"
            
            draw.text((30, 20), title, font=t_font, fill=txt_color)
            draw.text((30, 30 + t_h), artist, font=a_font, fill=txt_color)
        else:
            # Direct text
            draw.text((30, 20), title, font=t_font, fill=accent)
            draw.text((30, 30 + t_h), artist, font=a_font, fill=accent)
            
        return label_canvas

    def _apply_halftone(self, target, ht_pattern, opacity=1.0, is_prop=False):
        """Uses the halftone as a luminance mask or overlay."""
        ht_resized = ht_pattern.resize(target.size).convert("L")
        if is_prop:
            # If used on props, use the halftone as a transparency filter (clipping)
            target_alpha = target.split()[-1]
            new_alpha = ImageMath.eval("convert(a & h, 'L')", a=target_alpha, h=ht_resized)
            target.putalpha(new_alpha)
            return target
        else:
            # If used on backdrop, simple overlay
            overlay = Image.new("RGBA", target.size, (0,0,0,0))
            overlay.putalpha(ht_resized)
            return Image.blend(target, Image.alpha_composite(target, overlay), opacity)

    def _get_dominant_color(self, img):
        return tuple(np.array(img.resize((1, 1))).flatten()[:3])

    def _get_accent_color(self, rgb):
        # Shift hue or invert for high pop
        return tuple(255 - c for c in rgb)