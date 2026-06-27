import numpy as np
from typing import Callable, List, Union, Tuple, Optional, Generator
from numpy.typing import DTypeLike, ArrayLike
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib import cm

"""
The PDE solution to the Lender and Borrower interest rates
"""
### Start: Auxiliary functions for PDE solver
def getDx(Ns: int) -> np.array:
    """
    Constructs the Auxiliary linear operator used for computing the finite differences for the PDE solver. This is simply the 
    tridiagonal tri(-1,0,1).
    Parameters:
    -----------
    Ns : int
        Number of inner points in the spatial domain
    Returns:
    --------
    np.array(Ns, Ns) : 
        Auxiliary linear operator  
    """
    Dx = (
        np.diag(np.ones(Ns)*0) 
        + np.diag(np.ones(Ns-1)*-1, k=-1) 
        + np.diag(np.ones(Ns-1)*1, k=1)
        )

    return Dx

def getDxx(Ns: int) -> np.array:
    """
    Constructs the Auxiliary linear operator used for computing the finite differences for the PDE solver. This is simply the 
    tridiagonal tri(1,-2,1).
    Parameters:
    -----------
    Ns : int
        Number of inner points in the spatial domain
    Returns:
    --------
    np.array(Ns, Ns) : 
        Auxiliary linear operator  
    """
    Dxx = (
            np.diag(np.ones(Ns)*-2) 
           + np.diag(np.ones(Ns-1)*1, k=-1) 
           + np.diag(np.ones(Ns-1)*1, k=1)
           )
    return Dxx

def getDiffMat(Ns: int, 
               S: np.array, 
               h: float) -> np.array:
    """
    Constructs the Auxiliary linear operator used for computing the finite differences for u - s partial u
    Parameters:
    -----------
    Ns : int
        Number of inner points in the spatial domain
    S : np.array(Ns+2, 1)
        Spatial domain
    h : float
        Step size in the spatial domain
    Returns:
    --------
    np.array(Ns, Ns) : 
        Auxiliary linear operator  
    """
    D = (
        np.diag(np.ones(Ns)) + 
        np.diag(np.ones(Ns-1), k=1) * -S[1:-1]/(2*h)+ 
        np.diag(np.ones(Ns-1), k=-1)* S[2:]/(2*h)
        )
    return D

def terminalCondition(S: np.array, 
                      K: float) -> np.array:
    """
    The terminal condition for the PDE solver, uses the standard European call option formula max(S_T - K).
    Parameters:
    -----------
    S : np.array(Ns+2, 1)
        The spatial domain.
    K : float
        Strike price for the option
    Returns:
    --------
    np.array(Ns+2, ) : 
        The function values at the terminal time. 
    """
    return np.maximum(S - K, 0)

def leftBound(s: float, 
              t: float) -> float:
    """
    Finds the left bound of the function on the spatial domain. We currently set it to zero since the lower bound should be out of money. 
    Parameters:
    -----------
    s : float
        Stock price
    t : float
        Current time point
    Returns:
    --------
    float : 
        The left bound associated with the stock price at the current time.  
    """
    return 0

def rightBound(s: float, 
               t: float,
               K: float,
               R: float,
               T: float) -> float:
    """
    Finds the right bound of the function on the spatial domain. We currently use the 
    stock price minus the discounted strike price.
    Parameters:
    -----------
    s : float
        Stock price
    t : float
        Current time point
    K : float
        Strike price of option
    R : float
        Borrower interest rate
    T : float
        Time of maturity
    Returns:
    --------
    float : 
        The right bound associated with the stock price at the current time.  
    """
    return s - K*np.exp(-R*(T-t))

def rate(x: np.array, 
         R: float, 
         r: float) -> np.array:
    """
    Returns the interest rate for each component of the vector x.
    Parameters:
    -----------
    x : np.array(Ns, )
        The values of the finite difference approximation of the u - s partial_s u
    R : float
        Borrower interest rate
    r : float
        Lending interest rate
    Returns:
    --------
    np.array(Ns, 1)
        The interest rate associated with every spatial component of the column vector. 
    """
    y = np.ones(x.shape)*R
    y[x >= 0] = r
    return y

