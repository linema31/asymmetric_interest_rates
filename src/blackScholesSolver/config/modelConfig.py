from dataclasses import dataclass
from numbers import Real
from blackScholesSolver.errors.Errors import InvalidConfigError

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
    T: float = 0.5
    sigma: float = 0.2
    r: float = 0.04
    R: float = 0.06
    mu: float = 0.06
    K: float = 100
    S0: float = 100

    

    def __post_init__(self):
        """
        Model config validation
        """
        self.params = [self.S0, self.K, self.sigma, self.R, self.r, self.mu, self.T]
        self._checkDatatype()
        self._checkPositivity()

    def _checkDatatype(self):
        """
        Validates that the user input is of the correct datatype.
        """

        for par in self.params:
            
            if not isinstance(par, Real):
                raise InvalidConfigError("Parameters must be of type float or integer.")

    def _checkPositivity(self):
        """
        Since all parameters of the model must be positive we perform validation.
        """
        for par in self.params:
            if not par >= 0:
                raise InvalidConfigError("Parameters must be greater or equal to zero.")
            
    def extractParams(self):
        """
        Extracts model parameters.
        """
        
        return self.params 
