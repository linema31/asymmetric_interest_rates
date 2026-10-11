from blackScholesSolver import modelConfig, pdeConfig, fbsdeConfig, PDEsolver, FBSDEsolver

"""
Example usage of the implementations for the Lender and Borrower interest rates
"""

def main():
    """
    Function for showing example use of the implementations. 
    Initially introducing the model parameters and the implementation specific parameters.
    Then using the different solvers along with the analytical solution seen above.
    
    A pretty light workload, around 10 seconds on an average laptop. 
    """

    mod_conf = modelConfig()
    
    pde_conf = pdeConfig()

    fbsde_conf = fbsdeConfig()

    u0, t, s, u = PDEsolver(mod_conf, pde_conf)

    Y0, Yt, Zt = FBSDEsolver(mod_conf, fbsde_conf)

    print(f"PDE price: {u0:.4f}")
    print(f"FBSDE price: {Y0:.4f}")


if __name__ == "__main__":
    main()
