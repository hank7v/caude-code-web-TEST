// Star database - will be loaded from JSON file
let starsDatabase = [];

// Load stars database
async function loadStarsDatabase() {
    try {
        const response = await fetch('stars-database.json');
        starsDatabase = await response.json();
        console.log(`Loaded ${starsDatabase.length} stars from database`);
    } catch (error) {
        console.error('Error loading stars database:', error);
        showError('Failed to load stars database. Please refresh the page.');
    }
}

// Date calculation service - calculates the number of days between two dates
class DateCalculationService {
    /**
     * Calculate the number of days between two dates
     * @param {Date} date1 - Start date
     * @param {Date} date2 - End date
     * @returns {number} Number of days (can be fractional for precision)
     */
    static calculateDaysBetween(date1, date2) {
        const millisecondsPerDay = 1000 * 60 * 60 * 24;
        const timeDifference = Math.abs(date2.getTime() - date1.getTime());
        return timeDifference / millisecondsPerDay;
    }

    /**
     * Convert days to light-years with day precision
     * @param {number} days - Number of days
     * @returns {number} Distance in light-years
     */
    static daysToLightYears(days) {
        const daysPerYear = 365.25; // Accounting for leap years
        return days / daysPerYear;
    }

    /**
     * Format a number to specified decimal places
     * @param {number} num - Number to format
     * @param {number} decimals - Number of decimal places
     * @returns {string} Formatted number
     */
    static formatNumber(num, decimals = 2) {
        return num.toLocaleString('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }
}

// Star finder service - finds stars at a specific distance
class StarFinderService {
    /**
     * Find stars at a specific distance from Earth
     * @param {number} targetLightYears - Target distance in light-years
     * @param {number} tolerancePercent - Tolerance as percentage (default 5%)
     * @returns {Array} Array of matching stars with their details
     */
    static findStarsAtDistance(targetLightYears, tolerancePercent = 5) {
        const tolerance = targetLightYears * (tolerancePercent / 100);
        const minDistance = targetLightYears - tolerance;
        const maxDistance = targetLightYears + tolerance;

        const matchingStars = starsDatabase.filter(star => {
            return star.distance >= minDistance && star.distance <= maxDistance;
        });

        // Sort by closest match to target distance
        matchingStars.sort((a, b) => {
            const diffA = Math.abs(a.distance - targetLightYears);
            const diffB = Math.abs(b.distance - targetLightYears);
            return diffA - diffB;
        });

        return matchingStars;
    }

    /**
     * Calculate the precision difference in days between target and actual star distance
     * @param {number} targetLightYears - Target distance
     * @param {number} starDistance - Actual star distance
     * @returns {number} Difference in days
     */
    static calculateDaysDifference(targetLightYears, starDistance) {
        const differenceInLightYears = Math.abs(starDistance - targetLightYears);
        return differenceInLightYears * 365.25;
    }
}

// UI Controller
class UIController {
    static showResults() {
        document.getElementById('results').classList.remove('hidden');
        document.getElementById('error').classList.add('hidden');
    }

    static hideResults() {
        document.getElementById('results').classList.add('hidden');
    }

    static showError(message) {
        const errorElement = document.getElementById('error');
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
        this.hideResults();
    }

    static updateStats(days, lightYears) {
        document.getElementById('daysValue').textContent =
            DateCalculationService.formatNumber(days, 0);
        document.getElementById('lightYearsValue').textContent =
            DateCalculationService.formatNumber(lightYears, 6);
    }

    static displayStars(stars, targetLightYears) {
        const starResultsContainer = document.getElementById('starResults');

        if (stars.length === 0) {
            starResultsContainer.innerHTML = `
                <div class="no-stars">
                    <div class="no-stars-icon">🔭</div>
                    <h3>No stars found at this exact distance</h3>
                    <p>Try a different date range. Stars in our database range from 4.2 to 2,615 light-years away.</p>
                </div>
            `;
            return;
        }

        const starsHTML = stars.map(star => {
            const daysDifference = StarFinderService.calculateDaysDifference(targetLightYears, star.distance);
            const accuracyText = daysDifference < 1
                ? 'Less than 1 day difference!'
                : `±${Math.round(daysDifference)} days difference`;

            return `
                <div class="star-card">
                    <div class="star-name">⭐ ${star.name}</div>
                    <div class="star-info">
                        <div><strong>Distance:</strong> <span class="star-distance">${star.distance} light-years</span></div>
                        <div><strong>Constellation:</strong> ${star.constellation}</div>
                        <div><strong>Type:</strong> ${star.type}</div>
                        <div><strong>Precision:</strong> ${accuracyText}</div>
                    </div>
                </div>
            `;
        }).join('');

        starResultsContainer.innerHTML = `
            <h2>✨ Your Star${stars.length > 1 ? 's' : ''}!</h2>
            <p style="color: #b8c5d6; margin-bottom: 20px;">
                Found ${stars.length} star${stars.length > 1 ? 's' : ''} whose light has been traveling
                for approximately this duration:
            </p>
            ${starsHTML}
        `;
    }
}

// Main application logic
async function calculateAndFindStars() {
    const date1Input = document.getElementById('date1').value;
    const date2Input = document.getElementById('date2').value;

    // Validate inputs
    if (!date1Input || !date2Input) {
        UIController.showError('Please select both dates');
        return;
    }

    const date1 = new Date(date1Input);
    const date2 = new Date(date2Input);

    // Validate date order
    if (date2 < date1) {
        UIController.showError('End date must be after start date');
        return;
    }

    // Calculate days between dates
    const numOfDays = DateCalculationService.calculateDaysBetween(date1, date2);

    // Convert to light-years
    const lightYears = DateCalculationService.daysToLightYears(numOfDays);

    // Update stats display
    UIController.updateStats(numOfDays, lightYears);

    // Find stars at this distance
    const matchingStars = StarFinderService.findStarsAtDistance(lightYears);

    // Display results
    UIController.showResults();
    UIController.displayStars(matchingStars, lightYears);
}

// Event listeners
document.addEventListener('DOMContentLoaded', async () => {
    // Load the stars database
    await loadStarsDatabase();

    // Set default dates (example: 10 years ago to today)
    const today = new Date();
    const tenYearsAgo = new Date();
    tenYearsAgo.setFullYear(today.getFullYear() - 10);

    document.getElementById('date2').valueAsDate = today;
    document.getElementById('date1').valueAsDate = tenYearsAgo;

    // Add click event listener to calculate button
    document.getElementById('calculateBtn').addEventListener('click', calculateAndFindStars);

    // Allow Enter key to trigger calculation
    document.querySelectorAll('input[type="date"]').forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                calculateAndFindStars();
            }
        });
    });
});

// Helper function to show errors
function showError(message) {
    UIController.showError(message);
}
