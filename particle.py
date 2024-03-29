import matplotlib.pyplot as plt
from matplotlib import animation as ani

class Particle():
    def __init__(self, x: float, y: float, r: float, x_vel: float, y_vel: float, m: int=1) -> None:
        """
        Initiate an instance of class Particle.

        x: float, the starting x coordinate for the particle
        y: float, the starting y coordinate for the particle
        r: float, the radius of the particle
        x_vel: float, the x velocity of the particle
        y_vel: float, the y velocity of the particle
        m: int, the mass of the particle. Defaults to 1
        """
        self.x = x
        self.starting_x = self.x
        self.y = y
        self.r = r
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.m = m
        # this store the object that will be drawn on the plot
        self.circle = plt.Circle((self.x, self.y), self.r, color='#7CECB4')
        # this stores the last thing the particle collided with
        self.last  = set()
        self.this = set()

    def update(self, time_step: float, xlim: int, ylim: int) -> None:
        """
        Update a particle's location and handle wall collisions.

        time_step: float, the size of the time_step
        xlim: int, the x boundary of the environment
        ylim: int, the y boundary of the environment
        """
        # calculate where the particle will be next 
        self.x = self.x + self.x_vel * time_step
        self.y = self.y + self.y_vel * time_step

        # update where to draw the circle
        self.circle.center = self.x, self.y

        # handle wall collisions
        if (self.x + self.r >= xlim) | (self.x - self.r <= -xlim):
            self.x_vel = -1 * self.x_vel
            self.this.clear()
        if (self.y + self.r >= ylim) | (self.y - self.r <= -ylim):
            self.y_vel = -1 * self.y_vel
            self.this.clear()