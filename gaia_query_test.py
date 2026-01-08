#!/usr/bin/env python3
"""
Gaia DR3 Star Density Test
Queries Gaia Archive to check how many stars are available at different distances.

Distance conversion:
- Gaia provides parallax in milliarcseconds (mas)
- Distance (parsecs) = 1000 / parallax (mas)
- Distance (light-years) = distance (parsecs) * 3.26156

For 100 light-years = 30.66 parsecs = parallax of 32.6 mas
For 10 light-years = 3.066 parsecs = parallax of 326 mas
"""

import requests
import time

# Gaia TAP endpoint
GAIA_TAP_URL = "https://gea.esac.esa.int/tap-server/tap/sync"

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
            response = requests.get(GAIA_TAP_URL, params=params, timeout=120)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"  Error: {e}")
            if attempt < max_retries - 1:
                print("  Retrying in 5 seconds...")
                time.sleep(5)
            else:
                raise
    return None

def parallax_to_lightyears(parallax_mas):
    """Convert parallax in milliarcseconds to light-years"""
    if parallax_mas <= 0:
        return float('inf')
    distance_parsecs = 1000.0 / parallax_mas
    return distance_parsecs * 3.26156

def lightyears_to_parallax(lightyears):
    """Convert light-years to parallax in milliarcseconds"""
    distance_parsecs = lightyears / 3.26156
    return 1000.0 / distance_parsecs

def check_star_density():
    """Check star density at various distance ranges"""
    print("=" * 70)
    print("Gaia DR3 Star Density Analysis")
    print("=" * 70)
    print()

    # Distance ranges to check (in light-years)
    ranges = [
        (0, 10),
        (10, 20),
        (20, 30),
        (30, 40),
        (40, 50),
        (50, 60),
        (60, 70),
        (70, 80),
        (80, 90),
        (90, 100),
    ]

    total_stars = 0
    results = []

    for min_ly, max_ly in ranges:
        # Convert to parallax (note: larger parallax = closer star)
        min_parallax = lightyears_to_parallax(max_ly)  # farther = smaller parallax
        max_parallax = lightyears_to_parallax(min_ly) if min_ly > 0 else 10000  # closer = larger parallax

        # ADQL query to count stars in this range
        # Using parallax > 0 and parallax_over_error > 5 for reliable distances
        query = f"""
        SELECT COUNT(*) as star_count
        FROM gaiadr3.gaia_source
        WHERE parallax >= {min_parallax}
          AND parallax < {max_parallax}
          AND parallax_over_error > 5
        """

        print(f"Checking {min_ly}-{max_ly} light-years (parallax {min_parallax:.2f}-{max_parallax:.2f} mas)...")

        try:
            result = query_gaia(query)
            if result and 'data' in result and len(result['data']) > 0:
                count = result['data'][0][0]
                results.append((min_ly, max_ly, count))
                total_stars += count
                print(f"  Found: {count:,} stars")
            else:
                print(f"  No data returned")
                results.append((min_ly, max_ly, 0))
        except Exception as e:
            print(f"  Error: {e}")
            results.append((min_ly, max_ly, -1))

        # Small delay to be nice to the server
        time.sleep(1)

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY: Stars within 100 light-years (Gaia DR3)")
    print("=" * 70)
    print()
    print(f"{'Distance Range':<20} {'Star Count':<15} {'Cumulative':<15}")
    print("-" * 50)

    cumulative = 0
    for min_ly, max_ly, count in results:
        if count >= 0:
            cumulative += count
            print(f"{min_ly:>3}-{max_ly:<3} light-years {count:>12,} {cumulative:>12,}")
        else:
            print(f"{min_ly:>3}-{max_ly:<3} light-years {'ERROR':>12} {'-':>12}")

    print("-" * 50)
    print(f"{'TOTAL':<20} {total_stars:>12,}")
    print()

    # Analysis for the app
    print("=" * 70)
    print("ANALYSIS FOR STARLIGHT TIME MACHINE")
    print("=" * 70)
    print()

    if total_stars > 0:
        avg_per_ly = total_stars / 100
        print(f"Average stars per light-year: {avg_per_ly:,.1f}")
        print(f"Stars per day (1/365.25 ly): {avg_per_ly / 365.25:,.2f}")
        print()

        if avg_per_ly > 1000:
            print("✓ EXCELLENT! Plenty of stars for day-precision matching!")
        elif avg_per_ly > 100:
            print("✓ GOOD! Should work well for most date ranges.")
        else:
            print("⚠ LIMITED. May need to increase tolerance for matching.")

    return results, total_stars

if __name__ == "__main__":
    try:
        results, total = check_star_density()
    except Exception as e:
        print(f"Error: {e}")
        print("\nIf the query times out, the Gaia Archive may be busy.")
        print("Try again later or use a local database approach.")
