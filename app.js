// Star database - SQLite instance
let db = null;
let dbLoaded = false;

// Load SQLite database
async function loadStarsDatabase() {
    try {
        console.log('Initializing SQL.js...');
        const SQL = await initSqlJs({
            locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
        });

        console.log('Fetching stars database...');
        const response = await fetch('stars.db');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const buffer = await response.arrayBuffer();
        db = new SQL.Database(new Uint8Array(buffer));

        // Test query to verify database
        const result = db.exec('SELECT COUNT(*) as count FROM stars');
        const starCount = result[0].values[0][0];
        console.log(`✓ Loaded database with ${starCount.toLocaleString()} stars`);

        dbLoaded = true;
        return true;
    } catch (error) {
        console.error('Error loading stars database:', error);
        showError('Failed to load stars database. Please refresh the page.');
        return false;
    }
}

// Date calculation service
class DateCalculationService {
    static calculateDaysBetween(date1, date2) {
        const millisecondsPerDay = 1000 * 60 * 60 * 24;
        const timeDifference = Math.abs(date2.getTime() - date1.getTime());
        return timeDifference / millisecondsPerDay;
    }

    static daysToLightYears(days) {
        const daysPerYear = 365.25;
        return days / daysPerYear;
    }

    static formatNumber(num, decimals = 2) {
        return num.toLocaleString('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }
}

// Star finder service - finds stars at a specific distance using SQLite
class StarFinderService {
    /**
     * Find stars at a specific distance with month tolerance
     * @param {number} targetLightYears - Target distance in light-years
     * @param {number} toleranceMonths - Tolerance in months (default 1 month)
     * @returns {Array} Array of matching stars
     */
    static findStarsAtDistance(targetLightYears, toleranceMonths = 1) {
        if (!dbLoaded || !db) {
            console.error('Database not loaded');
            return [];
        }

        // Calculate tolerance: 1 month ≈ 1/12 light-year ≈ 0.0833 ly
        const toleranceLY = (toleranceMonths / 12);
        const minDistance = Math.max(0, targetLightYears - toleranceLY);
        const maxDistance = targetLightYears + toleranceLY;

        console.log(`Querying stars between ${minDistance.toFixed(4)} and ${maxDistance.toFixed(4)} light-years (±${toleranceMonths} month${toleranceMonths > 1 ? 's' : ''})`);

        try {
            const query = `
                SELECT
                    proper_name,
                    bayer,
                    constellation,
                    distance,
                    mag,
                    spect,
                    ra,
                    dec
                FROM stars
                WHERE distance >= ? AND distance <= ?
                ORDER BY ABS(distance - ?) ASC
                LIMIT 50
            `;

            const result = db.exec(query, [minDistance, maxDistance, targetLightYears]);

            if (!result.length || !result[0].values.length) {
                return [];
            }

            const stars = result[0].values.map(row => {
                const [proper_name, bayer, constellation, distance, mag, spect, ra, dec] = row;

                let name = proper_name || bayer || `HIP ${Math.floor(Math.random() * 100000)}`;

                let type = 'Unknown';
                if (spect) {
                    const spec = spect.trim().toUpperCase();
                    if (spec.startsWith('O')) type = 'O-type (Blue)';
                    else if (spec.startsWith('B')) type = 'B-type (Blue-white)';
                    else if (spec.startsWith('A')) type = 'A-type (White)';
                    else if (spec.startsWith('F')) type = 'F-type (Yellow-white)';
                    else if (spec.startsWith('G')) type = 'G-type (Yellow)';
                    else if (spec.startsWith('K')) type = 'K-type (Orange)';
                    else if (spec.startsWith('M')) type = 'M-type (Red)';
                    else if (spec.startsWith('D')) type = 'White Dwarf';
                }

                // Get color based on spectral type (enhanced contrast)
                // M and K stars dominate nearby space, so make their colors distinct
                let color = '#FFFFFF';
                if (spect) {
                    const spec = spect.trim().toUpperCase();
                    if (spec.startsWith('O')) color = '#92B5FF';      // Deep blue
                    else if (spec.startsWith('B')) color = '#A2C0FF'; // Blue-white
                    else if (spec.startsWith('A')) color = '#D5E0FF'; // White-blue
                    else if (spec.startsWith('F')) color = '#F9F5FF'; // Pure white
                    else if (spec.startsWith('G')) color = '#FFF4E0'; // Yellow (Sun-like)
                    else if (spec.startsWith('K')) color = '#FFCC80'; // Distinct orange
                    else if (spec.startsWith('M')) color = '#FF9966'; // Red-orange (most common)
                }

                return {
                    name: name,
                    distance: distance,
                    constellation: constellation || 'Unknown',
                    type: type,
                    magnitude: mag || 10,
                    ra: ra || 0,
                    dec: dec || 0,
                    color: color
                };
            });

            console.log(`Found ${stars.length} stars`);
            return stars;

        } catch (error) {
            console.error('Error querying database:', error);
            return [];
        }
    }

    static calculateDaysDifference(targetLightYears, starDistance) {
        const differenceInLightYears = Math.abs(starDistance - targetLightYears);
        return differenceInLightYears * 365.25;
    }
}

// Constellation Renderer - draws stars on canvas
class ConstellationRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.stars = [];
        this.connections = [];
    }

