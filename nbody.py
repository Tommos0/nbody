#nbody gravity solution

import numpy as np #numpy arrays can be multiplied etc. like vectors
import matplotlib
matplotlib.use('Agg') #no display, output to PDF
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2,figsize=(10,20))

G = 1e-4        #gravitational constant
epsilon = 0.01  #softened force parameter
plotint = 10    #plot after N timesteps
boxsize = (0,2) #stop after body leaves box of this size
dtscale = 0.1   #scale factor for dt - multiplies min. distance between bodies
pointsize = 1   #size of points in scatter plot

class body:
    def __init__(self,x=0,y=0,z=0,mass=1.):
        self.position = np.array([x,y,z])
        self.velocity = np.array([0,0,0])
        self.mass = mass
    def accel(self,b2): #acceleration due to other body
        r = b2.position-self.position #vector pointing to b2 - the other body
        return (r/np.linalg.norm(r)) * G*b2.mass / ((np.linalg.norm(r) + epsilon)**2) #a = r(unit_vector)*GM / (|r|+eps)^2

bodies = (body(1.5,1.,1.),body(0.75,1.133,1.001),body(0.751,0.567,0.799)) #starting conditions
steps = 0
while all(boxsize[0] < coordinate < boxsize[1] for coordinate in np.concatenate([b.position for b in bodies])): #while in box
    steps += 1
    #scale timestep dt with the minimum distance between bodies 
    dt = min(np.linalg.norm(b1.position-b2.position) for b1 in bodies for b2 in bodies if b1!=b2)*dtscale
    for b in bodies:
        b.position = b.position + b.velocity*dt #update position at time t
        b.velocity = b.velocity + np.sum([b.accel(b2) for b2 in bodies if b2!=b],0) * dt #new velocity @ time t+dt/2
        if (steps%plotint == 0): #add plot points every plotint timesteps
            axes[0].scatter(b.position[0],b.position[1],s=pointsize,color=['red','green','blue'][bodies.index(b)]) #x,y
            axes[1].scatter(b.position[0],b.position[2],s=pointsize,color=['red','green','blue'][bodies.index(b)]) #x,z

#set axis/labels etc.
for ax in axes:
    ax.axis([boxsize[0],boxsize[1]]*2)
    ax.set_xlabel('x')
axes[0].set_ylabel('y')
axes[1].set_ylabel('z')
fig.tight_layout()
plt.savefig("output.pdf")
