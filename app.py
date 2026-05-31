# ============================================
# Comparison of e^x with its Maclaurin Polynomial P_n(x)
# Using numpy and matplotlib
# ============================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from matplotlib.gridspec import GridSpec
import math

# --------------------------------------------------
# helper functions
# --------------------------------------------------

def factorial(n):
    # calculate n! using a simple loop
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result = result * i
    return result


def calc_polynomial(x_values, degree):
    # Maclaurin series for e^x:
    # P_n(x) = 1 + x + x^2/2! + x^3/3! + ... + x^n/n!
    result = np.zeros(len(x_values))
    for i in range(0, degree + 1):
        result = result + (x_values ** i) / factorial(i)
    return result


# --------------------------------------------------
# settings / constants
# --------------------------------------------------

x_min = -2
x_max = 2
initial_degree = 9
initial_step = 0.01

# colors from the web version so it looks the same
BG_COLOR = '#FAFAFA'
CARD_COLOR = '#FFFFFF'
TEXT_COLOR = '#2A2A2A'
MUTED_COLOR = '#5C5C5C'
TEAL = '#14B8A6'
TEAL_DARK = '#0D9488'
ERROR_RED = '#EF4444'
GRID_COLOR = '#E5E7EB'
BORDER_COLOR = '#E5E7EB'
SOFT_BG = '#F3F4F6'

# --------------------------------------------------
# matplotlib font settings
# --------------------------------------------------

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['text.color'] = TEXT_COLOR
plt.rcParams['axes.labelcolor'] = TEXT_COLOR
plt.rcParams['xtick.color'] = MUTED_COLOR
plt.rcParams['ytick.color'] = MUTED_COLOR

# --------------------------------------------------
# create the figure and layout
# --------------------------------------------------

fig = plt.figure(figsize=(14, 8), facecolor=BG_COLOR)
fig.canvas.manager.set_window_title('Polynomial Approximation of e^x')

# title at the top
fig.suptitle(
    'Comparison of $e^x$ with $P_n(x)$',
    fontsize=16, fontweight='bold', color=TEXT_COLOR, y=0.97
)

# gridspec for the two-column layout
# left column = main chart (big)
# right column = error chart on top, stats below
gs = GridSpec(
    3, 2,
    figure=fig,
    width_ratios=[2, 1],
    height_ratios=[2.5, 1.2, 0.8],
    hspace=0.45, wspace=0.3,
    left=0.07, right=0.96, top=0.91, bottom=0.18
)

# axes
ax_main = fig.add_subplot(gs[0:2, 0])      # main chart takes up left 2 rows
ax_error = fig.add_subplot(gs[0, 1])        # error chart top-right
ax_stats = fig.add_subplot(gs[1, 1])        # stats area middle-right

# --------------------------------------------------
# style the main chart
# --------------------------------------------------

ax_main.set_facecolor(CARD_COLOR)
ax_main.set_xlabel('x', fontsize=11)
ax_main.set_ylabel('y', fontsize=11)
ax_main.set_ylim(-2, 10)   # fixed y range so you can see divergence
ax_main.set_xlim(x_min, x_max)
ax_main.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.8)

# remove top and right borders for a cleaner look
ax_main.spines['top'].set_visible(False)
ax_main.spines['right'].set_visible(False)
ax_main.spines['bottom'].set_color(BORDER_COLOR)
ax_main.spines['left'].set_color(BORDER_COLOR)

# --------------------------------------------------
# style the error chart
# --------------------------------------------------

ax_error.set_facecolor(CARD_COLOR)
ax_error.set_title(
    'Pointwise error ($e^x$ − $P_n$)',
    fontsize=11, fontweight='bold', color=TEXT_COLOR, pad=10, loc='left'
)
ax_error.grid(False)
ax_error.tick_params(axis='x', bottom=False, labelbottom=False)  # hide x labels like sparkline

for spine in ax_error.spines.values():
    spine.set_color(BORDER_COLOR)

# --------------------------------------------------
# stats area (just text, no axes)
# --------------------------------------------------

ax_stats.set_facecolor(SOFT_BG)
ax_stats.set_xticks([])
ax_stats.set_yticks([])
for spine in ax_stats.spines.values():
    spine.set_visible(False)

# --------------------------------------------------
# generate the initial data
# --------------------------------------------------

x_data = np.arange(x_min, x_max + initial_step, initial_step)
x_data = np.round(x_data, 4)   # avoid floating point weirdness

true_values = np.exp(x_data)
approx_values = calc_polynomial(x_data, initial_degree)
error_values = true_values - approx_values

# --------------------------------------------------
# plot the initial data on the main chart
# --------------------------------------------------

line_true, = ax_main.plot(
    x_data, true_values,
    color=TEXT_COLOR, linewidth=2, solid_capstyle='round',
    label='True function $e^x$'
)
line_approx, = ax_main.plot(
    x_data, approx_values,
    color=TEAL, linewidth=2, linestyle='--',
    label='Maclaurin $P_n(x)$'
)
ax_main.legend(
    loc='upper left', fontsize=9,
    framealpha=0.9, edgecolor=BORDER_COLOR,
    fancybox=True
)

# --------------------------------------------------
# plot the initial error chart
# --------------------------------------------------

