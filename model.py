from particle import Particle
import numpy as np

class Model():
    def __init__(self, t, size, num_particles) -> None:
        self.t = t
        self.size = size
        self.particles = [self.create_particle() for i in range(num_particles)]
    
    def create_particle(self):
        rng = np.random.default_rng()
        r = rng.integers(1, 10)
        x = rng.integers(-10, 10)
        y = rng.integers(-10, 10)
        x_vel = rng.integers(-10, 10)
        y_vel = rng.integers(-10, 10)
        return Particle(x, y, r, x_vel, y_vel)
    
    def animate(self, i):
        # this is really fucky but basically to animate we have to update the 
        # circle object for each particle
        circles = []
        for p in self.particles:
            p.update(self.t, self.size, self.size)
            p.circle.center = p.x, p.y
            circles.append(p.circle)
        return circles
    
model = Model(.05, 25, 2)
print(model.size)

"""
p = Particle(0, 0, 1, 2, -2)
p2 = Particle(1, 1, 3, 2, 2)

fig, axes = plt.subplots()
circle = plt.Circle((p.x, p.y), p.radius)
circle2 = plt.Circle((p2.x, p2.y), p2.radius)


def animate(i):
    t = 0.25
    p.update(t, 25, 25)
    p2.update(t, 25, 25)
    circle.center = p.x, p.y
    circle2.center = p2.x, p2.y
    return circle, circle2

anim = ani.FuncAnimation(fig, animate, frames = 1000, interval=30)
    

axes.set_aspect(1) 
axes.add_artist(circle) 
axes.add_patch(circle2)
axes.set_xlim([-25, 25])
axes.set_ylim([-25, 25])
plt.title( 'Colored Circle' ) 
plt.show()
"""