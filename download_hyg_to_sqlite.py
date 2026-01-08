#!/usr/bin/env python3
"""
Download and convert HYG stellar database to SQLite
Optimized for minimal memory usage and no content output
"""

import csv
import sqlite3
import urllib.request
import sys
import os

# HYG Database URL (v4.2)
HYG_DATABASE_URL = "https://codeberg.org/astronexus/hyg/raw/branch/main/hyg/v42/hyg_v42.csv"

# Alternative URLs if primary fails
ALTERNATIVE_URLS = [
    "https://github.com/astronexus/HYG-Database/raw/main/hyg/v4/hyg_v42.csv",
    "http://www.astronexus.com/files/downloads/hygdata_v42.csv"
]

def download_file(url, output_path="hyg_temp.csv"):
    """Download file with progress indication"""
    print(f"Downloading from: {url}")
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            total_size = response.headers.get('content-length')
            if total_size:
                total_size = int(total_size)
                print(f"File size: {total_size / 1024 / 1024:.2f} MB")

            with open(output_path, 'wb') as f:
                downloaded = 0
                chunk_size = 8192
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}%", end='', flush=True)

        print(f"\n✓ Download complete: {output_path}")
        return True
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        return False

def create_sqlite_database(csv_path, db_path="stars.db"):
    """Convert CSV to SQLite database (streaming, no memory loading)"""
    print(f"\nCreating SQLite database: {db_path}")

    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table with coordinates for constellation drawing
    cursor.execute('''
        CREATE TABLE stars (
            id INTEGER PRIMARY KEY,
            hip INTEGER,
            ra REAL NOT NULL,
            dec REAL NOT NULL,
            distance REAL NOT NULL,
            mag REAL,
            absmag REAL,
            proper_name TEXT,
            bayer TEXT,
            flam TEXT,
            spect TEXT,
            constellation TEXT
        )
    ''')

    # Create indexes for fast queries
    cursor.execute('CREATE INDEX idx_distance ON stars(distance)')
    cursor.execute('CREATE INDEX idx_ra_dec ON stars(ra, dec)')

    print("Processing CSV (streaming mode)...")

    # Process CSV line by line (streaming)
    # Note: HYG CSV uses semicolons as delimiters
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')

        batch = []
        batch_size = 1000
        total_processed = 0
        total_inserted = 0

        for row in reader:
            total_processed += 1

            # Extract distance (already in parsecs, convert to light-years)
            try:
                dist_parsecs = float(row.get('Distance', 0))
                if dist_parsecs <= 0:
                    continue  # Skip stars without distance

                distance_ly = dist_parsecs * 3.26156

                # Filter: Only stars within 5000 light-years (manageable dataset)
                if distance_ly > 5000:
                    continue

            except (ValueError, TypeError):
                continue

            # Extract other fields - use exact column names from CSV
            try:
                hip_str = row.get('Hipparcos cat. ID', '').strip()
                hip = int(hip_str) if hip_str else None
                ra = float(row.get('RA', 0))
                dec = float(row.get('Dec', 0))

                mag_str = row.get('Magnitude', '').strip()
                mag = float(mag_str) if mag_str else 99

                absmag_str = row.get('Absolute magnitude', '').strip()
                absmag = float(absmag_str) if absmag_str else 99

                proper = row.get('Proper', '').strip()
                bayer = row.get('Bayer / Flamsteed designation', '').strip()
                flam = row.get('Flamsteed number', '').strip()
                spect = row.get('Spectral type', '').strip()
                con = row.get('Constellation abbreviation', '').strip()

            except (ValueError, TypeError):
                continue

            # Add to batch
            batch.append((hip, ra, dec, distance_ly, mag, absmag, proper, bayer, flam, spect, con))

            # Insert batch when it reaches batch_size
            if len(batch) >= batch_size:
                cursor.executemany('''
                    INSERT INTO stars (hip, ra, dec, distance, mag, absmag, proper_name, bayer, flam, spect, constellation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', batch)
                total_inserted += len(batch)
                batch = []

                # Progress update
                if total_inserted % 10000 == 0:
                    print(f"  Inserted {total_inserted:,} stars...", flush=True)

        # Insert remaining batch
        if batch:
            cursor.executemany('''
                INSERT INTO stars (hip, ra, dec, distance, mag, absmag, proper_name, bayer, flam, spect, constellation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', batch)
            total_inserted += len(batch)

    conn.commit()
    conn.close()

    print(f"\n✓ Database created successfully!")
    print(f"  Total rows processed: {total_processed:,}")
    print(f"  Total stars inserted: {total_inserted:,}")

    # Get file size
    db_size = os.path.getsize(db_path)
    print(f"  Database size: {db_size / 1024 / 1024:.2f} MB")

    return total_inserted

def verify_database(db_path="stars.db"):
    """Quick verification of database"""
    print(f"\nVerifying database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Count total stars
    cursor.execute('SELECT COUNT(*) FROM stars')
    total = cursor.fetchone()[0]
    print(f"  Total stars: {total:,}")

    # Count named stars
    cursor.execute("SELECT COUNT(*) FROM stars WHERE proper_name != ''")
    named = cursor.fetchone()[0]
    print(f"  Named stars: {named:,}")

    # Distance range
    cursor.execute('SELECT MIN(distance), MAX(distance) FROM stars')
    min_dist, max_dist = cursor.fetchone()
    print(f"  Distance range: {min_dist:.2f} to {max_dist:.2f} light-years")

    # Sample query: stars around 10 light-years
    cursor.execute('SELECT COUNT(*) FROM stars WHERE distance BETWEEN 9.9 AND 10.1')
    sample_count = cursor.fetchone()[0]
    print(f"  Sample (9.9-10.1 ly): {sample_count} stars")

    conn.close()

def main():
    print("=" * 70)
    print("HYG Database to SQLite Converter")
    print("=" * 70)
    print()

    csv_file = "hyg_temp.csv"
    db_file = "stars.db"
    cleanup_csv = True  # Whether to delete CSV after conversion

    # Check if CSV file path provided as argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        if not os.path.exists(csv_file):
            print(f"✗ Error: File not found: {csv_file}")
            sys.exit(1)
        print(f"Using existing CSV file: {csv_file}")
        cleanup_csv = False  # Don't delete user's file
    else:
        # Try downloading from primary URL
        success = download_file(HYG_DATABASE_URL, csv_file)

        # Try alternatives if primary fails
        if not success:
            print("\nTrying alternative URLs...")
            for alt_url in ALTERNATIVE_URLS:
                success = download_file(alt_url, csv_file)
                if success:
                    break

        if not success:
            print("\n✗ All download attempts failed!")
            print("Please manually download from: https://www.astronexus.com/hyg")
            print("Then run: python3 download_hyg_to_sqlite.py /path/to/hyg_v42.csv")
            sys.exit(1)

    # Convert to SQLite
    try:
        total_stars = create_sqlite_database(csv_file, db_file)

        # Verify
        verify_database(db_file)

        # Cleanup CSV only if it was downloaded (not user's file)
        if cleanup_csv:
            print(f"\nCleaning up temporary file: {csv_file}")
            os.remove(csv_file)
        else:
            print(f"\nKeeping original CSV file: {csv_file}")

        print("\n" + "=" * 70)
        print("✓ SUCCESS!")
        print(f"Database ready: {db_file}")
        print("=" * 70)

    except Exception as e:
        print(f"\n✗ Error creating database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
