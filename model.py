from particle import Particle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import itertools as it

#avg displacement between x and y on log-log scale

class Model():
    def __init__(self, t: float, size: int, num_particles: int, intervals: int=10) -> None:
        """
        Initiate instancec of class Particle

        t: float, the size of the timestep
        size: int, the size of bounding box to make. The box will be a square
            ranging from -size to +size in both the x and y directions
        num_particles: int, the number of particles to create in the simulation
        """
        self.t = t
        self.size = size
        self.particles = [self.create_particle() for _ in range(num_particles)]
        self.particle_combos = list(it.combinations(self.particles, 2))
        self.bench_num = 1
        self.x_displacement_timings = []
        self.x_displacement = []
        self.benchmark_intervals = intervals
    
    def create_particle(self, vel_scale=100) -> Particle:
        """
        Create a particle with randomly generate starting position and radius. 
        The velocity is drawn from a Gaussian distribution.

        vel_scale: int representing how much to scale the velocity by

        returns: Particle object
        """
        # set up instance of random number generator
        rand_num_gen = np.random.default_rng()
        
        # randomly generate starting params for particle
        r = rand_num_gen.uniform(low=1.0, high=3.0)
        x = rand_num_gen.uniform(low=-self.size + r, high=self.size - r)
        y = rand_num_gen.uniform(low=-self.size + r, high=self.size - r)
        
        # draw velocity from a Gaussian distribution
        x_vel = rand_num_gen.standard_normal(1) * vel_scale
        y_vel = rand_num_gen.standard_normal(1)* vel_scale

        return Particle(x, y, r, x_vel, y_vel, m=r)
    
    def animate(self, i: int) -> list:
        """
        Function that gets passed to the matplotlib animation function. 

        i: integer, essentially a counter of how many timesteps we've done.
            It's passed automatically by matplotlib's animation class

        returns: array of plt.Circle objects
        """
        if i == self.bench_num * self.benchmark_intervals:
            avg_x_disp = sum([(p.x - p.starting_x) ** 2 for p in self.particles]) / len(self.particles)
            self.x_displacement.append(avg_x_disp)
            self.bench_num *= self.benchmark_intervals
            self.x_displacement_timings.append(self.bench_num)
        for p in self.particles:
            p.update(self.t, self.size, self.size)
        self.particle_collision_handling()
        
        # we have to pass back an array of all the circle objects we want to draw 
        circles = [p.circle for p in self.particles]
        return circles
    
    def draw_particles(self, axes: plt.axes) -> None:
        """
        Draw each particle on the plot axes.

        axes: plt.axes objec to draw the particles on
        """
        for p in self.particles:
            axes.add_patch(p.circle)

    def particle_collision_handling(self) -> None:
        """
        Handle collisions between particles.

        Due to the storage of the particles in a list, collisions are always
        handled in sequential order (the order of the particles in the list)
        rather than random order.

        This function uses teleporation to prevent particles getting stuck in each 
        other. If two particles last collided with each other, they will be able 
        to move through each other, preventing them getting stuck in a collision loop.
        Ultimately this results in a more accurate model. 
        """
        seen = set()
        for p1, p2 in self.particle_combos:
            # this makes sure we're not mixing up last time's collisions with this time's
            if p1 not in seen:
                p1.last = p1.this
                p1.this = set()
            if p2 not in seen:
                p2.last = p2.this
                p2.this = set()

            dist = np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
            # make sure particles aren't touching and didn't collide most recently
            if (dist <= p1.r + p2.r) & (p2 not in p1.last):
                p1_init_x = p1.x_vel
                p1_init_y = p1.y_vel
                
                total_mass = p1.m + p2.m
                p1.x_vel = (p1.m - p2.m) * p1.x_vel / total_mass + 2 * p2.m * p2.x_vel / total_mass
                p1.y_vel = (p1.m - p2.m) * p1.y_vel / total_mass + 2 * p2.m * p2.y_vel / total_mass

                p2.x_vel = 2 * p1.m * p1_init_x / total_mass + (p2.m - p1.m) * p2.x_vel / total_mass
                p2.y_vel = 2 * p1.m * p1_init_y / total_mass + (p2.m - p1.m) * p2.y_vel / total_mass

                # keep track of the collision
                p1.this.add(p2)
                p2.this.add(p1)
            seen.add(p1)
            seen.add(p2)
    
    def display_benchmarking(self):
        """
        Display a graph of the average displacement of particles at
        exponentially increasing intervals.
        """
        plt.loglog(self.x_displacement_timings, self.x_displacement, 'o')
        plt.axis("equal")
        plt.title("Average Particle x Displacement Over Time")
        plt.xlabel("Timestep")
        plt.ylabel("Average x^2 displacement")
        plt.show()  
    

# set up the environment for the particles
fig, axes = plt.subplots()    
model = Model(.01, 35, 100, intervals=2)

# set up the animation
anim = ani.FuncAnimation(fig, model.animate, interval=20, blit=True)

axes.set_aspect(1) 
model.draw_particles(axes)
axes.set_xlim([-model.size, model.size])
axes.set_ylim([-model.size, model.size])
plt.title('Particles Go Boing Boing') 
plt.show()
model.display_benchmarking()
