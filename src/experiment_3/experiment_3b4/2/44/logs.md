# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- The division must produce at least \var{min_batches_{p}} batches of part \var{p} each month to fulfill a contract.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this linear programming problem, we need to establish the decision variables, objective function, and constraints based on the given problem description. Let's define the decision variables and then write the mathematical model in LaTeX.

######### Decision Variables
- Let \( x_{p} \) be the number of batches of part \( p \) produced each month.

######### Objective Function
The objective is to maximize the total profit. Total profit is calculated as the difference between the revenue from selling the parts and the cost of using the machines:

\[
\text{total profit} = \sum_{p=1}^{P} (\text{price}_{p} \times x_{p}) - \sum_{m=1}^{M} (\text{cost}_{m} \times \text{total time on machine } m)
\]

Where \(\text{total time on machine } m = \sum_{p=1}^{P} (\text{time}_{m,p} \times x_{p}) \).

######### Constraints
1. Machine Availability Constraints:
   \[
   \sum_{p=1}^{P} (\text{time}_{m,p} \times x_{p}) \leq \text{available}_{m}, \quad \text{for } m = 1, \ldots, M
   \]

2. Minimum Production Requirement Constraints:
   \[
   x_{p} \geq \text{min\_batches}_{p}, \quad \text{for } p = 1, \ldots, P
   \]

3. Non-negativity Constraints:
   \[
   x_{p} \geq 0, \quad \text{for } p = 1, \ldots, P
   \]

Now, let's format this model in LaTeX.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model}

\textbf{Decision Variables:}

Let \( x_{p} \) be the number of batches of part \( p \) produced each month.

\textbf{Objective Function:}

Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} (\text{price}_{p} \times x_{p}) - \sum_{m=1}^{M} \left(\text{cost}_{m} \times \sum_{p=1}^{P} (\text{time}_{m,p} \times x_{p})\right)
\]

\textbf{Subject to:}

1. Machine Availability Constraints
\[
\sum_{p=1}^{P} (\text{time}_{m,p} \times x_{p}) \leq \text{available}_{m}, \quad \text{for } m = 1, \ldots, M
\]

2. Minimum Production Requirement Constraints
\[
x_{p} \geq \text{min\_batches}_{p}, \quad \text{for } p = 1, \ldots, P
\]

3. Non-negativity Constraints
\[
x_{p} \geq 0, \quad \text{for } p = 1, \ldots, P
\]

\end{document}
```

This LaTeX code provides a mathematical representation of the problem, including the objective function and all constraints necessary to solve for the optimal number of batches of each part to produce each month to maximize profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model}

\textbf{Decision Variables:}

Let \( x_{p} \) be the number of batches of part \( p \) produced each month.

\textbf{Objective Function:}

Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} (\text{price}_{p} \times x_{p}) - \sum_{m=1}^{M} \left(\text{cost}_{m} \times \sum_{p=1}^{P} (\text{time}_{m,p} \times x_{p})\right)
\]

\textbf{Subject to:}

1. Machine Availability Constraints
\[
\sum_{p=1}^{P} (\text{time}_{m,p} \times x_{p}) \leq \text{available}_{m}, \quad \text{for } m = 1, \ldots, M
\]

2. Minimum Production Requirement Constraints
\[
x_{p} \geq \text{min\_batches}_{p}, \quad \text{for } p = 1, \ldots, P
\]

3. Non-negativity Constraints
\[
x_{p} \geq 0, \quad \text{for } p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

#### Constants
P = len(prices)  #### Number of parts
M = len(availability)  #### Number of machines

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

#### Objective Function
profit = pulp.lpSum([prices[p] * x[p] for p in range(P)])
machine_costs_expr = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) for m in range(M)])
problem += profit - machine_costs_expr

#### Constraints
#### Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) <= availability[m], f'Machine_Availability_{m}'

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

