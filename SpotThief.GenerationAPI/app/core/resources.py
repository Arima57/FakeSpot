import os
from PIL import Image

class ResourceManager:
    def __init__(self):
        self.base_path = "assets"
        self.fonts = self._load_fonts()
        self.props = self._load_image_folder("props")
        self.backdrops = self._load_image_folder("backdrops")
        self.halftones = self._load_image_folder("halftones")

    def _load_fonts(self):
        # Returns dict: {'en': [paths...], 'ja': [paths...], 'ru': [paths...]}
        fonts = {}
        for locale in ["en", "ja", "ru"]:
            path = os.path.join(self.base_path, "fonts", locale)
            if os.path.exists(path):
                fonts[locale] = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".ttf")]
        return fonts

    def _load_image_folder(self, subfolder):
        path = os.path.join(self.base_path, subfolder)
        if not os.path.exists(path): return []
        # Return loaded PIL Images to avoid disk I/O during request
        return [Image.open(os.path.join(path, f)).convert("RGBA") 
                for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Global instance
assets = ResourceManager()