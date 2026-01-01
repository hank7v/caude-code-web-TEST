# Android Development Setup Guide

## Using Termux for Git & Development

### 1. Install Termux

**Recommended:** Install from **F-Droid** (more up-to-date than Play Store)
- Download F-Droid: https://f-droid.org/
- Search for "Termux" and install

**Alternative:** Google Play (older version, but works)

### 2. Initial Setup

```bash
# Update package lists
pkg update && pkg upgrade -y

# Install essential tools
pkg install git python openssh

# Configure git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Generate SSH key (optional, for GitHub authentication)
ssh-keygen -t ed25519 -C "your.email@example.com"
```

### 3. Clone Your Repository

```bash
# Navigate to storage (access your phone files)
termux-setup-storage
cd ~/storage/shared/Documents  # or another folder

# Clone your repo
git clone https://github.com/hank7v/caude-code-web-TEST.git
cd caude-code-web-TEST
```

### 4. Download & Process HYG Database

```bash
# Make sure you're in the project directory
cd ~/storage/shared/Documents/caude-code-web-TEST

# Run the download script
python3 download_hyg_to_sqlite.py
```

**Expected output:**
- Download: ~14MB CSV file
- Process: ~2-3 minutes
- Result: `stars.db` file (~5-15MB)

### 5. Add Database to Git

```bash
# Check file size
ls -lh stars.db

# If under 100MB (should be ~5-15MB):
git add stars.db
git commit -m "Add HYG stellar database with RA/Dec coordinates"
git push

# If you get authentication error, use token:
# Settings → Developer settings → Personal access tokens → Generate new token
# Use token as password when prompted
```

### 6. GitHub File Size Limits

| Method | Limit | Notes |
|--------|-------|-------|
| Web upload | 25MB | ❌ Won't work for stars.db |
| Git CLI | 100MB | ✅ Perfect for our database |
| Git LFS | Unlimited* | Only if needed (not required) |

### 7. Useful Termux Tips

**Access phone storage:**
```bash
termux-setup-storage
cd ~/storage/shared  # Your phone's internal storage
```

**Install Python packages:**
```bash
pip install requests pandas numpy
```

**Keep Termux running (prevent Android from killing it):**
- Settings → Battery → Termux → Don't optimize

**Text editor in Termux:**
```bash
pkg install nano
nano filename.txt
```

**File transfer between phone and Termux:**
```bash
# Termux can access ~/storage/shared
# That's your phone's regular storage
cp ~/storage/shared/Downloads/file.txt ./
```

## Next Steps After Database Setup

Once you have `stars.db` uploaded:

1. **Integrate sql.js** - JavaScript SQLite library for web
2. **Build constellation generator** - Query stars at exact distance
3. **Create visualization** - Draw custom constellations with Canvas/SVG
4. **Add interactivity** - Zoom, pan, rotate constellation view

---

## Database Schema

The `stars.db` SQLite database contains:

```sql
CREATE TABLE stars (
    id INTEGER PRIMARY KEY,
    hip INTEGER,              -- Hipparcos catalog number
    ra REAL NOT NULL,         -- Right Ascension (0-24 hours)
    dec REAL NOT NULL,        -- Declination (-90 to +90 degrees)
    distance REAL NOT NULL,   -- Distance in light-years
    mag REAL,                 -- Apparent magnitude (brightness)
    absmag REAL,              -- Absolute magnitude
    proper_name TEXT,         -- Common name (e.g., "Sirius")
    bayer TEXT,               -- Bayer designation (e.g., "α CMa")
    flam TEXT,                -- Flamsteed number
    spect TEXT,               -- Spectral type
    constellation TEXT        -- Constellation abbreviation
);

-- Indexes for fast queries
CREATE INDEX idx_distance ON stars(distance);
CREATE INDEX idx_ra_dec ON stars(ra, dec);
```

**Example Query (for constellation generation):**
```sql
-- Find all stars at 10.5 light-years (±0.003 for day precision)
SELECT ra, dec, mag, proper_name
FROM stars
WHERE distance BETWEEN 10.497 AND 10.503
ORDER BY mag ASC;
```

## Troubleshooting

**"Permission denied" errors:**
```bash
termux-setup-storage
# Accept storage permission in Android popup
```

**Git push fails with "403 Forbidden":**
```bash
# Use personal access token instead of password
# GitHub.com → Settings → Developer settings → PAT
```

**Python import errors:**
```bash
pip install --upgrade pip
pip install module-name
```

**Database file too large:**
```bash
# Check actual size
ls -lh stars.db

# If >100MB, we can optimize by reducing distance limit
# Edit download_hyg_to_sqlite.py and change:
# if distance_ly > 5000:  # Change to 1000 or 2000
```

---

**Need help?** Create an issue in the repo or ask Claude Code!
