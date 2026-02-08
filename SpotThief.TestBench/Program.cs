using SpotThief.DataLib;

string seed = "itransition_rocks_not";
string locale = "ja"; // Testing 'ja' to see the 60:40 backdrop logic
double likesSlider = 3.7;
string mockApi = "http://localhost:8000";

Console.WriteLine($"--- SpotThief Visual Integration Test (Locale: {locale}) ---");

// Generate 10 songs to see variety in props and backdrops
var songs = SongGenerator.GenerateSongs(seed, locale, count: 10, startIndex: 0, likesSlider, mockApi);

foreach (var s in songs)
{
    Console.WriteLine($"\n[#{s.Index}] {s.Title}");
    Console.WriteLine($"Artist: {s.Artist}");
    // This link is now clickable in most modern IDE terminals (VS Code/Rider)
    Console.WriteLine($"View Cover: {s.CoverUrl}");
}

Console.WriteLine("\n--- Logic Stress Test ---");
// Let's grab song #105 specifically to see if it remains stable
var song105 = SongGenerator.GenerateSongs(seed, locale, 1, 105, likesSlider, mockApi)[0];
Console.WriteLine($"Song #105 Stable URL: {song105.CoverUrl}");