from model import Model
import matplotlib.pyplot as plt
import matplotlib.animation as ani

"""
This script creates models with 10, 25, 50, and 150 particles in a 
70x70 environment. The script will open an animation will which run 
until the environment is closed.
"""

# adjust time step or environment size here
t= .01
size = 35

# adjust number of particles in each model here
model1 = Model(t, size, 10)
model2 = Model(t, size, 25)
model3 = Model(t, size, 50)
model4 = Model(t, size, 150)
models = [model1, model2, model3, model4]

fig, axes = plt.subplots(2, 2)
fig.tight_layout(h_pad=2)
plt.subplots_adjust(top=.85)

axes[0, 0].set_title(f"n = {len(model1.particles)}")
axes[0, 1].set_title(f"n = {len(model2.particles)}")
axes[1, 0].set_title(f"n = {len(model3.particles)}")
axes[1, 1].set_title(f"n = {len(model4.particles)}")

axes[0, 0].set_aspect(1)
axes[0, 1].set_aspect(1)
axes[1, 0].set_aspect(1)
axes[1, 1].set_aspect(1)

axes[0, 0].set_xlim(-size, size)
axes[0, 0].set_ylim(-size, size)
axes[0, 1].set_xlim(-size, size)
axes[0, 1].set_ylim(-size, size)
axes[1, 0].set_xlim(-size, size)
axes[1, 0].set_ylim(-size, size)
axes[1, 1].set_xlim(-size, size)
axes[1, 1].set_ylim(-size, size)

model1.draw_particles(axes[0, 0])
model2.draw_particles(axes[0, 1])
model3.draw_particles(axes[1, 0])
model4.draw_particles(axes[1, 1])

def animate(i: int) -> list:
    """
    Function that gets passed to the matplotlib animation function. 

    i: integer, essentially a counter of how many timesteps we've done.
        It's passed automatically by matplotlib's animation class

    returns: array of plt.Circle objects
    """
    circles = []
    for model in models:
        for p in model.particles:
            p.update(model.t, model.size, model.size)
            circles.append(p.circle)
        model.particle_collision_handling()
    # we have to pass back an array of all the circle objects we want to draw 
    return circles

anim = ani.FuncAnimation(fig, animate, interval=20, blit=True)
plt.suptitle("Comparison of Different Particle Densities", fontsize=20)
plt.show()
