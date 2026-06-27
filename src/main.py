
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List, Union, Tuple, Optional, Generator
from numpy.typing import DTypeLike, ArrayLike
from scipy.stats import norm
from matplotlib import cm
import scienceplots

from PDE import PDEsolver
from FBSDE import FBSDEsolver

"""
Main file for the project - Lender and Borrower Interest Rates
For the different implementations namely PDE and FBSDE see the respecitive files. 
This file contains the code for the different tests and illustrations used throughout the report. 
"""

plt.style.use('science')

""" Start: Global parameters """
# Parameters used throughout the assignment. 
T = 0.5
mu = 0.06
sigma = 0.2
r = 0.04
R = 0.06
K = 100
S0 = 100
""" End: Global parameters"""


### Start: Validation functionality
def analyticalSolution(S0, K, r, s, T):
    d1 = (np.log(S0/K) + (r + 1/2 * s**2)*T)/(s*np.sqrt(T))
    d2 = d1 - s*np.sqrt(T)

    return S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

def error(u, K, S, r, s, T):
    """
    Root mean square error for the implementation
    """
    n = u.shape[0]
    errs = np.zeros(n)

    for i in range(n):
        err = u[i, 0] - analyticalSolution(S[i], K, R, s, T)

        errs[i] = err**2
    
    RMSE = np.sqrt(np.mean(errs))
    print(f"RMSE: {RMSE}")
    return RMSE

### End: Validation functionality

### Start: Functions used for the result section of the report for PDE
def plotSurface(s, t, u):
    """
    Surface plot of the solution function
    """
    X, Y = np.meshgrid(s, t)
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(Y, X, u.T, vmin=u.min() * 2, cmap=cm.coolwarm)

    ax.set_xlabel("Time (t)")
    ax.set_ylabel("Stock price (S)")
    ax.set_zlabel("Option price (u(x,t))")

    plt.title("Surface plot of option pricing")
    plt.legend(["Option price function"])

    plt.show()

def gettingSurfacePlot():
    """
    Surface plot for the lab report
    """
    # Numeric scheme parameters
    Nt = 100
    Ns = 1000
    theta = 1/2
    s_max = 1000
    s_min = 1
    t_max = T
    t_min = 0

    u0, t, s, u = PDEsolver(S0, K, sigma, R, r, Ns, s_min, s_max, Nt, t_min, t_max, theta)

    plotSurface(s, t, u)

def comparingCurvesBetweenAnalyticalAndNumerical():
    """
    Function for plotting the different curves at time 0, specifically the difference between the numerical solution and the analytical solution.
    """
    Nt = 1000
    Ns = 1000
    theta = 1/2
    s_max = 1000
    s_min = 1
    t_max = T
    t_min = 0

    u0, t, s, u = PDEsolver(S0, K, sigma, R, r, Ns, s_min, s_max, Nt, t_min, t_max, theta)

    analytical_curve = np.zeros(s.shape)
    for i in range(len(s)):
        analytical_curve[i] = analyticalSolution(s[i], K, r, sigma, T)
    
    plt.plot(s, u[:, 0], s, analytical_curve)
    plt.xlim([1, 200])
    plt.ylim([0, 200])
    plt.legend(["Numerical solution", "Analytical solution"])
    plt.title("Comparison between numerical and analytical solution")
    plt.xlabel("Stock price (S)")
    plt.ylabel("Option price")
    plt.show()

def convergenceWithRMSE():
    """
    Function finding the root mean square error using different step sizes and studying the convergence of the solution.
    """
    Nt = 1000
    Ns = 1000
    theta = 1/2
    s_max = 1000
    s_min = 1
    t_max = T
    t_min = 0

    Ns = [20, 50, 80, 100, 200, 500, 800, 1000]
    res = np.zeros((len(Ns),1))
    for i in range(len(Ns)):
        _, t, s, u = PDEsolver(S0, K, sigma, R, r, Ns[i], s_min, s_max, Nt, t_min, t_max, theta)
        res[i, 0] = error(u, K, s, R, sigma, T)
        print(f"Progress: {(i+1)/len(Ns) * 100}%")
    
    out = np.hstack((np.reshape(np.array(Ns), (len(Ns), 1)), res))
    _ = numpy_to_latex_table(out)
    plt.loglog(Ns, res)
    plt.legend(["RMSE"])
    plt.title("RMSE for decreasing spatial step size")
    plt.xlabel("Number of gridpoints")
    plt.ylabel("RMSE")
    plt.show()

