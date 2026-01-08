#!/usr/bin/env python3
"""
Gaia DR3 Star Data Downloader

Downloads stars from Gaia DR3 archive with good parallax measurements,
converts to light-years distance, and saves to SQLite database.

Gaia DR3 provides:
- source_id: Unique identifier
- ra, dec: Coordinates in degrees
- parallax: Parallax in milliarcseconds (mas)
- parallax_error: Parallax uncertainty
- phot_g_mean_mag: G-band magnitude
- bp_rp: Blue-Red color index (for spectral classification)

Distance conversion:
- Distance (parsecs) = 1000 / parallax (mas)
- Distance (light-years) = distance (parsecs) * 3.26156
"""

import requests
import sqlite3
import time
import json
import sys

# Gaia TAP endpoint
GAIA_TAP_URL = "https://gea.esac.esa.int/tap-server/tap/sync"

def lightyears_to_parallax(lightyears):
    """Convert light-years to parallax in milliarcseconds"""
    distance_parsecs = lightyears / 3.26156
    return 1000.0 / distance_parsecs

def parallax_to_lightyears(parallax_mas):
    """Convert parallax in milliarcseconds to light-years"""
    if parallax_mas <= 0:
        return float('inf')
    distance_parsecs = 1000.0 / parallax_mas
    return distance_parsecs * 3.26156

def bp_rp_to_spectral_type(bp_rp):
    """
    Estimate spectral type from Gaia BP-RP color index.
    BP-RP ranges roughly:
    - O/B stars: < 0.0 (blue)
    - A stars: 0.0 to 0.3
    - F stars: 0.3 to 0.6
    - G stars: 0.6 to 0.9
    - K stars: 0.9 to 1.4
    - M stars: > 1.4 (red)
    """
    if bp_rp is None:
        return None
    if bp_rp < -0.1:
        return 'O'
    elif bp_rp < 0.0:
        return 'B'
    elif bp_rp < 0.3:
        return 'A'
    elif bp_rp < 0.6:
        return 'F'
    elif bp_rp < 0.9:
        return 'G'
    elif bp_rp < 1.4:
        return 'K'
    else:
        return 'M'

def query_gaia(adql_query, max_retries=3):
    """Execute an ADQL query against Gaia Archive"""
    params = {
        'REQUEST': 'doQuery',
        'LANG': 'ADQL',
        'FORMAT': 'json',
        'QUERY': adql_query
    }

    for attempt in range(max_retries):
        try:
            print(f"  Querying Gaia Archive (attempt {attempt + 1})...")
            response = requests.get(GAIA_TAP_URL, params=params, timeout=300)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"  Error: {e}")
            if attempt < max_retries - 1:
                wait_time = 10 * (attempt + 1)
                print(f"  Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
    return None

def download_gaia_stars(max_distance_ly=100, min_parallax_snr=5):
    """
    Download stars from Gaia DR3 within specified distance.

    Args:
        max_distance_ly: Maximum distance in light-years
        min_parallax_snr: Minimum parallax signal-to-noise ratio for reliability

    Returns:
        List of star dictionaries
    """
    # Calculate minimum parallax for the max distance
    min_parallax = lightyears_to_parallax(max_distance_ly)

    print(f"Downloading Gaia DR3 stars within {max_distance_ly} light-years")
    print(f"Minimum parallax: {min_parallax:.2f} mas")
    print(f"Minimum parallax S/N: {min_parallax_snr}")
    print()

    # ADQL query to get stars with reliable distances
    # We limit the fields to minimize data transfer
    query = f"""
    SELECT
        source_id,
        ra,
        dec,
        parallax,
        parallax_error,
        phot_g_mean_mag,
        bp_rp,
        radial_velocity
    FROM gaiadr3.gaia_source
    WHERE parallax >= {min_parallax}
      AND parallax_over_error >= {min_parallax_snr}
      AND parallax > 0
    ORDER BY parallax DESC
    """

    print("Executing query...")
    result = query_gaia(query)

    if not result or 'data' not in result:
        print("No data returned from Gaia")
        return []

    metadata = result.get('metadata', [])
    data = result.get('data', [])

    print(f"Received {len(data):,} stars from Gaia DR3")

    # Parse the results
    stars = []
    for row in data:
        source_id, ra, dec, parallax, parallax_error, g_mag, bp_rp, rv = row

        # Convert parallax to distance in light-years
        distance_ly = parallax_to_lightyears(parallax)

        # Estimate spectral type from color
        spect = bp_rp_to_spectral_type(bp_rp)

        stars.append({
            'gaia_id': source_id,
            'ra': ra,
            'dec': dec,
            'distance': distance_ly,
            'parallax': parallax,
            'parallax_error': parallax_error,
            'mag': g_mag,
            'bp_rp': bp_rp,
            'spect': spect,
            'radial_velocity': rv
        })

    return stars

def create_gaia_database(stars, output_file='gaia_stars.db'):
    """
    Create SQLite database from downloaded Gaia stars.

    The schema is compatible with the existing stars.db format.
    """
    print(f"\nCreating SQLite database: {output_file}")

    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()

    # Create table with same schema as existing database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stars (
            id INTEGER PRIMARY KEY,
            gaia_id INTEGER UNIQUE,
            hip INTEGER,
            ra REAL,
            dec REAL,
            distance REAL,
            parallax REAL,
            mag REAL,
            absmag REAL,
            proper_name TEXT,
            bayer TEXT,
            flam TEXT,
            spect TEXT,
            constellation TEXT
        )
    ''')

    # Create index on distance for fast queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_distance ON stars(distance)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_gaia_id ON stars(gaia_id)')

    # Insert stars
    for star in stars:
        # Calculate absolute magnitude if we have apparent magnitude
        absmag = None
        if star['mag'] is not None and star['distance'] > 0:
            # M = m - 5 * (log10(d) - 1), where d is in parsecs
            distance_pc = star['distance'] / 3.26156
            absmag = star['mag'] - 5 * (3.141592653589793 * (distance_pc / 10))  # Simplified

        cursor.execute('''
            INSERT OR REPLACE INTO stars
            (gaia_id, ra, dec, distance, parallax, mag, absmag, spect)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            star['gaia_id'],
            star['ra'],
            star['dec'],
            star['distance'],
            star['parallax'],
            star['mag'],
            absmag,
            star['spect']
        ))

    conn.commit()

    # Verify
    cursor.execute('SELECT COUNT(*) FROM stars')
    count = cursor.fetchone()[0]
    print(f"Database created with {count:,} stars")

    # Show distance distribution
    print("\nDistance distribution:")
    ranges = [(0, 10), (10, 20), (20, 30), (30, 50), (50, 100)]
    for min_d, max_d in ranges:
        cursor.execute(
            'SELECT COUNT(*) FROM stars WHERE distance >= ? AND distance < ?',
            (min_d, max_d)
        )
        c = cursor.fetchone()[0]
        print(f"  {min_d:3}-{max_d:3} ly: {c:,} stars")

    conn.close()
    return output_file

