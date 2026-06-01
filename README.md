# Polynomial Approximation of $e^x$

## Overview
This was built to visualize how Maclaurin polynomial approximations $P_n(x)$ hold up against the real $e^x$. You can drag a slider to change the polynomial degree.

Runs on NumPy and Matplotlib, nothing else.

## Features
- **Degree slider**: Adjust $n$ from 0 to 25. The plot redraws when you click update plot.
- **Grid step input**: Change the step size for the calculation grid. Garbage inputs (text, out-of-range numbers) just reset to 0.01.
- **Error plot**: A second chart shows the absolute error $e^x - P_n(x)$ across the domain so you can actually see where things go wrong.
- **Error stats**: Shows the max absolute error over $[-2, 2]$ and the exact $x$ where it's worst.

## Requirements
Python 3, plus:
- `numpy`
- `matplotlib`

```bash
pip install numpy matplotlib
```

## Usage
```bash
python3 app.py
```

### Controls
1. **Degree $n$**: Drag the slider (bottom left). Plots update automatically.
2. **Grid step**: Type a value like `0.01` or `0.05` in the text box (bottom right).
3. **Update plot**: Click to apply. Anything invalid or out of range (0.0–0.5) falls back to 0.01.

## Math
The Maclaurin series for $e^x$ (Taylor series centered at $a = 0$) is:

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots + \frac{x^n}{n!}$$

The tool computes the partial sum $P_n(x)$ up to whatever degree $n$ you pick and plots it against `np.exp(x)` over $[-2, 2]$.