def approximateOptionPrice(S0: float, 
                           s: np.array, 
                           u: np.array,
                           ds: float) -> float:
    """
    Approximates the value of the call option for the spot price S0. 
    Using second degree taylor expansion with the derivatives approximated by finite differences.
    Parameters:
    -----------
    S0 : float
        Spot price of the stock.
    s : np.array(Ns+2, )
        Spatial domain
    u : np.array (Ns+2, Nt+1)
        Array of numerical option price
    ds : float
        Spatial grid step size
    Returns:
    --------
    float : 
        Approximative option price given spot price S0
    """
    # Closest point
    c = (np.abs(s - S0)).argmin()
    
    # First derivative (central difference)
    df = (u[c+1, 0] - u[c-1, 0])/(2*ds)

    # Second derivative (second degree central diff)
    ddf = (u[c+1, 0] - 2*u[c, 0] + u[c-1, 0])/(ds**2)

    u0 = u[c, 0] + (S0 - s[c])*df + 1/2 * (S0 - s[c])**2 * ddf

    return u0
### End: Auxiliary functions for PDE solver

### Start: PDE solver
def PDEsolver(S0: float, 
              K: float, 
              sigma: float, 
              R: float, 
              r: float, 
              Ns: int, 
              S_min: float, 
              S_max: float, 
              Nt: int, 
              t_min: float, 
              t_max: float, 
              theta: float) -> tuple[float, np.array, np.array, np.array]:
    """
    PDE solver for the Borrower and Lender interest rates problem. 
    Uses finite differences theta scheme to find a numerical solution. 
    Parameters:
    -----------
    S0 : float
        Spot price of the stock.
    Ns : int
        Number of inner grid points for the spatial domain
    S_min : float
        Left bound of the spatial domain
    S_max : float
        Right bound of the spatial domain
    Nt : int
        Number of gridpoints for the time domain.
    t_min : float
        Left bound of the time domain.
    t_max : float
        Right bound of the time domain.
    theta : float [0,1]
        The character of the theta scheme, 1/2 for crank-nicolson
    Returns:
    --------
    float : 
        Option price given the spot price
    np.array(Nt+1, 1) :
        Time domain
    np.array(Ns+2, 1) :
        Spatial domain
    np.array(Ns+2, Nt+1) : 
        Array of the function value of the solution function 
    """
    # Auxiliary matrices for the linear system
    Dx = getDx(Ns)
    Dxx = getDxx(Ns)

    # Space and time domain set up
    s = np.linspace(S_min, S_max, Ns+2, endpoint=True)
    h = (S_max - S_min)/(Ns+1)

    t = np.linspace(t_min, t_max, Nt+1, endpoint=True)
    dt = t_max/Nt
    
    # Function domain and terminal condition
    u = np.zeros((Ns+2, Nt+1))
    u[:, -1] = terminalCondition(s, K)

    # For the auxiliary vectors containing the impact from the boundaries.
    B = np.zeros(Ns)
    a_bar = 1/2 * sigma**2 * s[1:-1]**2

    # For determening the sign of rho (interest rate)
    Du = getDiffMat(Ns, s, h)
    d = np.zeros(Ns)
    d[0] = s[1]/(2*h)
    d[-1] = -s[-2]/(2*h)
    
    for n in range(len(t)-1, 0, -1):
        # Boundaries for next time step
        u[0, n-1] = leftBound(s[0], t[n-1])
        u[-1, n-1] = rightBound(s[-1], t[n-1], K, R, t_max)

        # Determening the rate, using previous (current time-step)
        rho = Du @ u[1:-1, n] + d*u[1:-1, n-1]
        ri = rate(rho, R, r)

        # Constructing the full linear operator used in the scheme
        Adx = (1/(h**2) * np.diag(a_bar) @ Dxx + 
               1/(2*h) * np.diag(np.ones(Ns))*s[1:-1]*ri @ Dx - 
               np.diag(np.ones(Ns))*ri
               )
        # Linear system matrices
        M1 = (np.eye(Ns) - theta*dt*Adx)
        M2 = (np.eye(Ns) + (1 - theta)*dt*Adx)

        # Coefficents used by auxiliary vectors
        a = (1/2 * sigma**2 * s[1]**2 / h**2) - (ri[0] * s[1] / (2 * h))
        g = (1/2 * sigma**2 * s[-2]**2 / h**2) + (ri[-1] * s[-2] / (2 * h))

        # Auxiliary vectors 
        B_n = B
        B_n[0] = a * u[0, n]
        B_n[-1] = g * u[-1, n]

        B_nm1 = B
        B_nm1[0] = a * u[0, n-1]
        B_nm1[-1] = g * u[-1, n-1]

        # Solving linear system
        rhs = M2 @ u[1:-1, n] + dt * (theta * B_nm1 + (1 - theta) * B_n)
        u[1:-1, n-1] = np.linalg.solve(M1, rhs)

    # Finds option price associated with spot price.
    u0 = approximateOptionPrice(S0, s, u, h)

    return u0, t, s, u
    
### End: PDE solver


def main():

    pass


if __name__ == "__main__":
    main()
