# ✨ Starlight Time Machine

A beautiful web application that finds stars whose light has been traveling for exactly the duration between two meaningful dates in your life.

## 🌟 Concept

Have you ever wondered which star's light started its journey on your wedding day and is arriving on Earth today? Or which star's light has been traveling since you were born? This application answers those questions!

When you look at a star, you're seeing it as it was in the past. The light takes years to reach us. This app calculates the distance light travels between two dates and finds real stars at that exact distance.

## 🚀 Features

- **Precise Date Calculations**: Calculate the exact number of days between two dates
- **Light-Year Conversion**: Convert days to light-years with day-level precision (days ÷ 365.25)
- **Real Star Database**: 40+ real stars from our astronomical neighborhood and beyond
- **Smart Matching**: Finds stars within a 5% tolerance range for the best matches
- **Beautiful UI**: Space-themed interface with smooth animations
- **Detailed Information**: Shows star names, distances, constellations, and types

## 📋 How It Works

1. **Input Two Dates**:
   - Start Date: When the light began its journey (e.g., your wedding day)
   - End Date: When the light arrives on Earth (e.g., today)

2. **Calculate Distance**:
   - Days between dates = (End Date - Start Date)
   - Light-years = Days ÷ 365.25

3. **Find Matching Stars**:
   - Searches the astronomy database for stars at the calculated distance
   - Uses ±5% tolerance to find near matches
   - Sorts by closest match

4. **View Results**:
   - See star name, exact distance, constellation, and type
   - View precision (how close the match is in days)

## 🎯 Example Usage

**Example 1: 10 Years Ago to Today**
- Days: ~3,652 days
- Light-years: ~10.00 light-years
- Matching Stars: Epsilon Eridani, Ross 248, Lacaille 9352

**Example 2: Wedding Anniversary**
- If you got married 25 years ago:
- Days: ~9,131 days
- Light-years: ~25.00 light-years
- Matching Stars: Vega, Fomalhaut

**Example 3: Your Birthday**
- If you're 36 years old:
- Days: ~13,149 days
- Light-years: ~36.00 light-years
- Matching Star: Arcturus

## 🗂️ Project Structure

```
starlight-time-machine/
├── index.html              # Main HTML structure
├── styles.css              # Beautiful space-themed styling
├── app.js                  # Core application logic
├── stars-database.json     # 40+ real stars with distances
└── README.md              # This file
```

## 🔧 Technical Details

### Date Calculation Service
- Calculates milliseconds between dates
- Converts to days with high precision
- Uses 365.25 days per year (accounting for leap years)

### Star Finder Service
- Searches database with configurable tolerance (default 5%)
- Sorts results by closest match
- Calculates precision difference in days

### Star Database
- Contains 40+ real stars
- Distances range from 4.2 light-years (Proxima Centauri) to 2,615 light-years (Deneb)
- Includes star name, distance, constellation, and spectral type

## 🌌 Stars in Database

Our database includes famous stars like:
- **Nearby Stars**: Proxima Centauri (4.2 ly), Sirius (8.6 ly), Tau Ceti (11.9 ly)
- **Bright Stars**: Vega (25 ly), Arcturus (36.7 ly), Altair (16.7 ly)
- **Giants**: Betelgeuse (548 ly), Antares (550 ly), Rigel (860 ly)
- **Distant Stars**: Deneb (2,615 ly), Alnilam (1,342 ly)

## 🚀 Getting Started

1. Simply open `index.html` in a web browser
2. Select your start and end dates
3. Click "Find My Star"
4. Discover which star's light has been traveling during your special time period!

## 🎨 Features Highlights

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Default Values**: Pre-filled with 10 years ago to today
- **Keyboard Support**: Press Enter to calculate
- **Error Handling**: Validates dates and shows helpful messages
- **Visual Feedback**: Smooth animations and hover effects

## 📊 Precision

The application uses:
- Day-level precision for time calculations
- 6 decimal places for light-year display
- ±5% tolerance for star matching (adjustable in code)
- Shows exact day difference for each matching star

## 🔬 Scientific Accuracy

- Light-year calculation based on 365.25 days per year
- Star distances from reliable astronomical sources
- Precise date calculations using JavaScript Date API

## 🎓 Educational Value

Learn about:
- The scale of the universe
- How far light travels over time
- Real stars and their distances
- Constellations and star types
- The concept of "looking back in time"

## 🛠️ Customization

You can easily:
- Add more stars to `stars-database.json`
- Adjust tolerance in `StarFinderService.findStarsAtDistance()`
- Modify the UI theme in `styles.css`
- Change default date range in the initialization code

## 📝 License

This project is open source and available for educational and personal use.

## 🌟 Credits

Built with love for astronomy and meaningful moments in time.

---

**Enjoy discovering which stars have been sending you light through your life's journey!** ✨