line_error, = ax_error.plot(x_data, error_values, color=ERROR_RED, linewidth=1.5)
error_fill = ax_error.fill_between(x_data, error_values, alpha=0.1, color=ERROR_RED)

# --------------------------------------------------
# stats text
# --------------------------------------------------

max_err = np.max(np.abs(error_values))
max_err_idx = np.argmax(np.abs(error_values))
max_err_x = x_data[max_err_idx]

# format small errors in scientific notation
if max_err < 1e-4:
    err_str = f"{max_err:.2e}"
else:
    err_str = f"{max_err:.5f}"

# two lines of text in the stats box
stats_main_text = ax_stats.text(
    0.5, 0.65, '',
    fontsize=11, ha='center', va='center',
    transform=ax_stats.transAxes, color=TEXT_COLOR, fontweight='bold'
)
stats_sub_text = ax_stats.text(
    0.5, 0.30, '',
    fontsize=9, ha='center', va='center',
    transform=ax_stats.transAxes, color=MUTED_COLOR
)

# set initial stats text
stats_main_text.set_text(f'Max |error|   {err_str}')
stats_sub_text.set_text(f'at x ≈ {max_err_x:.3f}   •   Grid: [-2, 2]   •   step: {initial_step}')

# --------------------------------------------------
# add a divider line in the stats box (like the web version's <hr>)
# --------------------------------------------------

ax_stats.axhline(y=0.48, xmin=0.1, xmax=0.9, color=BORDER_COLOR, linewidth=0.8,
                 transform=ax_stats.transAxes)

# --------------------------------------------------
# interactive widgets
# --------------------------------------------------

# degree slider
slider_ax = fig.add_axes([0.07, 0.08, 0.55, 0.025], facecolor=SOFT_BG)
degree_slider = Slider(
    slider_ax, 'Degree  $n$', 0, 25,
    valinit=initial_degree, valstep=1,
    color=TEAL, initcolor='none'
)
degree_slider.label.set_fontsize(11)
degree_slider.valtext.set_fontsize(11)

# step size text box
step_label_ax = fig.add_axes([0.70, 0.08, 0.08, 0.025])
step_label_ax.set_facecolor(BG_COLOR)
step_label_ax.set_xticks([])
step_label_ax.set_yticks([])
for spine in step_label_ax.spines.values():
    spine.set_visible(False)
step_label_ax.text(0.5, 0.5, 'Grid step:', fontsize=10, ha='center', va='center',
                   color=MUTED_COLOR, transform=step_label_ax.transAxes)

step_box_ax = fig.add_axes([0.79, 0.075, 0.06, 0.03])
step_textbox = TextBox(step_box_ax, '', initial=str(initial_step))
step_textbox.label.set_fontsize(10)

# update button
btn_ax = fig.add_axes([0.87, 0.07, 0.08, 0.04])
update_btn = Button(btn_ax, 'Update plot', color=TEAL, hovercolor=TEAL_DARK)
update_btn.label.set_color('white')
update_btn.label.set_fontweight('bold')
update_btn.label.set_fontsize(10)

# --------------------------------------------------
# the update function - this runs when you change the slider or press the button
# --------------------------------------------------

# we need this to be global so we can remove the old fill
current_step = initial_step

def update_plot(val=None):
    global error_fill, current_step

    # get current degree from slider
    degree = int(degree_slider.val)

    # try to read step from the text box
    try:
        step = float(step_textbox.text)
        if step <= 0 or step > 0.5:
            step = 0.01   # safety fallback
    except:
        step = 0.01       # if they type something weird

    current_step = step

    # recalculate everything
    x = np.arange(x_min, x_max + step, step)
    x = np.round(x, 4)

    true_vals = np.exp(x)
    approx_vals = calc_polynomial(x, degree)
    errors = true_vals - approx_vals

    # update the main chart
    line_true.set_xdata(x)
    line_true.set_ydata(true_vals)
    line_approx.set_xdata(x)
    line_approx.set_ydata(approx_vals)

    # update the error chart
    line_error.set_xdata(x)
    line_error.set_ydata(errors)

    # have to remove old fill and make a new one (matplotlib is annoying about this)
    error_fill.remove()
    error_fill = ax_error.fill_between(x, errors, alpha=0.1, color=ERROR_RED)

    # rescale the error chart y axis
    ax_error.relim()
    ax_error.autoscale_view()

    # update stats
    max_e = np.max(np.abs(errors))
    max_e_idx = np.argmax(np.abs(errors))
    max_e_x = x[max_e_idx]

    if max_e < 1e-4:
        formatted_err = f"{max_e:.2e}"
    else:
        formatted_err = f"{max_e:.5f}"

    stats_main_text.set_text(f'Max |error|   {formatted_err}')
    stats_sub_text.set_text(f'at x ≈ {max_e_x:.3f}   •   Grid: [-2, 2]   •   step: {step}')

    # redraw
    fig.canvas.draw_idle()


# connect the slider and button to the update function
degree_slider.on_changed(update_plot)
update_btn.on_clicked(update_plot)

# also update when they press enter in the step textbox
step_textbox.on_submit(lambda text: update_plot())

# --------------------------------------------------
# show the plot!
# --------------------------------------------------

plt.show()