    /**
     * Set the stars to render
     * @param {Array} stars - Array of star objects with ra, dec, magnitude, color
     */
    setStars(stars) {
        this.stars = stars;
        this.generateConnections();
    }

    /**
     * Generate constellation lines connecting nearby stars
     */
    generateConnections() {
        this.connections = [];
        if (this.stars.length < 2) return;

        // Connect stars based on proximity (create a simple pattern)
        const sortedStars = [...this.stars].sort((a, b) => a.ra - b.ra);

        // Connect sequential stars to form a pattern
        for (let i = 0; i < sortedStars.length - 1; i++) {
            // Connect to next star
            this.connections.push([i, i + 1]);

            // Occasionally connect to create triangles
            if (i < sortedStars.length - 2 && i % 2 === 0) {
                this.connections.push([i, i + 2]);
            }
        }

        // Close the constellation if we have enough stars
        if (sortedStars.length >= 3) {
            this.connections.push([sortedStars.length - 1, 0]);
        }
    }

    /**
     * Convert RA/Dec to canvas coordinates
     * RA: 0-24 hours (or 0-360 degrees)
     * Dec: -90 to +90 degrees
     */
    raDecToCanvas(ra, dec) {
        const padding = 60;
        const width = this.canvas.width - padding * 2;
        const height = this.canvas.height - padding * 2;

        // Normalize RA to 0-1 range
        const normalizedRA = (ra % 24) / 24;

        // Normalize Dec to 0-1 range (-90 to +90 -> 0 to 1)
        const normalizedDec = (dec + 90) / 180;

        const x = padding + normalizedRA * width;
        const y = padding + (1 - normalizedDec) * height; // Flip Y axis

        return { x, y };
    }

    /**
     * Calculate star size based on magnitude
     * Brighter stars (lower magnitude) should be larger
     */
    magnitudeToSize(magnitude) {
        // Magnitude typically ranges from -1 (very bright) to 15+ (very dim)
        // Map to size 2-12 pixels
        const minMag = -1;
        const maxMag = 12;
        const minSize = 2;
        const maxSize = 10;

        const clampedMag = Math.max(minMag, Math.min(maxMag, magnitude));
        const normalized = (maxMag - clampedMag) / (maxMag - minMag);
        return minSize + normalized * (maxSize - minSize);
    }

    /**
     * Draw the constellation
     */
    render() {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        // Clear canvas with dark space background
        ctx.fillStyle = '#0a0a1a';
        ctx.fillRect(0, 0, width, height);

        // Draw subtle grid/background stars
        this.drawBackgroundStars();

        if (this.stars.length === 0) {
            this.drawNoStarsMessage();
            return;
        }

        // Calculate canvas positions for all stars
        const starPositions = this.stars.map(star => ({
            ...star,
            pos: this.raDecToCanvas(star.ra, star.dec)
        }));

        // Sort by RA for consistent connections
        starPositions.sort((a, b) => a.ra - b.ra);

        // Draw constellation lines
        this.drawConnections(starPositions);

        // Draw stars
        this.drawStars(starPositions);

        // Draw labels for named stars
        this.drawLabels(starPositions);

        // Draw title
        this.drawTitle();
    }

