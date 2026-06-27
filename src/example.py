import numpy as np
from typing import Callable, List, Union, Tuple, Optional, Generator
from numpy.typing import DTypeLike, ArrayLike
from scipy.stats import norm

from PDE import PDEsolver
from FBSDE import FBSDEsolver

"""
Example usage of the implementations for the Lender and Borrower interest rates
"""
def analyticalSolution(S0, K, r, s, T):
    """
    Analytical solution of the European option price in the Black-Scholes model. 
    """
    d1 = (np.log(S0/K) + (r + 1/2 * s**2)*T)/(s*np.sqrt(T))
    d2 = d1 - s*np.sqrt(T)

    return S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

def main():
    """
    Function for showing example use of the implementations. 
    Initially introducing the model parameters and the implementation specific parameters.
    Then using the different solvers along with the analytical solution seen above.
    
    A pretty light workload, around 10 seconds on an average laptop. 
    """
    
    # Model params
    T = 0.5
    mu = 0.06
    sigma = 0.2
    r = 0.04
    R = 0.06
    K = 100
    S0 = 100

    # PDE-scheme params
    Nt = 100
    Ns = 1000
    theta = 1/2
    s_max = 1000
    s_min = 1
    t_max = T
    t_min = 0

    # PDE numerical solution
    u0, t, s, u = PDEsolver(S0, K, sigma, R, r, Ns, s_min, s_max, Nt, t_min, t_max, theta)

    # FBSDE-scheme params
    N = 100
    M = 200000 

    # FBSDE numerical solution
    Y0, Yt, Zt = FBSDEsolver(S0, K, mu, sigma, R, r, T, M, N)

    print(f"PDE numerical solution: {u0:.4f}\nFBSDE numerical solution: {Y0:.4f}\nAnalytical solution: {analyticalSolution(S0, K, R, sigma, T):.4f}")


if __name__ == "__main__":
    main()