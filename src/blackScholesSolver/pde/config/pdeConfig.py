
from dataclasses import dataclass

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
    Nt = 100
    Ns = 1000
    theta = 1/2
    s_max = 1000
    s_min = 1
    t_max = 0.5
    t_min = 0

    def extractParams(self):
        """
        Extracts the parameters of the config class.
        """
        return (self.Ns, self.s_min, self.s_max, self.Nt, self.t_min, self.t_max, self.theta)