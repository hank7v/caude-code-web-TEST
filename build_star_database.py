#!/usr/bin/env python3
"""
Star Database Builder
Downloads and processes the HYG (Hipparcos, Yale, Gliese) stellar database
to create a comprehensive JSON database for the Starlight Time Machine app.
"""

import csv
import json
import urllib.request
import sys

# HYG Database URL (v4.2 - includes proper names, distances, spectral types)
# Database moved to Codeberg in 2025
HYG_DATABASE_URL = "https://codeberg.org/astronexus/hyg/raw/branch/main/hyg/v42/hyg_v42.csv"

def spectral_type_to_description(spectral_class):
    """Convert spectral classification to human-readable type"""
    if not spectral_class or spectral_class.strip() == '':
        return "Unknown"

    spec = spectral_class.strip().upper()

    # Main spectral classes
    if spec.startswith('O'):
        return "O-type Main Sequence"
    elif spec.startswith('B'):
        if 'III' in spec or 'II' in spec:
            return "B-type Giant"
        elif 'I' in spec:
            return "B-type Supergiant"
        else:
            return "B-type Main Sequence"
    elif spec.startswith('A'):
        if 'III' in spec or 'II' in spec:
            return "A-type Giant"
        elif 'I' in spec:
            return "A-type Supergiant"
        else:
            return "A-type Main Sequence"
    elif spec.startswith('F'):
        if 'III' in spec or 'II' in spec:
            return "F-type Giant"
        elif 'IV' in spec:
            return "F-type Subgiant"
        elif 'I' in spec:
            return "F-type Supergiant"
        else:
            return "F-type Main Sequence"
    elif spec.startswith('G'):
        if 'III' in spec or 'II' in spec:
            return "G-type Giant"
        elif 'IV' in spec:
            return "G-type Subgiant"
        elif 'I' in spec:
            return "G-type Supergiant"
        else:
            return "G-type Main Sequence"
    elif spec.startswith('K'):
        if 'III' in spec or 'II' in spec:
            return "K-type Giant"
        elif 'IV' in spec:
            return "K-type Subgiant"
        elif 'I' in spec:
            return "K-type Supergiant"
        else:
            return "K-type Main Sequence"
    elif spec.startswith('M'):
        if 'III' in spec or 'II' in spec:
            return "Red Giant"
        elif 'I' in spec:
            return "Red Supergiant"
        else:
            return "Red Dwarf"
    elif spec.startswith('L') or spec.startswith('T') or spec.startswith('Y'):
        return "Brown Dwarf"
    elif spec.startswith('D') or 'D' in spec:
        return "White Dwarf"

    return "Unknown"

def parse_constellation(con):
    """Parse constellation abbreviation to full name"""
    constellation_map = {
        'And': 'Andromeda', 'Ant': 'Antlia', 'Aps': 'Apus', 'Aql': 'Aquila',
        'Aqr': 'Aquarius', 'Ara': 'Ara', 'Ari': 'Aries', 'Aur': 'Auriga',
        'Boo': 'Boötes', 'Cae': 'Caelum', 'Cam': 'Camelopardalis', 'Cap': 'Capricornus',
        'Car': 'Carina', 'Cas': 'Cassiopeia', 'Cen': 'Centaurus', 'Cep': 'Cepheus',
        'Cet': 'Cetus', 'Cha': 'Chamaeleon', 'Cir': 'Circinus', 'CMa': 'Canis Major',
        'CMi': 'Canis Minor', 'Cnc': 'Cancer', 'Col': 'Columba', 'Com': 'Coma Berenices',
        'CrA': 'Corona Australis', 'CrB': 'Corona Borealis', 'Crt': 'Crater', 'Cru': 'Crux',
        'Crv': 'Corvus', 'CVn': 'Canes Venatici', 'Cyg': 'Cygnus', 'Del': 'Delphinus',
        'Dor': 'Dorado', 'Dra': 'Draco', 'Equ': 'Equuleus', 'Eri': 'Eridanus',
        'For': 'Fornax', 'Gem': 'Gemini', 'Gru': 'Grus', 'Her': 'Hercules',
        'Hor': 'Horologium', 'Hya': 'Hydra', 'Hyi': 'Hydrus', 'Ind': 'Indus',
        'Lac': 'Lacerta', 'Leo': 'Leo', 'Lep': 'Lepus', 'Lib': 'Libra',
        'LMi': 'Leo Minor', 'Lup': 'Lupus', 'Lyn': 'Lynx', 'Lyr': 'Lyra',
        'Men': 'Mensa', 'Mic': 'Microscopium', 'Mon': 'Monoceros', 'Mus': 'Musca',
        'Nor': 'Norma', 'Oct': 'Octans', 'Oph': 'Ophiuchus', 'Ori': 'Orion',
        'Pav': 'Pavo', 'Peg': 'Pegasus', 'Per': 'Perseus', 'Phe': 'Phoenix',
        'Pic': 'Pictor', 'PsA': 'Piscis Austrinus', 'Psc': 'Pisces', 'Pup': 'Puppis',
        'Pyx': 'Pyxis', 'Ret': 'Reticulum', 'Scl': 'Sculptor', 'Sco': 'Scorpius',
        'Sct': 'Scutum', 'Ser': 'Serpens', 'Sex': 'Sextans', 'Sge': 'Sagitta',
        'Sgr': 'Sagittarius', 'Tau': 'Taurus', 'Tel': 'Telescopium', 'TrA': 'Triangulum Australe',
        'Tri': 'Triangulum', 'Tuc': 'Tucana', 'UMa': 'Ursa Major', 'UMi': 'Ursa Minor',
        'Vel': 'Vela', 'Vir': 'Virgo', 'Vol': 'Volans', 'Vul': 'Vulpecula'
    }
    return constellation_map.get(con, con) if con else "Unknown"