def merge_with_existing(gaia_db='gaia_stars.db', existing_db='stars.db', output_db='stars_merged.db'):
    """
    Merge Gaia stars with existing HYG database.
    Prioritizes existing named stars, adds Gaia stars that don't overlap.
    """
    import shutil

    print(f"\nMerging {gaia_db} with {existing_db}")

    # Copy existing database
    shutil.copy(existing_db, output_db)

    conn = sqlite3.connect(output_db)
    cursor = conn.cursor()

    # Attach Gaia database
    cursor.execute(f"ATTACH DATABASE '{gaia_db}' AS gaia")

    # Get count before
    cursor.execute('SELECT COUNT(*) FROM stars')
    before = cursor.fetchone()[0]

    # Add gaia_id column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE stars ADD COLUMN gaia_id INTEGER')
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Add parallax column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE stars ADD COLUMN parallax REAL')
    except sqlite3.OperationalError:
        pass

    # Insert Gaia stars that don't overlap with existing
    # We consider stars at very similar positions (within 0.01 degrees) as duplicates
    cursor.execute('''
        INSERT INTO stars (gaia_id, ra, dec, distance, parallax, mag, spect)
        SELECT g.gaia_id, g.ra, g.dec, g.distance, g.parallax, g.mag, g.spect
        FROM gaia.stars g
        WHERE NOT EXISTS (
            SELECT 1 FROM stars s
            WHERE ABS(s.ra - g.ra) < 0.01
            AND ABS(s.dec - g.dec) < 0.01
        )
    ''')

    inserted = cursor.rowcount
    print(f"Inserted {inserted:,} new Gaia stars")

    conn.commit()

    # Get count after
    cursor.execute('SELECT COUNT(*) FROM stars')
    after = cursor.fetchone()[0]

    print(f"Total stars: {before:,} -> {after:,}")

    # Show new distance distribution within 100 ly
    print("\nStars within 100 light-years:")
    cursor.execute('SELECT COUNT(*) FROM stars WHERE distance <= 100')
    print(f"  Total: {cursor.fetchone()[0]:,}")

    cursor.execute("DETACH DATABASE gaia")
    conn.close()

    return output_db

def main():
    print("=" * 70)
    print("Gaia DR3 Star Downloader for Starlight Time Machine")
    print("=" * 70)
    print()

    # Check if we have requests module
    try:
        import requests
    except ImportError:
        print("Error: 'requests' module not found.")
        print("Install with: pip install requests")
        sys.exit(1)

    # Download options
    max_distance = 100  # light-years
    min_snr = 5  # minimum parallax signal-to-noise

    if len(sys.argv) > 1:
        max_distance = float(sys.argv[1])

    print(f"Configuration:")
    print(f"  Max distance: {max_distance} light-years")
    print(f"  Min parallax S/N: {min_snr}")
    print()

    # Download from Gaia
    try:
        stars = download_gaia_stars(max_distance, min_snr)
    except Exception as e:
        print(f"Error downloading from Gaia: {e}")
        print("\nNote: The Gaia archive may be temporarily unavailable.")
        print("Try again later or check https://gea.esac.esa.int/archive/")
        sys.exit(1)

    if not stars:
        print("No stars downloaded. Exiting.")
        sys.exit(1)

    # Create Gaia database
    gaia_db = create_gaia_database(stars)

    # Merge with existing database
    import os
    if os.path.exists('stars.db'):
        merged_db = merge_with_existing(gaia_db, 'stars.db', 'stars_new.db')
        print(f"\nMerged database saved to: {merged_db}")
        print("\nTo use the new database:")
        print("  mv stars.db stars_old.db")
        print("  mv stars_new.db stars.db")
    else:
        print(f"\nGaia database saved to: {gaia_db}")
        print("Rename to stars.db to use with the app.")

    print()
    print("Done!")

if __name__ == "__main__":
    main()
