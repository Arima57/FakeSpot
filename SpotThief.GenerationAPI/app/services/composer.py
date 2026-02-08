import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageMath

class ImageComposer:
    def __init__(self):
        self.output_size = (600, 600)

    def compose(self, seed, backdrop, props, halftone, font_path, title, artist):
        rng = random.Random(seed)
        
        # 1. Background Preparation
        canvas, base_dominant = self._prepare_canvas(rng, backdrop)
        accent_color = self._get_accent_color(base_dominant)

        # 2. Halftone Logic (Mutex Backdrop vs Props)
        ht_on_backdrop = rng.choice([True, False]) if halftone else False
        if ht_on_backdrop:
            canvas = self._apply_halftone(canvas, halftone, opacity=0.3)

        # 3. Label Config & Baking
        on_prop = rng.random() < 0.80 if props else False
        use_empty_rect = rng.random() < 0.25 if on_prop else False
        music_bigger = rng.random() < 0.80
        t_size, a_size = (60, 35) if music_bigger else (35, 60)
        
        # Determine rotation early to bake it into the containment logic
        label_rot = self._get_weighted_rotation(rng)

        # This generates, outlines, rotates, and shrinks the label to fit
        label_img = self._generate_label(
            rng, title, artist, font_path, t_size, a_size, 
            accent_color, base_dominant, props, on_prop, use_empty_rect, label_rot
        )

        # 4. Prop Scattering
        processed_props = props
        if not ht_on_backdrop and halftone and props:
            processed_props = [self._apply_halftone(p, halftone, is_prop=False) for p in props]

        canvas = self._place_random_props(rng, canvas, processed_props)
        
        # 5. Final Label Placement
        label_pos = rng.randint(0, 24) # 5x5 Grid
        canvas = self._place_label(canvas, label_img, label_pos)

        return canvas.convert("RGB")

    # --- CORE HELPERS ---

    def _get_opposite_color(self, rgb):
        """Inverts RGB for high-contrast outlines."""
        return tuple(255 - c for c in rgb)

    def _generate_label(self, rng, title, artist, font_path, t_size, a_size, 
                        accent, dom_color, props, on_prop, use_empty_rect, rotation):
        """Creates the text block with mandatory high-contrast stroke and baked rotation."""
        try:
            t_font = ImageFont.truetype(font_path, t_size)
            a_font = ImageFont.truetype(font_path, a_size)
        except:
            t_font = ImageFont.load_default()
            a_font = ImageFont.load_default()
        
        # Measure text
        t_bbox = t_font.getbbox(title)
        a_bbox = a_font.getbbox(artist)
        t_w, t_h = t_bbox[2] - t_bbox[0], t_bbox[3] - t_bbox[1]
        a_w, a_h = a_bbox[2] - a_bbox[0], a_bbox[3] - a_bbox[1]
        
        # Padding for stroke and layout
        stroke_width = 4
        padding = 70
        w, h = max(t_w, a_w) + padding, (t_h + a_h) + padding + 10
        
        label_canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(label_canvas)

        # Determine Main Text Color
        if on_prop:
            if use_empty_rect:
                draw.rectangle([0, 0, w-1, h-1], outline=accent, width=5)
                txt_color = accent
            else:
                base_prop = rng.choice(props).resize((w, h), Image.Resampling.LANCZOS)
                label_canvas.paste(base_prop, (0, 0), base_prop)
                txt_color = dom_color if rng.random() < 0.7 else (255, 255, 255)
        else:
            txt_color = accent

        outline_color = self._get_opposite_color(txt_color)

        # Draw Title and Artist with Stroke
        draw.text((35, 25), title, font=t_font, fill=txt_color, 
                  stroke_width=stroke_width, stroke_fill=outline_color)
        draw.text((35, 35 + t_h), artist, font=a_font, fill=txt_color, 
                  stroke_width=stroke_width, stroke_fill=outline_color)

        # 10% Cutout Effect
        if on_prop and not use_empty_rect and rng.random() < 0.10:
            mask = Image.new("L", (w, h), 255)
            m_draw = ImageDraw.Draw(mask)
            m_draw.text((35, 25), title, font=t_font, fill=0, stroke_width=stroke_width)
            m_draw.text((35, 35 + t_h), artist, font=a_font, fill=0, stroke_width=stroke_width)
            label_canvas.putalpha(mask)

        # ROTATE AND SCALE TO FIT 600x600
        rotated = label_canvas.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
        rw, rh = rotated.size
        
        # Limit to 580 to prevent touching the absolute edge
        if rw > 580 or rh > 580:
            scale = min(580 / rw, 580 / rh)
            rotated = rotated.resize((int(rw * scale), int(rh * scale)), Image.Resampling.LANCZOS)
            
        return rotated

    def _place_label(self, canvas, label, pos_index):
        """Uses a centered grid system with boundary clamping."""
        lw, lh = label.size
        
        cell_size = 600 // 5
        center_x = (pos_index % 5) * cell_size + (cell_size // 2)
        center_y = (pos_index // 5) * cell_size + (cell_size // 2)

        # Calculate top-left for composite
        x = center_x - (lw // 2)
        y = center_y - (lh // 2)

        # Final safety clamp: Push back onto 600x600 canvas
        final_x = max(0, min(x, 600 - lw))
        final_y = max(0, min(y, 600 - lh))

        canvas.alpha_composite(label, (final_x, final_y))
        return canvas

    def _prepare_canvas(self, rng, backdrop):
        dom = self._get_dominant_color(backdrop)
        if rng.random() < 0.20:
            pop = self._get_accent_color(dom)
            canvas = Image.new("RGBA", self.output_size, pop + (255,))
            inner = backdrop.resize((500, 500), Image.Resampling.LANCZOS).convert("RGBA")
            canvas.paste(inner, (50, 50), inner)
            return canvas, dom
        return backdrop.resize(self.output_size, Image.Resampling.LANCZOS).convert("RGBA"), dom

    def _apply_halftone(self, target, ht_pattern, opacity=1.0, is_prop=False):
        ht_resized = ht_pattern.resize(target.size).convert("L")
        if is_prop:
            target_alpha = target.split()[-1]
            new_alpha = ImageMath.eval("convert(a & h, 'L')", a=target_alpha, h=ht_resized)
            target.putalpha(new_alpha)
            return target
        overlay = Image.new("RGBA", target.size, (0, 0, 0, 0))
        overlay.putalpha(ht_resized)
        return Image.blend(target, Image.alpha_composite(target, overlay), opacity)

    def _get_dominant_color(self, img):
        return tuple(np.array(img.resize((1, 1))).flatten()[:3])

    def _get_accent_color(self, rgb):
        return tuple(255 - c for c in rgb)

    def _get_weighted_rotation(self, rng):
        roll = rng.random()
        if roll < 0.50: return 0
        if roll < 0.85: return rng.choice([90, 270])
        if roll < 0.95: return rng.choice([45, 135, 225, 315])
        return rng.randint(0, 359)

    def _place_random_props(self, rng, canvas, props):
        return canvas