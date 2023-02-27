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
        size: int, the size of bounding box to make. The box will be a square of 
            size x size
        num_particles: int, the number of particles to create in the simulation
        """
        self.t = t
        self.size = size
        self.particles = [self.create_particle() for i in range(num_particles)]

    def assign_vel(self, particle: Particle, dir:int=1) -> None:
        rng = np.random.default_rng()
        particle.x_vel = rng.integers(0, 10) * dir
        particle.y_vel = rng.integers(0, 10) * dir
    
    def create_particle(self) -> Particle:
        rng = np.random.default_rng()
        r = rng.integers(1, 3)
        x = rng.integers(-self.size, self.size)
        y = rng.integers(-self.size, self.size)
        x_vel = rng.standard_normal(1) * 10
        y_vel = rng.standard_normal(1)* 10
        return Particle(x, y, r, x_vel, y_vel)
    
    def animate(self, i: int) -> list:
        # this is really fucky but basically to animate we have to update the 
        # circle object for each particle
        circles = []
        for p in self.particles:
            p.update(self.t, self.size, self.size)
            p.circle.center = p.x, p.y
            circles.append(p.circle)
        self.particle_collision_handling()
        return circles
    
    def draw_particles(self, axes: plt.axes) -> None:
        # draw each particle in the environment
        for p in self.particles:
            axes.add_patch(p.circle)

    def particle_collision_handling(self) -> None:
        handled = set()
        for p in self.particles:
            if p not in handled:
                for q in self.particles:
                    if (p != q):
                        dist = np.sqrt((p.x - q.x) ** 2 + (p.y - q.y) ** 2)
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


    

fig, axes = plt.subplots()    
model = Model(.01, 25, 50)

anim = ani.FuncAnimation(fig, model.animate, frames = 1000, interval=30)
    
axes.set_aspect(1) 
model.draw_particles(axes)
axes.set_xlim([-model.size, model.size])
axes.set_ylim([-model.size, model.size])
plt.title( 'Particles Go Boing Boing' ) 
plt.show()
