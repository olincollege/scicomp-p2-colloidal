from model import Model
import matplotlib.pyplot as plt
import matplotlib.animation as ani

"""
This script shows an animation of a model side by size with an 
animation of its average displacement over time. 
"""

# adjust model params here
t= .01
size = 35
num_particles = 100

model = Model(t, size, num_particles, intervals=2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
fig.tight_layout(h_pad=5)
plt.suptitle("Side-by-Side Animation and Displacement", size=20)
plt.subplots_adjust(top=.9)

model.draw_particles(ax1)
ax1.set_xlim(-size, size)
ax1.set_ylim(-size, size)
ax1.set_aspect(1)
ax1.set_xlabel("x")
ax1.set_ylabel("y")

benchmark_plot, = ax2.loglog([], [])
ax2.set_xlim(1, 10e3)
ax2.set_ylim(1, 10e3)
ax2.set_aspect(1)
ax2.set_xlabel("Timestep")
ax2.set_ylabel("Average x^2 displacement")


def animate(i: int) -> list:
    """
    Function that gets passed to the matplotlib animation function. 

    i: integer, essentially a counter of how many timesteps we've done.
        It's passed automatically by matplotlib's animation class

    returns: array of objects to update
    """
    objects_to_update = []
    # update all particle positions
    for p in model.particles:
        p.update(model.t, model.size, model.size)
        objects_to_update.append(p.circle)
    model.particle_collision_handling()

    # log the average displacement at increasing intervals
    if i == model.bench_num * model.benchmark_intervals:
        avg_x_disp = sum([(p.x - p.starting_x) ** 2 for p in model.particles]) / len(model.particles)

        model.x_displacement.append(avg_x_disp)
        model.bench_num *= model.benchmark_intervals
        model.x_displacement_timings.append(model.bench_num)
        print(model.x_displacement)

        benchmark_plot.set_data(model.x_displacement_timings, model.x_displacement)
        objects_to_update.append(benchmark_plot,)
   
    # we have to pass back an array of all the objects we want to draw  
    return objects_to_update

anim = ani.FuncAnimation(fig, animate, interval=20)
plt.show()