### End: Functions used for the result section of the report for PDE

### Start: Functions for outputting tables in latex
def numpy_to_latex_table(array, caption=None, label=None, decimals=5):
    """
    Convert a NumPy array into a LaTeX tabular environment.

    Parameters
    ----------
    array : np.ndarray
        1D or 2D NumPy array
    caption : str, optional
        Table caption
    label : str, optional
        Table label
    decimals : int
        Number of decimals for floats
    """

    array = np.asarray(array)

    # Convert 1D array to 2D row vector
    if array.ndim == 1:
        array = array.reshape(1, -1)

    rows, cols = array.shape

    # Column alignment string
    alignment = "c" * cols

    latex = []

    latex.append(r"\begin{table}[h!]")
    latex.append(r"\centering")
    latex.append(rf"\begin{{tabular}}{{{alignment}}}")
    latex.append(r"\hline")

    for row in array:
        formatted_row = []

        for item in row:
            if isinstance(item, (float, np.floating)):
                formatted_row.append(f"{item:.{decimals}f}")
            else:
                formatted_row.append(str(item))

        latex.append(" & ".join(formatted_row) + r" \\")
    
    latex.append(r"\hline")
    latex.append(r"\end{tabular}")

    if caption is not None:
        latex.append(rf"\caption{{{caption}}}")

    if label is not None:
        latex.append(rf"\label{{{label}}}")

    latex.append(r"\end{table}")

    latex_code = "\n".join(latex)

    print(latex_code)

    return latex_code
### End: Functions for outputting tables in latex

def confInt():
    """
    Finding montecarlo estimate for the FBSDE approach with the corresponding confidence interval
    """
    N = 100
    n = 100
    M = 200000 
    
    res = np.zeros(N)

    for i in range(N):

        res[i] = FBSDEsolver(S0, K, mu, sigma, R, r, T, M, n)

        print(f"Progress: {( i +1)/ (N) * 100:.2f}%")

    print(np.mean(res), np.std(res))

    x_bar = np.mean(res)
    x_std = np.std(res)

    SE = x_std / np.sqrt(N)

    c = norm.ppf(0.975)

    print(f"Confidence interval:\n [{x_bar - c*SE:.4f}, {x_bar + c*SE:.4f}]")

    plt.hist(res)
    plt.show()

def convergenceOfFBSDE():
    N = 100
    n = 100
    M = 20000
    m = 10
    
    res = np.zeros((m, N))
    for j in range(m):
        for i in range(N):
            
            res[j, i] = FBSDEsolver(S0, K, mu, sigma, R, r, T, M*(j+1), n)

            print(f"Progress: {((i +1) + N * (j))/ (N * m) * 100:.2f}%")

    sol = analyticalSolution(S0, K, R, sigma, T)
    RMSE = np.zeros(m)
    for i in range(m):
        err = (res[i, :] - sol)**2
        RMSE[i] = np.sqrt(np.mean(err))

    print(np.mean(res, axis=1), np.std(res, axis=1)) 
    print(RMSE)
    Mr = np.linspace(M, m*M, m, endpoint=True)
    plt.loglog(Mr, RMSE/np.sqrt(Mr))
    plt.legend(["RMSE"])
    plt.xlabel("Number of trajectories")
    plt.ylabel("RMSE")
    plt.title("RMSE for increasing number of paths")
    plt.show()
def main():
    Nt = 100
    Ns = 1000
    theta = 1/2
    s_max = 1000
    s_min = 1
    t_max = T
    t_min = 0

    u0, _, _, _  = PDEsolver(S0, K, sigma, R, r, Ns, s_min, s_max, Nt, t_min, t_max, theta)
    print(u0)
if __name__ == "__main__":
    main()