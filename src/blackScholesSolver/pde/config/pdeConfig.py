from numbers import Real
from dataclasses import dataclass
from blackScholesSolver.errors.Errors import InvalidConfigError
@dataclass
class pdeConfig:
    """
    Pde solver model parameter
    ----------
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
    """
    Nt: int = 100
    Ns: int = 1000
    theta: float = 1/2
    s_max: float = 1000
    s_min: float = 1
    t_max: float = 0.5
    t_min: float  = 0

    def __post_init__(self):
        """
        Pde model validation.
        """
        self.params = [self.Ns, self.s_min, self.s_max, self.Nt, self.t_min, self.t_max, self.theta]
        self._checkReal()
        self._checkProperValues()

    def _checkReal(self):
        """
        Checks such that all parameters are real and that the integers are indeed integers.
        """
        for par in self.params:
            if not isinstance(par, Real):
                raise InvalidConfigError("Pde parameters must be real numbers")
        
        if not isinstance(self.Ns, int):
            raise InvalidConfigError(f"{self.Ns!r} must be an integer.")
        elif not isinstance(self.Nt, int):
            raise InvalidConfigError(f"{self.Nt!r} must be an integer.")

    def _checkProperValues(self):
        """
        Checks such that all parameters are positive and that the theta variable is between 0 and 1.
        """

        for par in self.params:
            if par < 0:
                raise InvalidConfigError("Parameters must be non-zero.")
        
        if self.theta > 1:
            raise InvalidConfigError("Theta parameter must be between 0 and 1.")
    def extractParams(self):
        """
        Extracts the parameters of the config class.
        """
        return self.params 