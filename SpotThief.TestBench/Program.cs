using SpotThief.DataLib;

string seed = "itransition_rocks_not";
string locale = "ru";
double likesSlider = 3.7;
string mockApi = "http://localhost:8000";

Console.WriteLine($"--- Testing Determinism (Seed: {seed}, Slider: {likesSlider}) ---");

// Generate 5 songs
var songs = SongGenerator.GenerateSongs(seed, locale, count:5, 0, likesSlider, mockApi);

foreach (var s in songs)
{
    Console.WriteLine($"[#{s.Index}] {s.Title} by {s.Artist} | Likes: {s.Likes}");
    Console.WriteLine($"      URL: {s.CoverUrl}");
}

Console.WriteLine("\n--- Verification: If I run it again, are the names identical? ---");
var songsCheck = SongGenerator.GenerateSongs(seed, locale, 1, 0, likesSlider, mockApi);
Console.WriteLine($"Check: {songsCheck[0].Title} == {songs[0].Title} ? {(songsCheck[0].Title == songs[0].Title ? "YES" : "NO")}");