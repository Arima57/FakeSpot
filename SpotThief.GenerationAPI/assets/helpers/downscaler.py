import os
import re
from PIL import Image

# The log data you provided
log_data = """
 ✓ 002765ee261fbc54e8d549ea4cf2cd7e.jpg: Upscaled from 236x236 to 500x500
 ✓ 081a3dc3ca4c414619bc9933983f39b8.jpg: Upscaled from 60x60 to 500x500  
 ✓ 0972d1f5f7da4ede9f9f77fe634625e5.jpg: Upscaled from 236x236 to 500x500
 ✓ 0bb2971d30174700ee37ab2b09a60806.jpg: Upscaled from 60x60 to 500x500  
 ✓ 0d4609a1d0996c09f4b0901bae099f9b.jpg: Upscaled from 60x60 to 500x500  
 ✓ 0debeed3ff3814e501e03fc3d7836cdd.jpg: Upscaled from 236x236 to 500x500
 ✓ 119c024809b51cb5e36fb702310fd593.jpg: Upscaled from 236x236 to 500x500
 ✓ 11fc20f4edc77c9c31d5577a5c9464ea.jpg: Upscaled from 236x236 to 500x500
 ✓ 14ce10b4ab034abcab6c2b5e0d0acfd6.jpg: Upscaled from 236x236 to 500x500
 ✓ 1bfa5fc5723bb8283ad5600b6049bc2a.jpg: Upscaled from 132x132 to 500x500
 ✓ 1e5b13873ff3a67a1c699455c7cc908b.jpg: Upscaled from 235x235 to 500x500
 ✓ 1f02959f7acddff8ca8a43b238a11931.jpg: Upscaled from 235x235 to 500x500
 ✓ 240_F_1672712699_mTidj1LW2IKkv5jSB1ngf6pA6Ufn7MXX.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_243540225_eFgLenOdWupvKzwPevl3jOTkTtcVu8AP.jpg: Upscaled from 240x240 to 500x500 
 ✓ 240_F_314667105_dDHNq3VgslbDsQPutrZlVy5dQUpJSghw.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_332378327_VjLMgYK3wta2mpyDqHxVxKei7P2DK68f.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_486097245_VDIQYlaTsrQ1gAwY025T89WRpNQQ6jAy.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_511786103_Jv7qDzafhobxsNSUZ73LVY4fV8ekG61p.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_511786155_2zkxpRcEEddD1Jyz0wjlrYYHiDLBDsY7.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_529014950_oowsLe7IMjQAqEl1QTRA5TH0Resd6kM9.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_537111191_fIKwpEADS3U5m1p0M4x5tW0jXs9ceAtg.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_547290206_MPVRUNHeapl0aBpuUl7WsAaZpEeSn09X.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_549300347_SX9jbPCtdqJ3lvDtkmizLPWzlbpjYfDJ.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_549300389_wnWJlik3ydCOVZc7B4ifWdu3ZEgezCOh.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_558238547_XENLmDuDj65RKbFmdABdWLyTMd5rafju.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_622880334_rN0N68xCyWuhOuM07ajqCWAuVgGJZxlL.jpg: Upscaled from 240x240 to 500x500
 ✓ 240_F_711696250_EpSfi5AHfvXSnHVlXcfEKsDfYrAoE8Ab.jpg: Upscaled from 240x240 to 500x500
 ✓ 247ede49e3e8cabde7f9eb7da8ec2524.jpg: Upscaled from 236x236 to 500x500
 ✓ 27a48340d789917cf22869655ff95dea.jpg: Upscaled from 60x60 to 500x500  
 ✓ 2bb9e24cc48fa9e988ca2bce6a5174e5.jpg: Upscaled from 236x236 to 500x500
 ✓ 360_F_1012460191_E0kLcTEN3EZSBgG9ThqwH2yvuR3R28ri.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_1532764721_ihlemV2h0VxvZmKI1LL6UvBXRwyrHeH0.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_1672747831_HjgNujC71zZ9bo98gJZp9fOhFhYxuM4L.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_257475320_KkSO91GhTlFYrW3b8asStkWPe1xNQl8b.jpg: Upscaled from 360x360 to 500x500 
 ✓ 360_F_332378327_VjLMgYK3wta2mpyDqHxVxKei7P2DK68f.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_332827424_Xf9fnGktUtoaDT9wcu38YRgw7SfsI7tg.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_529068793_T5VEd5qvDEtPXWGyMp4shDfZFcakjhQc.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_541482584_Oo647alovInzgQtuZ1rlgUcvBn2ywsxE.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_570659666_UXrfivtiwXTVd5lBCQkpTLYIKtC5XdWg.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_575476059_HA7V33bf2VJCFRK97nh0RiLVnnHiK4RM.jpg: Upscaled from 360x360 to 500x500
 ✓ 360_F_904331755_PwaPvrttwANBqoRsm1Dj140TVuLeXnqd.jpg: Upscaled from 360x360 to 500x500
 ✓ 3616e2f8cdce9697a622ab1685ffb930.jpg: Upscaled from 234x234 to 500x500
 ✓ 38693e90006fb166f1e51f37019bbf09.jpg: Upscaled from 132x132 to 500x500
 ✓ 3b3c96b301e354406f667472fbc70bb9.jpg: Upscaled from 236x236 to 500x500
 ✓ 492c4f761ca7aec4ae3e3f1e935c35df.jpg: Upscaled from 232x231 to 500x500
 ✓ 5282ade590cd40ec4744cc708e523b65.jpg: Upscaled from 224x223 to 500x500
 ✓ 6134a5743c3eafbdc57fd2b58353e477.jpg: Upscaled from 236x236 to 500x500
 ✓ 65db88272cdacb6f83bbb989433e5409.jpg: Upscaled from 132x132 to 500x500
 ✓ 6a4fd650487bdd0670906c8ee308152a.jpg: Upscaled from 236x236 to 500x500
 ✓ 6a88c6571e5514ce329b8c50f1bb3cea.jpg: Upscaled from 236x236 to 500x500
 ✓ 7dd0abfea7553dd326039b6fb6018360.jpg: Upscaled from 236x236 to 500x500
 ✓ 8185efc2abe6cf1052e9048203d6b464.jpg: Upscaled from 236x236 to 500x500
 ✓ 882c39a2ef270547e09e391533434cec.jpg: Upscaled from 236x236 to 500x500
 ✓ 88982129f0315219ad9f65124d6680eb.jpg: Upscaled from 236x236 to 500x500
 ✓ 8cacabd609a04ecc845a3c987c1ff660.jpg: Upscaled from 132x132 to 500x500
 ✓ 8e8c5445605767cbcd673d75a31bded8.jpg: Upscaled from 236x236 to 500x500
 ✓ 925499b86b94ba690c0a56adbff89682.jpg: Upscaled from 132x132 to 500x500
 ✓ 97f9c74232011a1c582f82a3a06eaa51.jpg: Upscaled from 236x236 to 500x500
 ✓ 9af702a35bfcc07bbc7fb7d25d5cb8ec.jpg: Upscaled from 155x155 to 500x500
 ✓ 9fdf5e309cf43642a4b1c0e352cc0ad7.jpg: Upscaled from 132x132 to 500x500
 ✓ adb3d8d0fe975e2c763423f03940e844.jpg: Upscaled from 236x236 to 500x500
 ✓ b2e13266a48b1df41166421128d3d878.jpg: Upscaled from 236x236 to 500x500
 ✓ ef1ac773ed46de8d302eb013925e7948.jpg: Upscaled from 236x236 to 500x500
 ✓ fbf12a814f34c9431d26753c3377a1d4.jpg: Upscaled from 236x236 to 500x500

""" # ... (Paste the rest of your log inside these triple quotes)

def restore_originals(log_text):
    # Pattern to find: [filename] then "from [width]x[height]"
    pattern = r"✓ (.*?): Upscaled from (\d+)x(\d+)"
    matches = re.findall(pattern, log_text)

    if not matches:
        print("No matches found in the log. Check your formatting!")
        return

    print(f"Found {len(matches)} images to restore. Commencing downscale...")

    for filename, orig_w, orig_h in matches:
        filename = filename.strip()
        if os.path.exists(filename):
            try:
                with Image.open(filename) as img:
                    # Restore to the smaller original size
                    # We use NEAREST here to avoid introducing any new "mush" 
                    # before the AI pass
                    orig_size = (int(orig_w), int(orig_h))
                    img_restored = img.resize(orig_size, Image.Resampling.NEAREST)
                    
                    img_restored.save(filename, quality=100)
                    print(f" ↺ Restored {filename} to {orig_w}x{orig_h}")
            except Exception as e:
                print(f" ✗ Error on {filename}: {e}")
        else:
            print(f" ? File not found: {filename}")

if __name__ == "__main__":
    restore_originals(log_data)
