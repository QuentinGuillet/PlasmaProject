import numpy as np


'''q = -1   #Charge
dx = 0.5 #Spatial step
dt = 0.5 #Temporal step
n = 1000 #Number of points on the grid
N = 10000 #Number of particles
T = 100 #Number of temporal steps
X = np.linspace(0,n*dx,n) #Grid array
m = 0.1 #Mass of a particule'''


#Classe de gestion de l'algorithme
    
class Plasma(object):
    
   
    def save_to_array(self):
        self.positionsstored[self.timestamp] = self.pos
        self.speedstored[self.timestamp] = self.speed    
    
    def __init__(self,q,m,dx,dt,n,N,T,eps0,pos_init,speed_init):
        '''Initialization of the intern variables'''
        self.q = q
        self.m = m
        self.dx = dx
        self.dt = dt
        self.n = n
        self.N = N
        self.T = T
        self.eps0 = eps0
        self.timestamp = 0
        '''Initialization of the array variables'''
        self.X = np.linspace(0,n*dx,n)
        self.positionsstored = np.zeros((T,N))
        self.speedstored = np.zeros((T,N))
        
        '''Creating the particules and information arrays'''
        self.pos = pos_init #pos_init should be a numpy array with dimension N
        self.speed = speed_init
        self.rho = np.zeros(n)
        self.rho_ = np.zeros(n)
        self.phi = np.zeros(n)
        self.phi_ = np.zeros(n)
        self.save_to_array()
        
        
    def barycentre(self,pos_i): #Returns the contribution of a particule at pos_i to the density on the grid
        j = int(pos_i/self.dx)
        alpha = (pos_i-self.X[j])/self.dx
        return j,1-alpha,alpha
    
    def position_to_density(self): #Transforms the particule positions to a density array along the grid
        self.rho = np.zeros(self.n)
        for i in range(self.N):
            j,alpha,beta = self.barycentre(self.pos[i]) 
            self.rho[j] += alpha/self.dx
            self.rho[(j+1)%self.n] += beta/self.dx
        
            
    def compute_ElectricField(self):
        self.rho_ = np.fft.fft(self.rho)
        K = np.fft.fftfreq(self.n,self.dx)*2*np.pi
        self.phi_[1:] = self.rho_[1:]/self.eps0/K[1:]**2
        self.phi = np.fft.ifft(self.phi_).real
        self.E = (np.roll(self.phi,1)-np.roll(self.phi,-1))/2/self.dx        # E(x) = - (phi(x+dx)-phi(x-dx)/2dx)
      
    def get_force(self,pos_i): #Returns the force applied on point qi on the grid
        F = self.q*self.E
        j = int(pos_i/self.dx)
        print((j+1)%self.n)
        alpha = (self.X[(j+1)%self.n] - pos_i)*F[j]/self.dx +  (pos_i - self.X[j])*F[(j+1)%self.n]/self.dx
        return alpha
    
    
    def field_to_particules(self): #Transforms a field on the grid to a force aplied to particules, returns the array of forces on the particules
        self.F = np.zeros(self.N)
        for i in range(self.N):
            self.F[i] = self.get_force(self.pos[i])
    
    
    def move_particules(self): #Moves every particule according to the force applied and the speeds
        self.speed += self.F/self.m*self.dt
        self.pos += self.speed*self.dt
                        
    def move_one_turn(self): #Executes a loop of the principle
        self.position_to_density()
        self.compute_ElectricField()
        self.field_to_particules()
        self.move_particules()
        self.timestamp += 1
        self.save_to_array()

        
    def save_to_text(self):
        np.savetxt("../results/position.dat", self.positionsstored)
        np.savetxt("../results/speed.dat", self.speedstored)
            
 
           
plasma = Plasma(q = -1,m = 1,dx = 1,dt = 1,n = 100,N = 1000,T = 10,eps0 = 8.854e-8,pos_init = np.linspace(0,100,1000,endpoint=False),speed_init = np.zeros(1000))
plasma.move_one_turn()
plasma.save_to_text()