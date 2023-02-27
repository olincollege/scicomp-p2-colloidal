import matplotlib.pyplot as plt
from matplotlib import animation as ani

class Particle():
    def __init__(self, x, y, r, x_vel, y_vel) -> None:
        self.x = x
        self.y = y
        self.radius = r
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.circle = plt.Circle((self.x, self.y), self.radius, color='#7CECB4')
        self.last  = None

    def update(self, time_step, xlim, ylim) -> None:
        # calculate where we'll be next time step
        self.x = self.x + self.x_vel * time_step
        self.y = self.y + self.y_vel * time_step

        # check if we're colliding with the walls
        if (self.x + self.radius >= xlim) | (self.x - self.radius <= -xlim):
            self.x_vel = -1 * self.x_vel
            self.last = None
        if (self.y + self.radius >= ylim) | (self.y - self.radius <= -ylim):
            self.y_vel = -1 * self.y_vel
            self.last = None
