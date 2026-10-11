# Asymmetric Interest Rates for European Call Option Pricing

> Numerical implementations of a finite-difference PDE solver and a forward-backward stochastic differential equation (FBSDE) solver for pricing a European call option with asymmetric borrowing and lending rates.

---

## Overview

This project studies European call option pricing in a Black–Scholes framework with asymmetric borrowing and lending interest rates. The model reflects the common setting in which the borrowing rate is higher than the lending rate.

Two numerical approaches are implemented: a finite-difference solver for the associated nonlinear partial differential equation (PDE) and a forward-backward stochastic differential equation (FBSDE) solver. For the studied pricing problem, both approaches agree with the Black–Scholes price obtained using the borrowing rate: the replicating strategy does not enter a lending position, so the lending rate does not affect the option value.

---

## Features

- Finite-difference PDE solver with Crank–Nicolson, explicit Euler, and implicit Euler schemes
- FBSDE solver based on Monte Carlo simulation and least-squares polynomial regression
- Configurable model and solver parameters
- Input validation for configuration parameters
- Runnable example

---

## Repository Structure

```text
docs/
figures/
src/
    blackScholesSolver/
        config/
        errors/
        fbsde/
        pde/
    examples/
```

- `docs/` contains the accompanying project report.
- `figures/` contains the figures displayed in this README.
- `src/blackScholesSolver/` contains the solver implementation.
- `src/examples/` contains runnable examples.

---

## Installation

```bash
git clone https://github.com/linema31/asymmetric_interest_rates.git
cd asymmetric_interest_rates
python3 -m pip install -r requirements.txt
```

## Run the example

```bash
cd src
python3 -m examples.example
```

## Quick Start

```python
from blackScholesSolver import modelConfig, pdeConfig, fbsdeConfig, PDEsolver, FBSDEsolver

mod_config = modelConfig()

pde_config = pdeConfig()

fbsde_config = fbsdeConfig()

u0, t, s, u = PDEsolver(mod_config, pde_config)

Y0, Yt, Zt = FBSDEsolver(mod_config, fbsde_config)

print(f"PDE price: {u0:.4f}")
print(f"FBSDE price: {Y0:.4f}")
```

---

## Mathematical Background

This section describes the pricing problem and the numerical methods implemented here. For specific details regarding the problem and solution, see `docs/lender_borrower_interest_rates.pdf`.

### Problem

This project studies the pricing of a European call option in a modified Black–Scholes framework with asymmetric borrowing and lending interest rates. Unlike the classical model, the interest rate depends on the cash position of the replicating portfolio, introducing a nonlinear term into the pricing equation.

The option price is governed by the nonlinear Black–Scholes PDE

$$
\frac{\partial u}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{ \partial^2 u}{\partial S^2} = 
\rho \left(u-S\frac{\partial u}{\partial S}\right)
\left(u-S\frac{\partial u}{\partial S}\right),
$$

where

$$
\rho(x)=
\begin{cases}
r, & x\ge0,\\
R, & x<0,
\end{cases}
\qquad R\ge r.
$$

To solve this nonlinear pricing problem, two independent numerical approaches are implemented: a deterministic PDE solver and a probabilistic FBSDE solver.

### PDE solution

The deterministic formulation is solved using a Crank–Nicolson finite-difference scheme on a uniform space-time grid. Since the active interest rate depends on the cash position, the nonlinear term is updated iteratively throughout the backward time-stepping procedure. The option price at the initial stock value is recovered using second-order Taylor interpolation.

### FBSDE solution

The probabilistic formulation is solved using a Forward–Backward Stochastic Differential Equation (FBSDE) framework. Stock price trajectories are simulated exactly under geometric Brownian motion, after which the BSDE is solved backward in time. Conditional expectations are approximated using least-squares polynomial regression, producing a Monte Carlo estimate of the option price.

## Results

The two numerical methods converge to the same solution and agree with the analytical Black–Scholes price calculated using the borrowing rate. The convergence studies show decreasing error as the PDE spatial resolution and the number of FBSDE simulation paths increase.

The following surface shows the numerical option value over the spatial and temporal grid.

<div style="text-align: center;">

![Numerical PDE solution surface](figures/res_surface_003.png "Surface plot of solution matrix.")

</div>

The following comparison shows the numerical PDE solution and the analytical Black–Scholes solution.

<div style="text-align: center;">

![Numerical PDE and analytical Black–Scholes solution comparison](figures/res_comparison_001.png "Line plot comparing analytical solution to numerical PDE solution.")

</div>

The numerical and analytical prices coincide, even though the analytical price does not account for different interest rates.

The root mean square error (RMSE) compares the analytical and numerical solutions.

<div style="text-align: center;">

![PDE RMSE convergence as spatial resolution increases](figures/res_rmse_conv_001.png "Logarithmic line plot of RMSE for increasing number of grid points.")

</div>

The RMSE plot shows that the PDE solution converges toward the analytical solution as the number of spatial grid points increases.

The FBSDE convergence study uses Monte Carlo estimates with an increasing number of simulated trajectories.

<div style="text-align: center;">

![FBSDE RMSE convergence as the number of simulated trajectories increases](figures/res_FBSDE_001.png "Logarithmic line plot of RMSE for increasing number of trajectories.")

</div>

The FBSDE convergence study shows decreasing error as the number of simulated trajectories increases.

The main conclusion is that, for this pricing problem, the lending rate has no influence on the option value because the replicating strategy never enters a lending position. Consequently, the nonlinear model produces the same price as the classical Black–Scholes model using the borrowing interest rate.

---

## Educational Context

This repository originated as a university laboratory project in computational finance and is maintained independently.

---

## Author

Linus Emanuel
