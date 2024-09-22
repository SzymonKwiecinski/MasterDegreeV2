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
- Extra available time for machine \var{m} can be acquired at $\var{extra_costs_{m}}/hour. 
- Up to \var{max_extra_{m}} hours can be purchased for each machine \var{m}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "extra_costs": [extra_cost_{m} for m in 1, ..., M],
    "max_extra": [max_extra_{m} for m in 1, ..., M]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{extra_time} denotes the additional hours purchased for each machine \var{m}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "extra_time": [extra_time_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem, we need to formulate a linear programming (LP) model. The objective is to maximize the total profit, which is calculated as the revenue from selling parts minus the costs of machining and any additional machine hours purchased.

Let's define the LP model with the following components:

1. **Decision Variables**:
   - \( x_p \): Number of batches of part \( p \) produced.
   - \( e_m \): Extra hours purchased for machine \( m \).

2. **Objective Function**:
   - Maximize the profit, which is the revenue from selling parts minus the machining costs and the costs for any extra hours.

3. **Constraints**:
   - Ensure that the production meets the minimum batch requirements for each part.
   - Ensure that the hours used on each machine do not exceed its available hours plus any extra hours purchased.
   - Limit the extra hours purchased for each machine to the maximum allowed.

Here's the LaTeX representation of this LP model:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Mathematical Formulation}

\textbf{Indices:}
\begin{itemize}
    \item \( p = 1, 2, \ldots, P \) : Parts
    \item \( m = 1, 2, \ldots, M \) : Machines
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{time\_required}_{m,p} \): Time required by machine \( m \) to produce 100 units of part \( p \) (in hours)
    \item \( \text{cost}_{m} \): Cost per hour for using machine \( m \)
    \item \( \text{available}_{m} \): Available hours for machine \( m \) per month
    \item \( \text{price}_{p} \): Selling price per batch (100 units) of part \( p \)
    \item \( \text{min\_batches}_{p} \): Minimum batches of part \( p \) required per month
    \item \( \text{extra\_cost}_{m} \): Extra cost for purchasing additional hours for machine \( m \)
    \item \( \text{max\_extra}_{m} \): Maximum extra hours that can be purchased for machine \( m \)
\end{itemize}

\textbf{Decision Variables:}
\begin{align*}
    x_p & : \text{Number of batches of part } p \text{ produced (integer)} \\
    e_m & : \text{Extra hours purchased for machine } m \text{ (continuous)}
\end{align*}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} \text{time\_required}_{m,p} \cdot x_p \cdot \text{cost}_{m} + e_m \cdot \text{extra\_cost}_{m} \right)
\]

\textbf{Constraints:}
\begin{align*}
    & x_p \geq \text{min\_batches}_{p}, && \forall p = 1, 2, \ldots, P \\
    & \sum_{p=1}^{P} \text{time\_required}_{m,p} \cdot x_p \leq \text{available}_{m} + e_m, && \forall m = 1, 2, \ldots, M \\
    & 0 \leq e_m \leq \text{max\_extra}_{m}, && \forall m = 1, 2, \ldots, M \\
    & x_p \geq 0 \text{ and integer}, && \forall p = 1, 2, \ldots, P \\
    & e_m \geq 0, && \forall m = 1, 2, \ldots, M
\end{align*}

\end{document}
```

This LaTeX document provides a complete mathematical formulation of the LP problem, including the objective function and constraints necessary to solve the problem of maximizing the profit for the auto parts division.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Mathematical Formulation}

\textbf{Indices:}
\begin{itemize}
    \item \( p = 1, 2, \ldots, P \) : Parts
    \item \( m = 1, 2, \ldots, M \) : Machines
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{time\_required}_{m,p} \): Time required by machine \( m \) to produce 100 units of part \( p \) (in hours)
    \item \( \text{cost}_{m} \): Cost per hour for using machine \( m \)
    \item \( \text{available}_{m} \): Available hours for machine \( m \) per month
    \item \( \text{price}_{p} \): Selling price per batch (100 units) of part \( p \)
    \item \( \text{min\_batches}_{p} \): Minimum batches of part \( p \) required per month
    \item \( \text{extra\_cost}_{m} \): Extra cost for purchasing additional hours for machine \( m \)
    \item \( \text{max\_extra}_{m} \): Maximum extra hours that can be purchased for machine \( m \)
\end{itemize}

\textbf{Decision Variables:}
\begin{align*}
    x_p & : \text{Number of batches of part } p \text{ produced (integer)} \\
    e_m & : \text{Extra hours purchased for machine } m \text{ (continuous)}
\end{align*}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} \text{time\_required}_{m,p} \cdot x_p \cdot \text{cost}_{m} + e_m \cdot \text{extra\_cost}_{m} \right)
\]

\textbf{Constraints:}
\begin{align*}
    & x_p \geq \text{min\_batches}_{p}, && \forall p = 1, 2, \ldots, P \\
    & \sum_{p=1}^{P} \text{time\_required}_{m,p} \cdot x_p \leq \text{available}_{m} + e_m, && \forall m = 1, 2, \ldots, M \\
    & 0 \leq e_m \leq \text{max\_extra}_{m}, && \forall m = 1, 2, \ldots, M \\
    & x_p \geq 0 \text{ and integer}, && \forall p = 1, 2, \ldots, P \\
    & e_m \geq 0, && \forall m = 1, 2, \ldots, M
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

#### Indices
P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
e = pulp.LpVariable.dicts("extra_hours", range(M), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
           pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + e[m] * data['extra_costs'][m] for m in range(M))

#### Constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"MinBatches_{p}"

for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m], f"AvailableTime_{m}"
    problem += e[m] <= data['max_extra'][m], f"MaxExtra_{m}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