    drawBackgroundStars() {
        const ctx = this.ctx;
        // Draw random small background stars for ambiance
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        for (let i = 0; i < 100; i++) {
            const x = Math.random() * this.canvas.width;
            const y = Math.random() * this.canvas.height;
            const size = Math.random() * 1.5;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    drawConnections(starPositions) {
        const ctx = this.ctx;

        // Draw subtle constellation lines
        ctx.strokeStyle = 'rgba(100, 150, 255, 0.2)';
        ctx.lineWidth = 1;
        ctx.shadowColor = 'rgba(100, 150, 255, 0.4)';
        ctx.shadowBlur = 4;

        ctx.beginPath();
        for (let i = 0; i < starPositions.length - 1; i++) {
            const star1 = starPositions[i];
            const star2 = starPositions[i + 1];
            ctx.moveTo(star1.pos.x, star1.pos.y);
            ctx.lineTo(star2.pos.x, star2.pos.y);
        }

        // Close the constellation
        if (starPositions.length >= 3) {
            const first = starPositions[0];
            const last = starPositions[starPositions.length - 1];
            ctx.moveTo(last.pos.x, last.pos.y);
            ctx.lineTo(first.pos.x, first.pos.y);
        }

        ctx.stroke();
        ctx.shadowBlur = 0;
    }

    drawStars(starPositions) {
        const ctx = this.ctx;

        for (const star of starPositions) {
            const size = this.magnitudeToSize(star.magnitude);

            // Draw glow
            const gradient = ctx.createRadialGradient(
                star.pos.x, star.pos.y, 0,
                star.pos.x, star.pos.y, size * 3
            );
            gradient.addColorStop(0, star.color);
            gradient.addColorStop(0.3, star.color + '80');
            gradient.addColorStop(1, 'transparent');

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(star.pos.x, star.pos.y, size * 3, 0, Math.PI * 2);
            ctx.fill();

            // Draw star core
            ctx.fillStyle = star.color;
            ctx.beginPath();
            ctx.arc(star.pos.x, star.pos.y, size, 0, Math.PI * 2);
            ctx.fill();

            // Draw bright center
            ctx.fillStyle = '#FFFFFF';
            ctx.beginPath();
            ctx.arc(star.pos.x, star.pos.y, size * 0.4, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    drawLabels(starPositions) {
        const ctx = this.ctx;
        ctx.font = '11px Arial, sans-serif';
        ctx.fillStyle = 'rgba(200, 220, 255, 0.9)';
        ctx.textAlign = 'center';

        // Only label the first few stars to avoid clutter
        const starsToLabel = starPositions.slice(0, 5);

        for (const star of starsToLabel) {
            if (star.name && !star.name.startsWith('HIP')) {
                ctx.fillText(star.name, star.pos.x, star.pos.y - 15);
            }
        }
    }

    drawTitle() {
        const ctx = this.ctx;
        ctx.font = 'bold 16px Arial, sans-serif';
        ctx.fillStyle = 'rgba(200, 220, 255, 0.9)';
        ctx.textAlign = 'center';
        ctx.fillText('Your Personal Constellation', this.canvas.width / 2, 30);

        ctx.font = '12px Arial, sans-serif';
        ctx.fillStyle = 'rgba(150, 170, 200, 0.8)';
        ctx.fillText(`${this.stars.length} stars at your special distance`, this.canvas.width / 2, 50);
    }

    drawNoStarsMessage() {
        const ctx = this.ctx;
        ctx.font = '18px Arial, sans-serif';
        ctx.fillStyle = 'rgba(150, 170, 200, 0.8)';
        ctx.textAlign = 'center';
        ctx.fillText('No stars found at this distance', this.canvas.width / 2, this.canvas.height / 2);
        ctx.font = '14px Arial, sans-serif';
        ctx.fillText('Try adjusting your date range', this.canvas.width / 2, this.canvas.height / 2 + 25);
    }

    /**
     * Download the constellation as PNG
     */
    downloadImage(filename = 'my-constellation.png') {
        const link = document.createElement('a');
        link.download = filename;
        link.href = this.canvas.toDataURL('image/png');
        link.click();
    }
}

// UI Controller
class UIController {
    static constellationRenderer = null;

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
                    <h3>No stars found within this date range</h3>
                    <p>Try a slightly different date range. We're searching with ±1 month tolerance.</p>
                </div>
            `;
            // Still render empty constellation
            this.renderConstellation([]);
            return;
        }

        // Create constellation section
        const constellationHTML = `
            <div class="constellation-section">
                <h2>✨ Your Personal Constellation</h2>
                <p class="constellation-subtitle">
                    ${stars.length} star${stars.length > 1 ? 's' : ''} form your unique pattern -
                    light that traveled ${targetLightYears.toFixed(2)} years to reach you!
                </p>
                <div class="constellation-container">
                    <canvas id="constellationCanvas" width="800" height="600"></canvas>
                </div>
                <button id="downloadBtn" class="download-btn">
                    📥 Download Constellation
                </button>
            </div>
        `;

        // Create star list
        const starsHTML = stars.slice(0, 10).map(star => {
            const daysDifference = StarFinderService.calculateDaysDifference(targetLightYears, star.distance);
            const accuracyText = daysDifference < 1
                ? 'Perfect match!'
                : `±${Math.round(daysDifference)} days`;

            return `
                <div class="star-card">
                    <div class="star-name">
                        <span class="star-dot" style="background: ${star.color}"></span>
                        ${star.name}
                    </div>
                    <div class="star-info">
                        <div><strong>Distance:</strong> ${star.distance.toFixed(4)} ly</div>
                        <div><strong>Type:</strong> ${star.type}</div>
                        <div><strong>Precision:</strong> ${accuracyText}</div>
                    </div>
                </div>
            `;
        }).join('');

        starResultsContainer.innerHTML = `
            ${constellationHTML}
            <div class="star-list">
                <h3>Stars in Your Constellation</h3>
                ${starsHTML}
                ${stars.length > 10 ? `<p class="more-stars">...and ${stars.length - 10} more stars</p>` : ''}
            </div>
        `;

        // Render constellation on canvas
        this.renderConstellation(stars);

        // Add download button handler
        document.getElementById('downloadBtn').addEventListener('click', () => {
            if (this.constellationRenderer) {
                const date = new Date().toISOString().split('T')[0];
                this.constellationRenderer.downloadImage(`constellation-${date}.png`);
            }
        });
    }

    static renderConstellation(stars) {
        // Wait for canvas to be in DOM
        setTimeout(() => {
            const canvas = document.getElementById('constellationCanvas');
            if (canvas) {
                this.constellationRenderer = new ConstellationRenderer('constellationCanvas');
                this.constellationRenderer.setStars(stars);
                this.constellationRenderer.render();
            }
        }, 100);
    }
}

// Main application logic
async function calculateAndFindStars() {
    const date1Input = document.getElementById('date1').value;
    const date2Input = document.getElementById('date2').value;

    if (!date1Input || !date2Input) {
        UIController.showError('Please select both dates');
        return;
    }

    const date1 = new Date(date1Input);
    const date2 = new Date(date2Input);

    if (date2 < date1) {
        UIController.showError('End date must be after start date');
        return;
    }

    if (!dbLoaded) {
        UIController.showError('Database is still loading. Please wait...');
        return;
    }

    // Calculate days between dates
    const numOfDays = DateCalculationService.calculateDaysBetween(date1, date2);
    const lightYears = DateCalculationService.daysToLightYears(numOfDays);

    // Update stats
    UIController.updateStats(numOfDays, lightYears);

    // Find stars with 1 month tolerance
    const matchingStars = StarFinderService.findStarsAtDistance(lightYears, 1);

    // Display results
    UIController.showResults();
    UIController.displayStars(matchingStars, lightYears);
}

// Event listeners
document.addEventListener('DOMContentLoaded', async () => {
    const calculateBtn = document.getElementById('calculateBtn');
    calculateBtn.disabled = true;
    calculateBtn.textContent = 'Loading Database...';

    const success = await loadStarsDatabase();

    calculateBtn.disabled = false;
    calculateBtn.textContent = 'Find My Constellation ⭐';

    if (!success) {
        UIController.showError('Failed to load star database. Please refresh the page.');
        return;
    }

    // Set default dates
    const today = new Date();
    const tenYearsAgo = new Date();
    tenYearsAgo.setFullYear(today.getFullYear() - 10);

    document.getElementById('date2').valueAsDate = today;
    document.getElementById('date1').valueAsDate = tenYearsAgo;

    calculateBtn.addEventListener('click', calculateAndFindStars);

    document.querySelectorAll('input[type="date"]').forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                calculateAndFindStars();
            }
        });
    });
});

function showError(message) {
    UIController.showError(message);
}
