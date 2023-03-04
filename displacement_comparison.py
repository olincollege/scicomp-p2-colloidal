from model import Model
import matplotlib.pyplot as plt
import matplotlib.animation as ani

"""
This script runs an animation of the change in average displacement
over time for four models, allowing comparison of how the movement
changes with particle density.
"""

# adjust time step or environment size here
t = .01
size = 35

# adjust plot axis limits here
axis_lim = 10e3

# adjust number of particles in each model here
model1 = Model(t, size, 10, intervals=2)
model2 = Model(t, size, 25, intervals=2)
model3 = Model(t, size, 50, intervals=2)
model4 = Model(t, size, 150, intervals=2)
models = [model1, model2, model3, model4]

fig, ax1 = plt.subplots()
benchmark_plot1, = plt.loglog([], [], 'o-', label=f'{len(model1.particles)}')
benchmark_plot2, = plt.loglog([], [], 'o-', label=f'{len(model2.particles)}')
benchmark_plot3, = plt.loglog([], [], 'o-', label=f'{len(model3.particles)}')
benchmark_plot4, = plt.loglog([], [], 'o-', label=f'{len(model4.particles)}')
plots = [benchmark_plot1, benchmark_plot2, benchmark_plot3, benchmark_plot4]

ax1.legend()
plt.suptitle("Displacement Comparison Across Different \nParticle Numbers", size=16)
plt.xlabel("Timestep")
plt.ylabel("Average x^2 Displacement")

ax1.set_xlim(1, axis_lim)
ax1.set_ylim(1, axis_lim)
ax1.set_aspect(1)

def animate(i: int) -> list:
    """
    Function that gets passed to the matplotlib animation function. 

    i: integer, essentially a counter of how many timesteps we've done.
        It's passed automatically by matplotlib's animation class

    returns: the updated axis object
    """
    for model, plot, in zip(models, plots):
        # update all particle positions
        for p in model.particles:
            p.update(model.t, model.size, model.size)
        model.particle_collision_handling()

        # log the average displacement at increasing intervals
        if i == model.bench_num * model.benchmark_intervals:
            avg_x_disp = sum([(p.x - p.starting_x) ** 2 for p in model.particles]) / len(model.particles)
            model.x_displacement.append(avg_x_disp)
            model.bench_num *= model.benchmark_intervals
            model.x_displacement_timings.append(model.bench_num)
            plot.set_data(model.x_displacement_timings, model.x_displacement)
   
    return ax1

anim = ani.FuncAnimation(fig, animate, interval=20)
plt.show()
