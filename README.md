# Asymmetric interst rates - Pricing an European call option.

### Disclaimer
Polishing of the university project on pricing an european call option with varying interest rates for borrowing and lending money. This project was initially done as part of a course in Monte Carlo methods for financial applications. Since then I have reworked some of the ideas and how it was implemented. This project is not affiliated with any institution or person from Umeå University. 

## TLDR - Installation
After downloading repo:
```
pip install requirements.txt
```
Then the modules can either be accessed (without compiling) by:
```
cd src/
python3 example.py
```
Or one can use pip to compile the module:
```
cd src/blackScholesSolver
pip install -e .
```
For all use cases, it should just work by then doing:
```
import blackScholesSolver
```

## Abstract
This project studies the application of asymmetric interest rates on the pricing of an European call option. The differing interest rates represents the realistic setting where an investor generally pays a higher interest rate when borrowing than what the investor recieves as a lender. This is applied to the Black-Scholes model. We price the European call option using numerical methods based on a Partial Differential Equation framework and a Forward Backwards Stochastic Differential Equation framework. We conclude that the interest rate for lending money has no impact on the solution since we are in fact never lending money to finance the replicating trading strategy.

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
- [ ] Make repo public.
- [ ] Get the documentation up.
- [ ] Integrate fields for error handling.


Probably a lot more to do real soon.