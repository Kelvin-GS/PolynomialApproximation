// Math Utilities
function factorial(n) {
    if (n === 0 || n === 1) return 1;
    let res = 1;
    for (let i = 2; i <= n; i++) {
        res *= i;
    }
    return res;
}

function calculatePolynomial(x, degree) {
    let result = 0;
    for (let i = 0; i <= degree; i++) {
        result += Math.pow(x, i) / factorial(i);
    }
    return result;
}

// Global Chart Instances
let mainChart;
let errorChart;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    setupEventListeners();
    updateApp(); // Initial render
});

function initCharts() {
    // Setup Chart.js global defaults for fonts
    Chart.defaults.font.family = "'Inter', system-ui, -apple-system, sans-serif";
    Chart.defaults.color = "#5C5C5C";

    const ctxMain = document.getElementById('mainChart').getContext('2d');
    const ctxError = document.getElementById('errorChart').getContext('2d');

    // Make charts responsive
    mainChart = new Chart(ctxMain, {
        type: 'line',
        data: {
            labels: [], // x values
            datasets: [
                {
                    label: 'True function eˣ',
                    data: [],
                    borderColor: '#2A2A2A', // Warm charcoal
                    borderWidth: 2,
                    borderDash: [], // Solid
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'Maclaurin Pₙ(x)',
                    data: [],
                    borderColor: '#14B8A6', // Bright teal
                    borderWidth: 2,
                    borderDash: [5, 5], // Dashed
                    tension: 0.4,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        boxWidth: 8,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#2A2A2A',
                    bodyColor: '#5C5C5C',
                    borderColor: '#E5E7EB',
                    borderWidth: 1,
                    displayColors: true,
                    callbacks: {
                        label: function (context) {
                            return `${context.dataset.label}: ${context.parsed.y.toFixed(5)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'x'
                    },
                    grid: {
                        color: '#E5E7EB',
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'y'
                    },
                    grid: {
                        color: '#E5E7EB',
                        drawBorder: false
                    },
                    min: -2,
                    max: 10 // Fixed scale to see divergence clearly without squishing
                }
            }
        }
    });

    errorChart = new Chart(ctxError, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Error (eˣ - Pₙ(x))',
                data: [],
                borderColor: '#EF4444', // Red for error representation
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                borderWidth: 1.5,
                fill: true,
                pointRadius: 0,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#2A2A2A',
                    bodyColor: '#5C5C5C',
                    borderColor: '#E5E7EB',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return `Error: ${context.parsed.y.toExponential(3)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: false // hide x axis for sparkline
                },
                y: {
                    grid: {
                        display: false
                    },
                    // auto scale y for error
                }
            }
        }
    });
}

function setupEventListeners() {
    const degreeInput = document.getElementById('degree-input');
    const degreeSlider = document.getElementById('degree-slider');
    const updateBtn = document.getElementById('update-btn');

    // Sync slider and input bidirectionally
    degreeInput.addEventListener('input', (e) => {
        degreeSlider.value = e.target.value;
    });

    degreeSlider.addEventListener('input', (e) => {
        degreeInput.value = e.target.value;
        // Optional: live update while sliding
        updateApp();
    });

    // Handle update click
    updateBtn.addEventListener('click', updateApp);
}

function updateApp() {
    const degree = parseInt(document.getElementById('degree-input').value, 10);
    let step = parseFloat(document.getElementById('step-input').value);

    // Safety fallback
    if (isNaN(step) || step <= 0) step = 0.01;
    if (isNaN(degree) || degree < 0) degree = 9;

    const xMin = -2;
    const xMax = 2;

    let labels = [];
    let eXData = [];
    let pXData = [];
    let errorData = [];

    let maxError = 0;
    let maxErrorX = 0;

    for (let x = xMin; x <= xMax; x += step) {
        // Handle floating point precision safely
        x = Math.round(x * 10000) / 10000;

        labels.push(x.toFixed(2));

        const trueValue = Math.exp(x);
        const approxValue = calculatePolynomial(x, degree);
        const error = trueValue - approxValue;
        const absError = Math.abs(error);

        eXData.push(trueValue);
        pXData.push(approxValue);
        errorData.push(error);

        if (absError > maxError) {
            maxError = absError;
            maxErrorX = x;
        }
    }

    // Update charts
    mainChart.data.labels = labels;
    mainChart.data.datasets[0].data = eXData;
    mainChart.data.datasets[1].data = pXData;
    mainChart.update();

    errorChart.data.labels = labels;
    errorChart.data.datasets[0].data = errorData;
    errorChart.update();

    // Update Stats Card
    // Using exponential notation for very small or very large errors
    const formattedError = maxError < 1e-4 ? maxError.toExponential(2) : maxError.toFixed(5);

    document.getElementById('max-error-val').textContent = formattedError;
    document.getElementById('max-error-x').textContent = maxErrorX.toFixed(3);
    document.getElementById('stat-step').textContent = step.toString();
}
