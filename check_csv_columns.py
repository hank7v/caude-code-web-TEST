#!/usr/bin/env python3
"""
Quick diagnostic to check CSV column names and sample data
"""
import csv
import sys

def check_csv(csv_path):
    print("=" * 70)
    print("CSV Column Inspector")
    print("=" * 70)
    print()

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Get column names
        columns = reader.fieldnames
        print(f"Total columns: {len(columns)}")
        print()
        print("Column names:")
        for i, col in enumerate(columns, 1):
            print(f"  {i:2d}. {col}")

        print()
        print("=" * 70)
        print("First 3 rows of data:")
        print("=" * 70)

        for idx, row in enumerate(reader):
            if idx >= 3:
                break
            print(f"\nRow {idx + 1}:")
            # Show key fields we care about
            for key in ['id', 'hip', 'proper', 'ra', 'dec', 'dist', 'distance',
                       'mag', 'absmag', 'spect', 'con', 'constellation']:
                if key in row:
                    value = row[key]
                    if len(value) > 50:
                        value = value[:50] + "..."
                    print(f"  {key:15s}: {value}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_csv.py /path/to/file.csv")
        sys.exit(1)

    csv_path = sys.argv[1]
    check_csv(csv_path)
