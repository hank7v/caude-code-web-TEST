#!/usr/bin/env python3
"""
Curated Star Database Builder
Creates a comprehensive, high-quality star database from curated data sources
including nearest stars, bright stars, and notable stars across various distances.
"""

import json

def create_comprehensive_star_database():
    """Create a comprehensive curated star database"""

    stars = [
        # ===== NEAREST STARS (0-20 light-years) =====
        # These are our stellar neighbors with precise distance measurements

        {"name": "Proxima Centauri", "distance": 4.2465, "constellation": "Centaurus", "type": "Red Dwarf"},
        {"name": "Alpha Centauri A", "distance": 4.37, "constellation": "Centaurus", "type": "G-type Main Sequence"},
        {"name": "Alpha Centauri B", "distance": 4.37, "constellation": "Centaurus", "type": "K-type Main Sequence"},
        {"name": "Barnard's Star", "distance": 5.96, "constellation": "Ophiuchus", "type": "Red Dwarf"},
        {"name": "Wolf 359", "distance": 7.86, "constellation": "Leo", "type": "Red Dwarf"},
        {"name": "Lalande 21185", "distance": 8.31, "constellation": "Ursa Major", "type": "Red Dwarf"},
        {"name": "Sirius A", "distance": 8.60, "constellation": "Canis Major", "type": "A-type Main Sequence"},
        {"name": "Sirius B", "distance": 8.60, "constellation": "Canis Major", "type": "White Dwarf"},
        {"name": "Luyten 726-8A", "distance": 8.73, "constellation": "Cetus", "type": "Red Dwarf"},
        {"name": "Luyten 726-8B", "distance": 8.73, "constellation": "Cetus", "type": "Red Dwarf"},
        {"name": "Ross 154", "distance": 9.69, "constellation": "Sagittarius", "type": "Red Dwarf"},
        {"name": "Ross 248", "distance": 10.29, "constellation": "Andromeda", "type": "Red Dwarf"},
        {"name": "Epsilon Eridani", "distance": 10.50, "constellation": "Eridanus", "type": "K-type Main Sequence"},
        {"name": "Lacaille 9352", "distance": 10.74, "constellation": "Piscis Austrinus", "type": "Red Dwarf"},
        {"name": "Ross 128", "distance": 11.01, "constellation": "Virgo", "type": "Red Dwarf"},
        {"name": "EZ Aquarii A", "distance": 11.27, "constellation": "Aquarius", "type": "Red Dwarf"},
        {"name": "61 Cygni A", "distance": 11.41, "constellation": "Cygnus", "type": "K-type Main Sequence"},
        {"name": "61 Cygni B", "distance": 11.41, "constellation": "Cygnus", "type": "K-type Main Sequence"},
        {"name": "Procyon A", "distance": 11.46, "constellation": "Canis Minor", "type": "F-type Subgiant"},
        {"name": "Procyon B", "distance": 11.46, "constellation": "Canis Minor", "type": "White Dwarf"},
        {"name": "Struve 2398 A", "distance": 11.52, "constellation": "Draco", "type": "Red Dwarf"},
        {"name": "Groombridge 34 A", "distance": 11.62, "constellation": "Andromeda", "type": "Red Dwarf"},
        {"name": "Groombridge 34 B", "distance": 11.62, "constellation": "Andromeda", "type": "Red Dwarf"},
        {"name": "Epsilon Indi A", "distance": 11.83, "constellation": "Indus", "type": "K-type Main Sequence"},
        {"name": "Tau Ceti", "distance": 11.91, "constellation": "Cetus", "type": "G-type Main Sequence"},
        {"name": "GJ 1061", "distance": 12.04, "constellation": "Horologium", "type": "Red Dwarf"},
        {"name": "YZ Ceti", "distance": 12.13, "constellation": "Cetus", "type": "Red Dwarf"},
        {"name": "Luyten's Star", "distance": 12.37, "constellation": "Canis Minor", "type": "Red Dwarf"},
        {"name": "Teegarden's Star", "distance": 12.51, "constellation": "Aries", "type": "Red Dwarf"},
        {"name": "Kapteyn's Star", "distance": 12.78, "constellation": "Pictor", "type": "Red Dwarf"},
        {"name": "Lacaille 8760", "distance": 12.87, "constellation": "Microscopium", "type": "Red Dwarf"},
        {"name": "Kruger 60 A", "distance": 13.15, "constellation": "Cepheus", "type": "Red Dwarf"},
        {"name": "Ross 614 A", "distance": 13.35, "constellation": "Monoceros", "type": "Red Dwarf"},
        {"name": "Wolf 1061", "distance": 13.99, "constellation": "Ophiuchus", "type": "Red Dwarf"},
        {"name": "Van Maanen's Star", "distance": 14.07, "constellation": "Pisces", "type": "White Dwarf"},
        {"name": "Gliese 1", "distance": 14.23, "constellation": "Sculptor", "type": "Red Dwarf"},
        {"name": "TZ Arietis", "distance": 14.62, "constellation": "Aries", "type": "Red Dwarf"},
        {"name": "Gliese 876", "distance": 15.24, "constellation": "Aquarius", "type": "Red Dwarf"},
        {"name": "Gliese 412 A", "distance": 15.83, "constellation": "Ursa Major", "type": "Red Dwarf"},
        {"name": "Groombridge 1618", "distance": 15.89, "constellation": "Ursa Major", "type": "K-type Main Sequence"},
        {"name": "Gliese 388", "distance": 16.22, "constellation": "Leo", "type": "Red Dwarf"},
        {"name": "Gliese 83.1", "distance": 16.53, "constellation": "Eridanus", "type": "Red Dwarf"},
        {"name": "Altair", "distance": 16.73, "constellation": "Aquila", "type": "A-type Main Sequence"},
        {"name": "Gliese 166 A", "distance": 16.78, "constellation": "Orion", "type": "Red Dwarf"},
        {"name": "82 Eridani", "distance": 19.71, "constellation": "Eridanus", "type": "G-type Main Sequence"},
        {"name": "Delta Pavonis", "distance": 19.92, "constellation": "Pavo", "type": "G-type Main Sequence"},

        # ===== NEARBY STARS (20-50 light-years) =====

        {"name": "Sigma Draconis", "distance": 18.77, "constellation": "Draco", "type": "K-type Main Sequence"},
        {"name": "Eta Cassiopeiae A", "distance": 19.42, "constellation": "Cassiopeia", "type": "G-type Main Sequence"},
        {"name": "36 Ophiuchi A", "distance": 19.51, "constellation": "Ophiuchus", "type": "K-type Main Sequence"},
        {"name": "HR 7703", "distance": 20.35, "constellation": "Sagittarius", "type": "K-type Main Sequence"},
        {"name": "Chi Draconis A", "distance": 26.30, "constellation": "Draco", "type": "F-type Main Sequence"},
        {"name": "Vega", "distance": 25.04, "constellation": "Lyra", "type": "A-type Main Sequence"},
        {"name": "Fomalhaut", "distance": 25.13, "constellation": "Piscis Austrinus", "type": "A-type Main Sequence"},
        {"name": "Beta Comae Berenices", "distance": 29.95, "constellation": "Coma Berenices", "type": "G-type Main Sequence"},
        {"name": "Alpha Mensae", "distance": 33.27, "constellation": "Mensa", "type": "G-type Main Sequence"},
        {"name": "Pollux", "distance": 33.78, "constellation": "Gemini", "type": "K-type Giant"},
        {"name": "Arcturus", "distance": 36.66, "constellation": "Boötes", "type": "K-type Giant"},
        {"name": "Zeta Tucanae", "distance": 28.01, "constellation": "Tucana", "type": "F-type Main Sequence"},
        {"name": "Beta Hydri", "distance": 24.33, "constellation": "Hydrus", "type": "G-type Subgiant"},
        {"name": "Gamma Pavonis", "distance": 30.21, "constellation": "Pavo", "type": "F-type Main Sequence"},
        {"name": "Mu Cassiopeiae", "distance": 24.62, "constellation": "Cassiopeia", "type": "G-type Main Sequence"},
        {"name": "Iota Persei", "distance": 34.38, "constellation": "Perseus", "type": "G-type Giant"},
        {"name": "Beta Canum Venaticorum", "distance": 27.30, "constellation": "Canes Venatici", "type": "G-type Main Sequence"},
        {"name": "Gliese 570 A", "distance": 19.20, "constellation": "Libra", "type": "K-type Main Sequence"},
        {"name": "Zeta Reticuli", "distance": 39.53, "constellation": "Reticulum", "type": "G-type Main Sequence"},
        {"name": "54 Piscium", "distance": 36.11, "constellation": "Pisces", "type": "K-type Main Sequence"},
        {"name": "Rho Coronae Borealis", "distance": 56.22, "constellation": "Corona Borealis", "type": "G-type Main Sequence"},
        {"name": "Capella", "distance": 42.92, "constellation": "Auriga", "type": "G-type Giant"},
        {"name": "Chi1 Orionis", "distance": 28.30, "constellation": "Orion", "type": "G-type Main Sequence"},
        {"name": "Psi Serpentis", "distance": 47.92, "constellation": "Serpens", "type": "G-type Main Sequence"},

        # ===== MID-RANGE STARS (50-100 light-years) =====

        {"name": "Castor", "distance": 51.50, "constellation": "Gemini", "type": "A-type Main Sequence"},
        {"name": "Mizar", "distance": 82.87, "constellation": "Ursa Major", "type": "A-type Main Sequence"},
        {"name": "Alcor", "distance": 81.70, "constellation": "Ursa Major", "type": "A-type Main Sequence"},
        {"name": "Denebola", "distance": 35.89, "constellation": "Leo", "type": "A-type Main Sequence"},
        {"name": "Regulus", "distance": 79.30, "constellation": "Leo", "type": "B-type Main Sequence"},
        {"name": "Aldebaran", "distance": 65.23, "constellation": "Taurus", "type": "K-type Giant"},
        {"name": "Dubhe", "distance": 123.00, "constellation": "Ursa Major", "type": "K-type Giant"},
        {"name": "Merak", "distance": 79.40, "constellation": "Ursa Major", "type": "A-type Main Sequence"},
        {"name": "Phecda", "distance": 83.20, "constellation": "Ursa Major", "type": "A-type Main Sequence"},
        {"name": "Megrez", "distance": 58.40, "constellation": "Ursa Major", "type": "A-type Main Sequence"},
        {"name": "Alioth", "distance": 82.60, "constellation": "Ursa Major", "type": "A-type Main Sequence"},
        {"name": "Alkaid", "distance": 103.90, "constellation": "Ursa Major", "type": "B-type Main Sequence"},
        {"name": "Alphard", "distance": 177.00, "constellation": "Hydra", "type": "K-type Giant"},
        {"name": "Kochab", "distance": 130.90, "constellation": "Ursa Minor", "type": "K-type Giant"},
        {"name": "Thuban", "distance": 303.13, "constellation": "Draco", "type": "A-type Giant"},
        {"name": "Eltanin", "distance": 154.30, "constellation": "Draco", "type": "K-type Giant"},
        {"name": "Rastaban", "distance": 380.00, "constellation": "Draco", "type": "G-type Bright Giant"},
        {"name": "Alderamin", "distance": 49.05, "constellation": "Cepheus", "type": "A-type Main Sequence"},
        {"name": "Alfirk", "distance": 595.00, "constellation": "Cepheus", "type": "B-type Supergiant"},
        {"name": "Errai", "distance": 45.20, "constellation": "Cepheus", "type": "K-type Subgiant"},

        # ===== BRIGHT STARS (100-300 light-years) =====

        {"name": "Achernar", "distance": 139.00, "constellation": "Eridanus", "type": "B-type Main Sequence"},
        {"name": "Hadar", "distance": 392.00, "constellation": "Centaurus", "type": "B-type Giant"},
        {"name": "Acrux", "distance": 321.00, "constellation": "Crux", "type": "B-type Main Sequence"},
        {"name": "Mimosa", "distance": 280.00, "constellation": "Crux", "type": "B-type Giant"},
        {"name": "Gacrux", "distance": 88.60, "constellation": "Crux", "type": "Red Giant"},
        {"name": "Shaula", "distance": 570.00, "constellation": "Scorpius", "type": "B-type Main Sequence"},
        {"name": "Bellatrix", "distance": 252.00, "constellation": "Orion", "type": "B-type Giant"},
        {"name": "Elnath", "distance": 131.00, "constellation": "Taurus", "type": "B-type Giant"},
        {"name": "Alnair", "distance": 101.00, "constellation": "Grus", "type": "B-type Main Sequence"},
        {"name": "Alhena", "distance": 109.00, "constellation": "Gemini", "type": "A-type Main Sequence"},
        {"name": "Peacock", "distance": 179.00, "constellation": "Pavo", "type": "B-type Main Sequence"},
        {"name": "Canopus", "distance": 310.00, "constellation": "Carina", "type": "A-type Bright Giant"},
        {"name": "Adhara", "distance": 405.00, "constellation": "Canis Major", "type": "B-type Bright Giant"},
        {"name": "Wezen", "distance": 1607.00, "constellation": "Canis Major", "type": "F-type Supergiant"},
        {"name": "Sargas", "distance": 272.00, "constellation": "Scorpius", "type": "F-type Supergiant"},
        {"name": "Kaus Australis", "distance": 143.00, "constellation": "Sagittarius", "type": "B-type Main Sequence"},
        {"name": "Avior", "distance": 610.00, "constellation": "Carina", "type": "K-type Giant"},
        {"name": "Menkalinan", "distance": 81.00, "constellation": "Auriga", "type": "A-type Main Sequence"},
        {"name": "Atria", "distance": 415.00, "constellation": "Triangulum Australe", "type": "K-type Giant"},
        {"name": "Alhena", "distance": 109.00, "constellation": "Gemini", "type": "A-type Subgiant"},
        {"name": "Alpheratz", "distance": 97.00, "constellation": "Andromeda", "type": "B-type Main Sequence"},
        {"name": "Mirach", "distance": 199.00, "constellation": "Andromeda", "type": "Red Giant"},
        {"name": "Almach", "distance": 355.00, "constellation": "Andromeda", "type": "K-type Bright Giant"},
        {"name": "Hamal", "distance": 65.80, "constellation": "Aries", "type": "K-type Giant"},
        {"name": "Sheratan", "distance": 59.60, "constellation": "Aries", "type": "A-type Main Sequence"},
        {"name": "Mesarthim", "distance": 204.00, "constellation": "Aries", "type": "A-type Main Sequence"},

        # ===== DISTANT BRIGHT STARS (300-1000 light-years) =====

        {"name": "Spica", "distance": 250.00, "constellation": "Virgo", "type": "B-type Main Sequence"},
        {"name": "Polaris", "distance": 433.00, "constellation": "Ursa Minor", "type": "F-type Supergiant"},
        {"name": "Antares", "distance": 550.00, "constellation": "Scorpius", "type": "Red Supergiant"},
        {"name": "Betelgeuse", "distance": 548.00, "constellation": "Orion", "type": "Red Supergiant"},
        {"name": "Rigel", "distance": 860.00, "constellation": "Orion", "type": "Blue Supergiant"},
        {"name": "Saiph", "distance": 724.00, "constellation": "Orion", "type": "B-type Supergiant"},
        {"name": "Mintaka", "distance": 1200.00, "constellation": "Orion", "type": "O-type Giant"},
        {"name": "Alnilam", "distance": 1342.00, "constellation": "Orion", "type": "B-type Supergiant"},
        {"name": "Alnitak", "distance": 1260.00, "constellation": "Orion", "type": "O-type Supergiant"},
        {"name": "Deneb", "distance": 2615.00, "constellation": "Cygnus", "type": "A-type Supergiant"},
        {"name": "Sadr", "distance": 1520.00, "constellation": "Cygnus", "type": "F-type Supergiant"},
        {"name": "Gienah", "distance": 165.00, "constellation": "Cygnus", "type": "K-type Giant"},
        {"name": "Albireo", "distance": 434.00, "constellation": "Cygnus", "type": "K-type Bright Giant"},
        {"name": "Schedar", "distance": 228.00, "constellation": "Cassiopeia", "type": "K-type Giant"},
        {"name": "Caph", "distance": 54.70, "constellation": "Cassiopeia", "type": "F-type Giant"},
        {"name": "Navi", "distance": 613.00, "constellation": "Cassiopeia", "type": "B-type Main Sequence"},
        {"name": "Ruchbah", "distance": 99.40, "constellation": "Cassiopeia", "type": "A-type Main Sequence"},
        {"name": "Segin", "distance": 442.00, "constellation": "Cassiopeia", "type": "B-type Main Sequence"},
        {"name": "Algol", "distance": 92.80, "constellation": "Perseus", "type": "B-type Main Sequence"},
        {"name": "Mirfak", "distance": 510.00, "constellation": "Perseus", "type": "F-type Supergiant"},
        {"name": "Capella Aa", "distance": 42.92, "constellation": "Auriga", "type": "G-type Giant"},

        # ===== VERY DISTANT STARS (1000+ light-years) =====

        {"name": "Naos", "distance": 1080.00, "constellation": "Puppis", "type": "O-type Supergiant"},
        {"name": "Aspidiske", "distance": 692.00, "constellation": "Carina", "type": "A-type Bright Giant"},
        {"name": "Miaplacidus", "distance": 113.00, "constellation": "Carina", "type": "A-type Main Sequence"},
        {"name": "Turais", "distance": 1090.00, "constellation": "Carina", "type": "F-type Supergiant"},
        {"name": "Acrab", "distance": 404.00, "constellation": "Scorpius", "type": "B-type Main Sequence"},
        {"name": "Dschubba", "distance": 402.00, "constellation": "Scorpius", "type": "B-type Main Sequence"},
        {"name": "Lesath", "distance": 580.00, "constellation": "Scorpius", "type": "B-type Main Sequence"},
        {"name": "Alniyat", "distance": 553.00, "constellation": "Scorpius", "type": "B-type Giant"},
        {"name": "Nunki", "distance": 228.00, "constellation": "Sagittarius", "type": "B-type Main Sequence"},
        {"name": "Ascella", "distance": 88.00, "constellation": "Sagittarius", "type": "A-type Main Sequence"},
        {"name": "Kaus Media", "distance": 306.00, "constellation": "Sagittarius", "type": "K-type Giant"},
        {"name": "Kaus Borealis", "distance": 77.00, "constellation": "Sagittarius", "type": "K-type Giant"},
        {"name": "Rukbat", "distance": 182.00, "constellation": "Sagittarius", "type": "B-type Main Sequence"},
        {"name": "Enif", "distance": 688.00, "constellation": "Pegasus", "type": "K-type Supergiant"},
        {"name": "Scheat", "distance": 196.00, "constellation": "Pegasus", "type": "Red Giant"},
        {"name": "Markab", "distance": 133.00, "constellation": "Pegasus", "type": "B-type Giant"},
        {"name": "Algenib", "distance": 390.00, "constellation": "Pegasus", "type": "B-type Main Sequence"},
        {"name": "Diphda", "distance": 96.30, "constellation": "Cetus", "type": "K-type Giant"},
        {"name": "Menkar", "distance": 249.00, "constellation": "Cetus", "type": "Red Giant"},
        {"name": "Ankaa", "distance": 85.00, "constellation": "Phoenix", "type": "K-type Giant"},

        # ===== ADDITIONAL NOTABLE STARS =====

        {"name": "Zubenelgenubi", "distance": 77.00, "constellation": "Libra", "type": "A-type Main Sequence"},
        {"name": "Zubeneschamali", "distance": 185.00, "constellation": "Libra", "type": "B-type Main Sequence"},
        {"name": "Unukalhai", "distance": 73.90, "constellation": "Serpens", "type": "K-type Giant"},
        {"name": "Rasalhague", "distance": 48.60, "constellation": "Ophiuchus", "type": "A-type Main Sequence"},
        {"name": "Cebalrai", "distance": 82.60, "constellation": "Ophiuchus", "type": "K-type Giant"},
        {"name": "Kornephoros", "distance": 139.00, "constellation": "Hercules", "type": "G-type Bright Giant"},
        {"name": "Rasalgethi", "distance": 359.00, "constellation": "Hercules", "type": "Red Giant"},
        {"name": "Sarin", "distance": 112.00, "constellation": "Hercules", "type": "A-type Main Sequence"},
        {"name": "Sheliak", "distance": 960.00, "constellation": "Lyra", "type": "B-type Main Sequence"},
        {"name": "Sulafat", "distance": 635.00, "constellation": "Lyra", "type": "B-type Bright Giant"},
        {"name": "Alya", "distance": 152.00, "constellation": "Serpens", "type": "A-type Main Sequence"},
        {"name": "Matar", "distance": 206.00, "constellation": "Pegasus", "type": "G-type Bright Giant"},
        {"name": "Sadalsuud", "distance": 612.00, "constellation": "Aquarius", "type": "G-type Supergiant"},
        {"name": "Sadalmelik", "distance": 758.00, "constellation": "Aquarius", "type": "G-type Supergiant"},
        {"name": "Skat", "distance": 160.00, "constellation": "Aquarius", "type": "A-type Main Sequence"},
        {"name": "Deneb Algedi", "distance": 38.70, "constellation": "Capricornus", "type": "A-type Giant"},
        {"name": "Nashira", "distance": 139.00, "constellation": "Capricornus", "type": "A-type Giant"},
        {"name": "Algiedi", "distance": 109.00, "constellation": "Capricornus", "type": "G-type Bright Giant"},
        {"name": "Dabih", "distance": 328.00, "constellation": "Capricornus", "type": "K-type Bright Giant"},
    ]

    return stars

