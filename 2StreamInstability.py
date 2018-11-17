
Spyder Editor


"""
import numpy as np
import matplotlib.pyplot as plt

#   Defining constants

dx = 1.0
dk = 1.0
dt = 1.0
n = 1000
N = 10000
X = np.linspace(0,n*dx,n)
eps0 = 8.854e-8

#   Initializing variables

pos = np.zeros(N)
rho = np.zeros(n)
rho_ = np.zeros(n)
phi = np.zeros(n)
phi_ = np.zeros(n)
E = np.zeros(n)

# Moving from dt

def compute_ElectricField(rho):
    rho_ = np.fft.fft(rho)
    K = np.fft.fftfreq(n,dx)*2*np.pi
    phi_[1:] = rho_[1:]/eps0/K[1:]**2
    phi = np.fft.ifft(phi_).real
    E = (np.roll(phi,1)-np.roll(phi,-1))/2/dx        # E(x) = - (phi(x+dx)-phi(x-dx)/2dx)
    return E

