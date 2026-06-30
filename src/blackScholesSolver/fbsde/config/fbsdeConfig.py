from dataclasses import dataclass

from blackScholesSolver.errors.Errors import InvalidConfigError
@dataclass
class fbsdeConfig:
    """
    Numerical solver specific parameters.
    Parameters:
    -----------
    M : int
        Number of trajectories
    N : int
        Number of timesteps
    """
    M: int = 1000
    N: int = 100

    def __post_init__(self):
        """
        Config validation
        """
        self.params = [self.M, self.N]

        for par in self.params:
            try:
                if par <= 0:
                    raise InvalidConfigError("Fbsde Parameters must be greater than zero.")
            except TypeError:
                raise InvalidConfigError("Fbsde parameters must be integer.")
            if not isinstance(par, int):
                raise InvalidConfigError("Fbsde parameters must be integers.")

    def extractParams(self):
        return self.params