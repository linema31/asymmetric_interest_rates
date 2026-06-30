from dataclasses import dataclass

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
    M = 1000
    N = 100

    def extractParams(self):
        return (self.M, self.N)