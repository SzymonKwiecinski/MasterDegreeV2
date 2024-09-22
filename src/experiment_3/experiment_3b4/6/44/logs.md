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
To formulate this problem as a linear programming model, we need to define the objective function, the decision variables, and the constraints.

######### Decision Variables
- Let \( x_p \) represent the number of batches of part \( p \) produced each month, where \( p = 1, 2, \ldots, P \).

######### Objective Function
The objective is to maximize the profit. The profit is calculated as the revenue from selling the parts minus the cost of using the machines. Thus, the objective function is:

\[
\text{Maximize} \quad \sum_{p=1}^{P} \left( \text{price}_p \times x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right)
\]

######### Constraints
1. **Minimum Production Constraints**: Ensure that production meets the contract requirements:
   \[
   x_p \geq \text{min_batches}_p, \quad \forall p \in \{1, 2, \ldots, P\}
   \]

2. **Machine Availability Constraints**: Ensure that the total production time on each machine does not exceed its available hours:
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_m, \quad \forall m \in \{1, 2, \ldots, M\}
   \]

3. **Non-negativity Constraints**: The number of batches produced cannot be negative:
   \[
   x_p \geq 0, \quad \forall p \in \{1, 2, \ldots, P\}
   \]

Below is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model}

\textbf{Decision Variables:}
\begin{align*}
x_p &: \text{Number of batches of part } p \text{ produced}, \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize} \quad Z = \sum_{p=1}^{P} \left( \text{price}_p \times x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right)
\end{align*}

\textbf{Subject to:}

\text{Minimum Production Constraints:}
\begin{align*}
x_p &\geq \text{min_batches}_p, \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\text{Machine Availability Constraints:}
\begin{align*}
\sum_{p=1}^{P} \text{time}_{m,p} \times x_p &\leq \text{available}_m, \quad \forall m \in \{1, 2, \ldots, M\}
\end{align*}

\text{Non-negativity Constraints:}
\begin{align*}
x_p &\geq 0, \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\end{document}
```

This model should be implemented in a linear programming solver to determine the optimal number of batches \( x_p \) for each part \( p \) to maximize the overall profit.

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
\begin{align*}
x_p &: \text{Number of batches of part } p \text{ produced}, \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize} \quad Z = \sum_{p=1}^{P} \left( \text{price}_p \times x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right)
\end{align*}

\textbf{Subject to:}

\text{Minimum Production Constraints:}
\begin{align*}
x_p &\geq \text{min_batches}_p, \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\text{Machine Availability Constraints:}
\begin{align*}
\sum_{p=1}^{P} \text{time}_{m,p} \times x_p &\leq \text{available}_m, \quad \forall m \in \{1, 2, \ldots, M\}
\end{align*}

\text{Non-negativity Constraints:}
\begin{align*}
x_p &\geq 0, \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

P = len(data['prices'])
M = len(data['machine_costs'])

#### Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function
revenue = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)])
costs = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) for m in range(M)])
problem += revenue - costs

#### Constraints

#### Minimum Production Constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

#### Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m]

#### Solve the problem
problem.solve()

#### Output The objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