def main():
    """Main execution"""
    print("=" * 60)
    print("Curated Star Database Builder")
    print("=" * 60)
    print()

    # Generate database
    stars = create_comprehensive_star_database()

    # Sort by distance
    stars.sort(key=lambda x: x['distance'])

    # Save to JSON
    output_file = 'stars-database.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stars, f, indent=4, ensure_ascii=False)

    # Calculate statistics
    import os
    file_size = os.path.getsize(output_file)
    min_dist = min(s['distance'] for s in stars)
    max_dist = max(s['distance'] for s in stars)

    print(f"✓ Database created successfully!")
    print(f"✓ Total stars: {len(stars)}")
    print(f"✓ Distance range: {min_dist:.2f} to {max_dist:.2f} light-years")
    print(f"✓ File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"✓ Output file: {output_file}")
    print()

    # Show distance distribution
    ranges = [
        (0, 20, "Very nearby"),
        (20, 50, "Nearby"),
        (50, 100, "Mid-range"),
        (100, 300, "Bright stars"),
        (300, 1000, "Distant bright"),
        (1000, 10000, "Very distant")
    ]

    print("Distance Distribution:")
    for min_r, max_r, label in ranges:
        count = sum(1 for s in stars if min_r <= s['distance'] < max_r)
        if count > 0:
            print(f"  {label:15s} ({min_r:4d}-{max_r:4d} ly): {count:3d} stars")

    print()
    print("=" * 60)
    print("Database build complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
