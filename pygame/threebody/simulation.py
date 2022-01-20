import numpy as np
import scipy as sci
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy import integrate
class metaverse():
    def __init__(self):
        #Define universal gravitation constant
        self.G=6.67408e-11 #N-m2/kg2

        #Reference quantities
        self.m_nd=1.989e+30 #kg #mass of the sun
        self.r_nd=5.326e+12 #m #distance between stars in Alpha Centauri
        self.v_nd=30000 #m/s #relative velocity of earth around the sun
        self.t_nd=79.91*365*24*3600*0.51 #s #orbital period of Alpha Centauri

        #Net constants
        self.K1=self.G*self.t_nd*self.m_nd/(self.r_nd**2*self.v_nd)
        self.K2=self.v_nd*self.t_nd/self.r_nd

class star():
    def __init__(self, m, r, v):
        #Define masses
        self.m=m
        
        #Define initial position vectors
        self.r=r #m
        #Convert pos vectors to arrays
        self.r=np.array(self.r,dtype="float64")

        #Define initial velocities
        self.v=v #m/s
        #Convert velocity vectors to arrays
        self.v=np.array(self.v,dtype="float64")

class com():
    """
    The centre of mass is a point where the the sum of the all 
    the mass moments of the system is zero — in simple terms, 
    you can imagine it as the point where the whole mass of the 
    system is balanced.
    """
    def __init__(self, m, r, v):
        self.m = np.array(m,dtype="float64")
        self.r = np.array(r,dtype="float64")
        self.v = np.array(v,dtype="float64")
        
        self.r_com = self.m.dot(self.r) / self.m.sum()
        self.v_com = self.m.dot(self.v) / self.m.sum()

#A function defining the equations of motion 
def TwoBodyEquations(w,t,K,m):
    K1=K[0]
    K2=K[1]
    m1=m[0]
    m2=m[1]
    r1=w[:3]
    r2=w[3:6]
    v1=w[6:9]
    v2=w[9:12]
    r=sci.linalg.norm(r2-r1) #Calculate magnitude or norm of vector
    dv1bydt=K1*m2*(r2-r1)/r**3
    dv2bydt=K1*m1*(r1-r2)/r**3
    dr1bydt=K2*v1
    dr2bydt=K2*v2
    r_derivs=np.concatenate((dr1bydt,dr2bydt))
    derivs=np.concatenate((r_derivs,dv1bydt,dv2bydt))
    return derivs

def ThreeBodyEquations(w,t,K,m):
    K1=K[0]
    K2=K[1]
    m1=m[0]
    m2=m[1]
    m3=m[2]
    r1=w[:3]
    r2=w[3:6]
    r3=w[6:9]
    v1=w[9:12]
    v2=w[12:15]
    v3=w[15:18]
    r12=sci.linalg.norm(r2-r1)
    r13=sci.linalg.norm(r3-r1)
    r23=sci.linalg.norm(r3-r2)
    
    dv1bydt=K1*m2*(r2-r1)/r12**3+K1*m3*(r3-r1)/r13**3
    dv2bydt=K1*m1*(r1-r2)/r12**3+K1*m3*(r3-r2)/r23**3
    dv3bydt=K1*m1*(r1-r3)/r13**3+K1*m2*(r2-r3)/r23**3
    dr1bydt=K2*v1
    dr2bydt=K2*v2
    dr3bydt=K2*v3
    r12_derivs=np.concatenate((dr1bydt,dr2bydt))
    r_derivs=np.concatenate((r12_derivs,dr3bydt))
    v12_derivs=np.concatenate((dv1bydt,dv2bydt))
    v_derivs=np.concatenate((v12_derivs,dv3bydt))
    derivs=np.concatenate((r_derivs,v_derivs))
    return derivs

def ode_3body(m, r, v, K, orbital_periods=20, points=500):
    #Package initial parameters
    init_params=np.array([r, v]) #Initial parameters
    init_params=init_params.flatten() #Flatten to make 1D array
    time_span=np.linspace(0,orbital_periods,points) #20 orbital periods and 500 points

    #Run the ODE solver
    three_body_sol=sci.integrate.odeint(ThreeBodyEquations,init_params,time_span,args=(K,m))
    
    r1_sol=three_body_sol[:,:3]
    r2_sol=three_body_sol[:,3:6]
    r3_sol=three_body_sol[:,6:9]

    r_sol = [r1_sol, r2_sol, r3_sol]
    return r_sol

def plot(r_sol, file_gif, title, colors, labels,
         xlim=(-2, 2), ylim=(-0.2, 0.8), zlim=(-4, 0)):
    n = len(r_sol)
    
    fig=plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)

    lines = []
    for i in range(n):
        line, = ax.plot([], [], [], color=colors[i], label=labels[i], alpha=0.5, linewidth=3)
        lines.append(line)

    def init():
        for line in lines:
            line.set_data([], [])
            line.set_3d_properties([])
        return lines

    def animate(i):
        for m, line in enumerate(lines):
            r = r_sol[m]
            x, y, z = r[:i ,0], r[:i, 1], r[:i, 2]

            line.set_data(x, y)
            line.set_3d_properties(z)
        return lines

    anim = animation.FuncAnimation(fig, 
                                 animate, 
                                 init_func=init, 
                                 frames=500, 
                                 interval=10, 
                                 blit=True)

    #Add a few more bells and whistles
    ax.set_xlabel("x-coordinate", fontsize=14)
    ax.set_ylabel("y-coordinate", fontsize=14)
    ax.set_zlabel("z-coordinate", fontsize=14)
    ax.set_title(title, fontsize=14)
    ax.legend(loc="upper left", fontsize=14)

    anim.save(file_gif, writer=animation.PillowWriter())
    plt.show()
    return None

def main():
    print('create a metavers!')
    meta = metaverse()
    K = [meta.K1, meta.K2]
    
    print('create stars!')
    m = [1.1, 0.907, 1]
    r = [[-0.5,0,0], [0.5,0,0], [0,1,0]]
    v = [[0.01,0.01,0], [-0.05,0,-0.1], [0,-0.01,0]]
    
    colors = ["darkblue", "tab:red", "tab:green"]
    labels = ["Alpha Centauri A", "Alpha Centauri B", "Third Star"]
    
    print('move stars!')
    r_sol = ode_3body(m, r, v, K)
    
    file_gif="three_body_model.gif"
    title="Visualization of orbits of stars in a three-body system\n"
    
    plot(r_sol=r_sol, 
         file_gif=file_gif, 
         title=title,
         colors=colors,
         labels=labels)

if __name__ == '__main__':
    main()