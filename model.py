from particle import Particle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

#avg displacement between x and y on log-log scale

class Model():
    def __init__(self, t: float, size: int, num_particles: int) -> None:
        """
        Initiate instancec of class Particle

        t: float, the size of the timestep
        size: int, the size of bounding box to make. The box will be a square
            ranging from -size to +size in both the x and y directions
        num_particles: int, the number of particles to create in the simulation
        """
        self.t = t
        self.size = size
        self.particles = [self.create_particle() for i in range(num_particles)]
    
    def create_particle(self) -> Particle:
        """
        Create a particle with randomly generate starting position and radius. 
        The velocity is drawn from a Gaussian distribution.

        returns: Particle object
        """
        # set up instance of random number generator
        rng = np.random.default_rng()
        # randomly generate radii between 1.0 and 3.0 (units need not apply)
        r = rng.uniform(low=0.5, high=3.0)
        # randomly generate a starting location between -size and +size in both
        # x and y directions
        x = rng.uniform(low=-self.size, high=self.size)
        y = rng.uniform(low=-self.size, high=self.size)
        # draw a random x and y velocity from a Gaussian distribution
        x_vel = rng.standard_normal(1) * 10
        y_vel = rng.standard_normal(1)* 10
        return Particle(x, y, r, x_vel, y_vel)
    
    def animate(self, i: int) -> list:
        """
        Function that gets passed to the matplotlib animation function. 

        i: integer, essentially a counter of how many timesteps we've done. 
            We don't use it but we still need to pass it or the animation
            will break

        returns: array of plt.Circle objects
        """
        # this is really fucky but basically to animate we have to update the 
        # circle object for each particle
        circles = []
        for p in self.particles:
            # calculate where the particle will be next step
            p.update(self.t, self.size, self.size)
            # update where to draw the circle
            p.circle.center = p.x, p.y
            circles.append(p.circle)
        # handle collisions that will occur
        self.particle_collision_handling()
        # we have to pass back an array of all the circle objects we want to draw
        return circles
    
    def draw_particles(self, axes: plt.axes) -> None:
        """
        Draw each particle on the plot axes.

        axes: plt.axes objec to draw the particles on
        """
        # draw each particle in the environment
        for p in self.particles:
            axes.add_patch(p.circle)

    def particle_collision_handling(self) -> None:
        """
        Handle collisions between particles.

        The function simply iterates through the list of particles and checks if 
        they are colliding. This means that particles at the beginning of the
        particle list will always be handled before particles at the end of the
        list. Therefore, the resolution of triple collisions is sequential 
        (meaning it is handled as multiple instances of collisions between three 
        particles, not one three-way collision) but the collisions are not 
        resolved in a random order.

        This function relies on a teleporation mechanism to prevent particles 
        getting stuck in each other and model more accurately. If two particles
        most recently collided with each other, they will be able to move through
        each other instead of getting stuck in a loop of switching velocities.
        """
        # track which particles we've already handled
        # this is because handling a collision between a and b is the same as
        # handling a collision between b and a so to save computational power
        # we don't want to recompute ones we've already dealt with
        handled = set()
        for p in self.particles:
            # I think something about this logic is a little funky but it works
            # better this way than if I do this check on q instead.
            if p not in handled:
                for q in self.particles:
                    # make sure we're not comparing a particle to itself
                    if (p != q):
                        # calculate the distance between the particle centers
                        dist = np.sqrt((p.x - q.x) ** 2 + (p.y - q.y) ** 2)
                        # check they're not touching, check that they didn't
                        # collide with each other most recently
                        if (dist <= p.radius + q.radius) & (p.last != q):
                            p_xvel = p.x_vel
                            p_yvel = p.y_vel
                            
                            p.x_vel = q.x_vel
                            p.y_vel = q.y_vel

                            q.x_vel = p_xvel
                            q.y_vel = p_yvel
                            p.last = q
                            q.last = p
                    handled.add(q)

# set up the environment for the particles
fig, axes = plt.subplots()    
model = Model(.01, 25, 50)

# set up the animation
anim = ani.FuncAnimation(fig, model.animate, frames = 1000, interval=30)

axes.set_aspect(1) 
# draw the particles on the axes
model.draw_particles(axes)
# set the axes size
axes.set_xlim([-model.size, model.size])
axes.set_ylim([-model.size, model.size])
plt.title('Particles Go Boing Boing') 
plt.show()
