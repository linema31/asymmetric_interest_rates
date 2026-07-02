# Asymmetric interst rates - Pricing an European call option.

### Disclaimer
Polishing of the university project on pricing an european call option with varying interest rates for borrowing and lending money. This project was initially done as part of a course in Monte Carlo methods for financial applications. Since then I have reworked some of the ideas and how it was implemented. This project is not affiliated with any institution or person from Umeå University. 


## Project documentation
For more in depth explanation and reasoning surrounding the problem and solutions, see the report in `docs/`.
## Workflow left to do
Below is what is left to do for this project.
### Done
- [x] Config class for the pde solver
- [x] Config implementation for fbsde solver
- [x] Handle user error when configuring model parameters, for all numerical tests and actual model params. 

### Left to do
- [ ] Polish both implementations a bit more.
- [ ] Add testing.
- [ ] Make repo public.
- [ ] Get the documentation up.
- [ ] Integrate fields for error handling.


Probably a lot more to do real soon.

Below is the Polished README:

# Black-Scholes Solvers

> Numerical implementations of the Black-Scholes model using both a finite difference (PDE) solver and a Forward-Backward Stochastic Differential Equation (FBSDE) solver.

---

## Overview

This project studies the application of asymmetric interest rates on the pricing of an European call option. The differing interest rates represents the realistic setting where an investor generally pays a higher interest rate when borrowing than what the investor recieves as a lender. This is applied to the Black-Scholes model. We price the European call option using numerical methods based on a Partial Differential Equation framework and a Forward Backwards Stochastic Differential Equation framework. We conclude that the interest rate for lending money has no impact on the solution since we are in fact never lending money to finance the replicating trading strategy.

>The project originated as part of a university course in computational finance and has since been refactored into a reusable Python package with improved software architecture, documentation, validation, and examples.

---

## Features

- Finite Difference (PDE) solver. Including Crank Nicolson, Explicit- and Implicit Euler. 
- FBSDE solver.
- Configurable model parameters.
- Input validation.
- Example script.
- Modular package structure

---

## Repository Structure

```text
.
├── examples/
├── docs/
|-- figures/
├── src/
│   └── blackScholesSolver/
│       ├── config/
│       ├── pde/
│       ├── fbsde/
│       ├── 
│       └── ...
├── tests/
├── README.md
└── pyproject.toml
```

To briefly explain the structure of the repository:
- `docs/` - Contains the report associated with the project.
- `figures/` - Contains the Figures used throughout the Result section of this README.md.
- `src/blackScholesSolver/` - Contains the source code of the project.  

---

## Installation

Explain how to clone and install the project.

```bash
git clone ...
cd ...

pip install -e .
```

or

```bash
pip install -r requirements.txt
```

Mention supported Python version if applicable.

---

## Quick Start

```python
from blackScholesSolver import modelConfig, pdeConfig, fbsdeConfig, PDEsolver, FBSDEsolver

mod_config = modelConfig()

pde_config = pdeConfig()

fbsde_config = fbsdeConfig()

u0, t, s, u = PDEsolver(mod_config, pde_config)

Y0, Yt, Zt = FBSDEsolver(mod_config, fbsde_config)

print(f"Price using pde: {u0:.4f}\n")
print(f"Price using fbsde: {Y0:.4f}\n")

```

---

## Examples

Describe the available example scripts.

For example:

- Basic PDE pricing
- Basic FBSDE pricing
- Parameter comparison
- Convergence study
- Runtime comparison

---

## Mathematical Background

Provide a high-level explanation of the implemented methods.

Keep this concise.

Point interested readers to the report for derivations.

Example:

>The PDE solver discretizes the Black-Scholes equation using finite differences.
>The stochastic solver reformulates the pricing problem as an FBSDE.

For complete derivations, see:

```
report/report.pdf
```

---

## Results

Present the most important numerical results.

Possible content:

- Pricing accuracy
- Runtime comparison
- Convergence plots
- Error analysis

Include figures if possible.

Example:

![Convergence](images/convergence.png)

---

## Design Decisions

Explain the software architecture.

Possible topics:

- Why dataclasses were used for configuration
- Validation strategy
- Package organization
- Separation between models and solvers
- Choice of numerical methods

This section demonstrates software engineering rather than mathematics.

---

## Testing

Describe the testing strategy.

Example:

```bash
pytest
```

Mention what kinds of functionality are tested.

---

## Future Improvements

Ideas that could naturally extend the project.

Example:

- American options
- Barrier options
- GPU acceleration
- Adaptive meshing
- Additional stochastic volatility models

---

## Educational Context

Briefly explain the project's origin.

Example:

>This repository originated from a university laboratory project in computational finance. The codebase has since been substantially refactored with improved software architecture, documentation, validation, and packaging. The repository is maintained independently and is not affiliated with or endorsed by the university.

---

## References

Include references to:

- Black & Scholes (1973)
- Any textbooks
- Numerical methods references
- Course report

---

## License

Specify the license.

Example:

MIT License

---

## Author

Your name

Short sentence about the project.

Optionally include links to:

- LinkedIn
- Personal website
- Other repositories