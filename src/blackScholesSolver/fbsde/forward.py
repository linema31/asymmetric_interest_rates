import numpy as np
from typing import Union, Tuple

"""
Code for the forward part of the FBSDE
Generating brownian motion and exact simulation of GBM.
"""

def generateBrownianMotion(T:Union[float,np.ndarray], 
                    N:int, 
                    M:int)->Tuple[np.ndarray, np.ndarray]:
    """Generate Brownian motion paths.
    
    Parameters
    ----------
    T : float
        The time horizon.
    N : int
        The number of time steps.
    M : int
        The number of paths.
    
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        The Brownian motion increments and paths.
        Shape of increments: (M, N-1), shape of paths: (M, N)
    """
    # Time-steps
    dt = T/(N-1)

    # Timegrid
    t = np.linspace(0, T, N)

    # Increments
    dWt = np.random.normal(0, np.sqrt(dt), (M, N-1))
    
    # Paths
    Wt = np.zeros((M, N))
    Wt[:, 1:] = np.cumsum(dWt, axis=1)

    return (dWt, Wt) 

def blackScholes(S0:float, 
                 T:float, 
                 mu:float, 
                 sigma:float, 
                 dW: np.array, 
                 N:int, 
                 M:int)->np.array:
    """Simulates M trajectories of the Black-Scholes model with N steps to terminal time T using explicit solution.
    Parameters
    ----------
    S0 : float
        The initial stock price.
    T : float
        The terminal time.
    mu : float
        Parameter of process
    sigma : float
        The volatility of the stock.
    dW : float
        Brownian motion increments 
    N : int
        Number of time-steps
    M : int
        The number of Monte Carlo simulations to perform.
    seed: int (Optional)
        Set seed for debugging, default None
        
    Returns
    -------
    np.array(M, N) :
        Trajectories of the Black-Scholes model
    """

    # Time-steps
    dt = T/(N-1)

    # Initialize trajectories
    St = np.zeros((M, N))
    St[:, 0] = S0
    # Using explicit formula to derive the next iteration of trajectories. 
    for j in range(N-1):
        St[:, j+1] = St[:, j]*np.exp(dt*(mu - sigma**2 / 2) + sigma *dW[:, j])
    
    return St
