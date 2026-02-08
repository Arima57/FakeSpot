import uvicorn
from urllib.parse import unquote_plus
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing the functional generators directly
from app.api.v1.image_gen import generator as generate_image
from app.api.v1.audio_gen import generator as generate_audio

app = FastAPI(
    title="SpotThief Generation API",
    description="The Image and audio gen microservice provider",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/image")
async def imagen(seed: str, index: int, title: str, artist: str, locale: str):
    # Reverse the C# Uri.EscapeDataString logic
    clean_title = unquote_plus(title)
    clean_artist = unquote_plus(artist)
    
    # This will return a StreamingResponse (the JPEG)
    return await generate_image(seed=seed, 
                                index=index, 
                                title=clean_title, 
                                artist=clean_artist,
                                locale=locale)

@app.get("/audio")
async def audio_gen(seed: str, index: int, title: str, artist: str):
    # Even if audio doesn't use title/artist yet, 
    # we decode it to keep the signatures identical
    clean_title = unquote_plus(title)
    clean_artist = unquote_plus(artist)
    
    # This will return a StreamingResponse (the MP3/WAV)
    return await generate_audio(seed, index, clean_title, clean_artist)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)