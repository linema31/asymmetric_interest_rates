from dataclasses import dataclass

@dataclass
class modelConfig:
    """
    Black Scholes model parameters
    --------------
    T : float
        Maturity time of the option.
    sigma : float
        Volatility of the asset.
    r : float
        Lending interest rate
    R : float
        Borrowing interest rate
    mu : float
        Drift of the asset. 
    K : float
        Strike price
    S0 : float
        Initial stock price 
    """
    T = 0.5
    sigma = 0.2
    r = 0.04
    R = 0.06
    mu = 0.06
    K = 100
    S0 = 100
