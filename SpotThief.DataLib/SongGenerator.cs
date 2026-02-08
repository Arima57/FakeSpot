using Bogus;
using System.Security.Cryptography;
using System.Text;

namespace SpotThief.DataLib;

public static class SongGenerator
{
    public static List<Song> GenerateSongs(string globalSeed, string locale, int count, int startIndex, double avgLikes, string apiBaseUrl)
    {
        var songs = new List<Song>();
        var cleanBaseUrl = apiBaseUrl.TrimEnd('/');

        for (int i = 0; i < count; i++)
        {
            int currentIndex = startIndex + i;
            // Stable seed ensures changing the 'avgLikes' slider won't change the Song Title
            int identitySeed = GetStableIntSeed(globalSeed, currentIndex);

            var faker = new Faker<Song>(locale)
                .UseSeed(identitySeed)
                .RuleFor(s => s.Index, f => currentIndex)
                .RuleFor(s => s.SongId, f => f.Random.Guid().ToString())
                // Use our "Chonky" dataset logic
                .RuleFor(s => s.Title, f => MusicData.GenerateLocalizedTitle(f, locale))
                .RuleFor(s => s.Artist, f => f.Name.FullName())
                .RuleFor(s => s.Album, f => f.Company.CompanyName() + " Hits")
                .RuleFor(s => s.Genre, f => f.PickRandom(MusicData.Genres))
                .RuleFor(s => s.Language, f => locale);

            var song = faker.Generate();

            // Deterministic Probability for Likes (e.g., 3.7 -> 70% chance of 4, 30% of 3)
            var mathRng = new Random(identitySeed);
            song.Likes = (mathRng.NextDouble() < (avgLikes % 1)) 
                         ? (int)Math.Floor(avgLikes) + 1 
                         : (int)Math.Floor(avgLikes);

            // Construct URLs for Python Service
            string encodedTitle = Uri.EscapeDataString(song.Title);
            string encodedArtist = Uri.EscapeDataString(song.Artist);

            song.CoverUrl = $"{cleanBaseUrl}/image?seed={globalSeed}&index={currentIndex}&title={encodedTitle}&artist={encodedArtist}&locale={locale}";
            song.AudioUrl = $"{cleanBaseUrl}/audio?seed={globalSeed}&index={currentIndex}";

            songs.Add(song);
        }

        return songs;
    }

    private static int GetStableIntSeed(string seed, int index)
    {
        byte[] hash = SHA256.HashData(Encoding.UTF8.GetBytes($"{seed}_{index}"));
        return BitConverter.ToInt32(hash, 0);
    }
}