
import numpy as np
from typing import Callable, List, Union, Tuple, Optional, Generator
from numpy.typing import DTypeLike, ArrayLike
from scipy.stats import norm

import matplotlib.pyplot as plt

from forward import blackScholes, generateBrownianMotion

"""
The FBSDE solution to the Lender and Borrower interest rates.
"""

def leastSquareRegression(response: np.array, 
                          independent: np.array, 
                          predictor: np.array) -> np.array:
    """
    Least-square regression using independent variables to degree two for response variables, 
    to then use predictor variables to estimate the conditional expectation. 
    Parameters:
    -----------
    response : np.array (M, )
        Response variables, for implementation either Y_{t_i+1} or dWt_I * Y_{t_i+1}
    independent : np.array (M, )
        Independent variables, for implementation S_{ti+1} 
    predictor : np.array (M, )
        Predictor variables, for implementation S_{ti}
    Returns:
    --------
    np.array
        The estimated conditional expectation of the respons given the predictor variables
    """
    # Constructing feature array, first parameter constant (1), second parameter S_ti, third parameter S_ti^2
    M = independent.shape[0]
    reg_array = np.ones((M, 3))
    reg_array[:, 1] = independent
    reg_array[:, 2] = independent**2

    beta = np.linalg.lstsq(reg_array, response)[0]

    # Constructing feature array for the predicting
    pred_array = np.ones((M, 3))
    pred_array[:, 1] = predictor
    pred_array[:, 2] = predictor**2

    # Predicting
    cond_est = pred_array @ beta

    return cond_est

def nonLinearFunction(t: float, 
                      y: np.array, 
                      z: np.array,
                      mu: float,
                      sigma: float,
                      r: float,
                      R: float) -> np.array:
    """
    The non-linear funciton described in the assignment.
    Parameters:
    -----------
    t : float
        Representing time
    y : np.array
        Vector-version of the estimated price process at time t.
    z : np.array
        Vector-version of the hedging process at time t.
    mu : float
        Drift constant for the driving SDE.
    sigma : float
        Volatility of the model
    r : float
        Lending interest rate
    R : float
        Borrowing interest rate
    Returns:
    --------
    np.array
        The resulting real-valued vector
    """
    lam = (mu - r)/sigma
    return -(y*r + z*lam + np.minimum( y - z/sigma, 0)*(R-r))


def estimateHedge(dt: float, 
                  response: np.array, 
                  independent: np.array, 
                  predictor: np.array) -> np.array:
    """
    Estimates the hedge Z_ti using the conditional expectation for Y_ti+1*dWt

    Parameters:
    -----------
    dt : float
    response : np.array
        Y_ti+1 * dWt
    independent : np.array
        St_i+1
    predictor : np.array
        St_i
    Returns:
    --------
    np.array
        Vectorized Z_{ti} 
    """

    return 1/dt * leastSquareRegression(response, independent, predictor)

def payOff(ST: np.array, 
           K: float) -> np.array:
    """
    Pay-off function. European call option with strike price K. CT = max(ST - K, 0)
    Parameters:
    -----------
    ST : np.array (M,)
        The stockprice at maturity time T. 
    K : float
        The strike price for the call option.
    Returns:
    --------
    np.array (M, )
        The pay-off for each trajectory.
    """

    return np.maximum(ST-K, 0)


def FBSDEsolver(S0: float, 
                K: float, 
                mu: float, 
                sigma: float, 
                R: float, 
                r: float, 
                T: float,
                M: int, 
                N: int) -> tuple[float, np.array, np.array]:
    """
    Iterative scheme for finding the solution to the FBSDE approach.
    Parameters:
    -----------
    S0 : float
        Spot price for the stock
    K : float
        Strike price for the option
    mu : float
        Drift term coefficient of the SDE. 
    sigma : float
        Volatility of the SDE
    R : float
        Borrower interest rate
    r : float
        Lender interest rate
    T : float
        Maturity time
    M : int
        Number of trajectories
    N : int
        Number of time steps
    Returns:
    --------
    float : 
        The approximated option price.
    np.array(M, N) : 
        The pricing process for all M trajectories.
    np.array(M, N-1) :
        The hedging process for all M trajectories.
    """
    # Time domain, grid and step size
    dt = T/(N-1)

    # Generate driving brownians and driving SDE for the stock.
    dW, Wt = generateBrownianMotion(T, N, M)
    St = blackScholes(S0, T, mu, sigma, dW, N, M)
    
    # Initializing processes
    Yt = np.zeros((M, N))
    Zt = np.zeros((M, N-1))

    # Terminal payoff
    Yt[:, -1] = payOff(St[:, -1], K)

    # Iterative scheme
    for j in range(N-2, -1, -1):
        Yt_cond = leastSquareRegression(Yt[:, j+1], St[:, j], St[:, j])
        Zt[:, j] = estimateHedge(dt, dW[:, j]*Yt[:, j+1], St[:, j], St[:, j])
        Yt[:, j] = Yt_cond + nonLinearFunction(j*dt, Yt[:, j+1], Zt[:, j], mu, sigma, r, R)*dt
    
    return np.mean(Yt[:, 0]), Yt, Zt


def main():
    pass

if __name__ == "__main__":
    main()