def download_hyg_database():
    """Download the HYG database"""
    print(f"Downloading HYG database from {HYG_DATABASE_URL}...")
    try:
        with urllib.request.urlopen(HYG_DATABASE_URL) as response:
            content = response.read().decode('utf-8')
        print("Download complete!")
        return content
    except Exception as e:
        print(f"Error downloading database: {e}")
        sys.exit(1)

def process_hyg_data(csv_content):
    """Process HYG CSV data and extract relevant stars"""
    print("Processing star data...")

    stars = []
    reader = csv.DictReader(csv_content.splitlines())

    for row in reader:
        # Get proper name (if available)
        proper_name = row.get('proper', '').strip()

        # Skip stars without proper names for main database
        # (We want named stars for better user experience)
        if not proper_name:
            continue

        # Get distance (convert parsecs to light-years)
        try:
            distance_parsecs = float(row.get('dist', 0))
            if distance_parsecs <= 0:
                continue
            distance_ly = distance_parsecs * 3.26156  # Convert parsecs to light-years

            # Filter: Include stars up to 5000 light-years for reasonable range
            if distance_ly > 5000:
                continue

        except (ValueError, TypeError):
            continue

        # Get constellation
        constellation = parse_constellation(row.get('con', ''))

        # Get spectral type and convert to description
        spectral = row.get('spect', '')
        star_type = spectral_type_to_description(spectral)

        # Create star entry
        star = {
            "name": proper_name,
            "distance": round(distance_ly, 2),
            "constellation": constellation,
            "type": star_type
        }

        stars.append(star)

    # Sort by distance
    stars.sort(key=lambda x: x['distance'])

    # Remove duplicates (some stars might have multiple entries)
    unique_stars = []
    seen_names = set()
    for star in stars:
        if star['name'] not in seen_names:
            unique_stars.append(star)
            seen_names.add(star['name'])

    print(f"Processed {len(unique_stars)} unique named stars")
    return unique_stars

def save_to_json(stars, filename='stars-database.json'):
    """Save stars to JSON file"""
    print(f"Saving to {filename}...")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(stars, f, indent=4, ensure_ascii=False)

    # Calculate file size
    import os
    file_size = os.path.getsize(filename)
    print(f"Database saved! File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"Total stars in database: {len(stars)}")

    # Show distance range
    if stars:
        min_dist = min(s['distance'] for s in stars)
        max_dist = max(s['distance'] for s in stars)
        print(f"Distance range: {min_dist:.2f} to {max_dist:.2f} light-years")

def main():
    """Main execution"""
    print("=" * 60)
    print("Star Database Builder for Starlight Time Machine")
    print("=" * 60)
    print()

    # Download database
    csv_content = download_hyg_database()

    # Process data
    stars = process_hyg_data(csv_content)

    if not stars:
        print("Error: No stars were processed!")
        sys.exit(1)

    # Save to JSON
    save_to_json(stars)

    print()
    print("=" * 60)
    print("Database build complete!")
    print("=" * 60)

    # Show some sample stars
    print("\nSample stars from database:")
    for star in stars[:5]:
        print(f"  - {star['name']}: {star['distance']} ly ({star['constellation']}, {star['type']})")

    if len(stars) > 5:
        print(f"  ... and {len(stars) - 5} more stars")

if __name__ == "__main__":
    main()
