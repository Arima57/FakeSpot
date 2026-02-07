namespace SpotThief.DataLib;

public class Song
{

    public int Index { get; set; }
    public string SongId { get; set; } = string.Empty; // ISRC
    public string Title { get; set; } = string.Empty;
    public string Artist { get; set; } = string.Empty;
    public string Album { get; set; } = string.Empty;
    public string Genre { get; set; } = string.Empty;

    
    public int Likes { get; set; }
    public double ReviewAverage { get; set; }

    public string CoverUrl { get; set; } = string.Empty;
    public string AudioUrl { get; set; } = string.Empty;

    // --- Metadata ---
    public string Language { get; set; } = string.Empty;
}