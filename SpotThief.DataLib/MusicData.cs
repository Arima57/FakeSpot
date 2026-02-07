namespace SpotThief.DataLib;

public static class MusicData
{
    public static readonly string[] Genres = {
        "Synthwave", "City Pop", "Dream Pop", "Math Rock", "Post-Punk", 
        "Lo-Fi Beats", "Future Funk", "Dark Techno", "Ambient Whale", 
        "Acid Jazz", "Hardstyle", "Phonk", "Nu-Disco", "Industrial", 
        "Shoegaze", "Glitch Hop", "Emo Rap", "Hyperpop", "Eurobeat", 
        "Krautrock", "Skate Punk", "Chamber Pop", "Doom Metal", "Bossa Nova", "Dubstep"
    };

    // --- Native English Dataset (Western Vibe) ---
    private static readonly string[] EnPrefix = { 
        "Electric", "Neon", "Broken", "Silent", "Crimson", "Velvet", "Digital", "Lunar", "Solar", "Midnight",
        "Atomic", "Bitter", "Sweet", "Faded", "Golden", "Iron", "Plastic", "Vivid", "Static", "Wild",
        "Abstract", "Aether", "Alpha", "Amnesic", "Ancient", "Apex", "Astral", "Aura", "Autumn", "Azure",
        "Bloom", "Blue", "Burning", "Canyon", "Carbon", "Celestial", "Chrome", "Cobalt", "Cosmic", "Crystal",
        "Deep", "Desert", "Divine", "Dusty", "Echoing", "Ethereal", "Ever", "Fallen", "Floral", "Frozen",
        "Ghostly", "Glass", "Glitch", "Hollow", "Infinite", "Jade", "Liquid", "Lonely", "Lost", "Luminous"
    };

    private static readonly string[] EnSuffix = { 
        "Dreams", "Rain", "Ghost", "Heart", "Sky", "Echo", "Machine", "River", "Night", "Summer",
        "Winter", "Road", "Mirror", "Shadow", "Voice", "Garden", "Ocean", "City", "Vibration", "Horizon",
        "Abyss", "Anomaly", "Arcade", "Archive", "Arrival", "Ascent", "Atmosphere", "Beacon", "Canyon", "Capsule",
        "Cascade", "Chapter", "Circuit", "Cloud", "Coast", "Code", "Colony", "Compass", "Current", "Dawn",
        "Daylight", "Drift", "Empire", "Entropy", "Era", "Escape", "Exile", "Fable", "Field", "Flare",
        "Flow", "Flux", "Forest", "Fragment", "Frequency", "Galaxy", "Gateway", "Gaze", "Glow", "Gravity"
    };

    // --- Japanese Dataset (Native + J-Pop Style English) ---
    private static readonly string[] JpNativePrefix = {
        "真夜中の", "都会の", "プラスティック", "週末の", "たそがれの", "秘密の", "銀河の", "色のない", "最後の", "透明な",
        "青い", "輝く", "踊る", "眠れない", "不思議な", "虹色の", "雨の", "光る", "遠い", "忘却の", "逆光", "命の"
    };

    private static readonly string[] JpNativeSuffix = {
        "ドア", "ラブ", "メロディ", "ダンス", "ハイウェイ", "ナイト", "リズム", "ハート", "シグナル", "記憶",
        "海辺", "電話", "風", "涙", "万華鏡", "物語", "パレード", "エコー", "幻想", "さよなら", "閃光", "革命"
    };

    private static readonly string[] JpEngStylePrefix = {
        "Kick", "Super", "Ultra", "Hyper", "Neo", "Giga", "Cyber", "Mega", "New", "Shining", 
        "Brave", "Burning", "Last", "First", "Final", "Idol", "Special", "Hero", "Sugar", "Bitter"
    };

    private static readonly string[] JpEngStyleSuffix = {
        "Back", "Drive", "Beat", "Girl", "Boy", "World", "Star", "Zone", "Gate", "Day",
        "High", "Low", "Game", "Show", "Music", "Song", "Live", "Life", "Hero", "Machine"
    };

    public static string GenerateLocalizedTitle(Bogus.Faker f, string locale)
    {
        string loc = locale.ToLower();
        if (loc == "ru") return f.Commerce.ProductName();

        bool isJpLocale = (loc == "ja" || loc == "jp");

        // Logic for JP Locale: 35% chance to be English-titled J-Pop song
        if (isJpLocale && f.Random.Decimal() < 0.35m)
        {
            return GenerateCompositeTitle(f, JpEngStylePrefix, JpEngStyleSuffix, " ");
        }

        // Standard JP logic (Wholly Japanese)
        if (isJpLocale)
        {
            return GenerateCompositeTitle(f, JpNativePrefix, JpNativeSuffix, "");
        }

        // Standard EN logic
        return GenerateCompositeTitle(f, EnPrefix, EnSuffix, " ");
    }

    private static string GenerateCompositeTitle(Bogus.Faker f, string[] prefixes, string[] suffixes, string separator)
    {
        int roll = f.Random.Int(1, 100);
        
        if (roll <= 15) return f.PickRandom(suffixes); // 1-word
        
        if (roll <= 80) // 2-words
            return $"{f.PickRandom(prefixes)}{separator}{f.PickRandom(suffixes)}";

        // 3-words
        return $"{f.PickRandom(prefixes)}{separator}{f.PickRandom(prefixes)}{separator}{f.PickRandom(suffixes)}";
    }
}