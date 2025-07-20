import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N = 500
t_vals = np.linspace(0, 1, N)

def smoothstep(x):
    return 3 * x**2 - 2 * x**3

# All centered
def line(t):
    return 4 * t - 2, np.zeros_like(t)

def circle(t):
    theta = 2 * np.pi * t
    return np.cos(theta), np.sin(theta)

def infinity(t):
    theta = 2 * np.pi * t
    x = np.sin(theta)
    y = np.sin(theta) * np.cos(theta)
    return x, y

def morph_shapes(t_vals, phase):
    if phase < 0.25:
        p = smoothstep(phase / 0.25)
        x1, y1 = line(t_vals)
        x2, y2 = circle(t_vals)
    elif phase < 0.5:
        p = smoothstep((phase - 0.25) / 0.25)
        x1, y1 = circle(t_vals)
        x2, y2 = infinity(t_vals)
    elif phase < 0.75:
        p = smoothstep((phase - 0.5) / 0.25)
        x1, y1 = infinity(t_vals)
        x2, y2 = line(t_vals)  # same original line again
    else:
        p = smoothstep((phase - 0.75) / 0.25)
        x1, y1 = line(t_vals)
        x2, y2 = line(t_vals)
    x = (1 - p) * x1 + p * x2
    y = (1 - p) * y1 + p * y2
    return x, y

# Plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')
ax.axis('off')
(line_plot,) = ax.plot([], [], 'k-', lw=2)

def init():
    return (line_plot,)

def animate(i):
    phase = i / 120
    x, y = morph_shapes(t_vals, phase)
    line_plot.set_data(x, y)
    return (line_plot,)

ani = animation.FuncAnimation(fig, animate, frames=120, init_func=init,
                              blit=True, interval=50, repeat=True)

ani.save("trs.gif", writer="pillow", fps=20)
