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
To model this problem using linear programming, we'll define decision variables, the objective function, and the necessary constraints. Let's denote the decision variables as \( x_p \), which represents the number of batches of part \( p \) produced in a month.

######### Decision Variables
- \( x_p \): Number of batches of part \( p \) produced, for \( p = 1, 2, \ldots, P \).

######### Parameters
- \( \text{time\_required}_{m,p} \): Time required for machine \( m \) to produce a batch of part \( p \).
- \( \text{cost}_{m} \): Cost per hour for using machine \( m \).
- \( \text{available}_{m} \): Available hours for machine \( m \) per month.
- \( \text{price}_{p} \): Selling price per batch of part \( p \).
- \( \text{min\_batches}_{p} \): Minimum batches of part \( p \) required each month.

######### Objective Function
To maximize profit, the objective function is formulated as:
\[
\text{Maximize} \quad \sum_{p=1}^{P} ( \text{price}_{p} \cdot x_p ) - \sum_{m=1}^{M} \sum_{p=1}^{P} ( \text{cost}_{m} \cdot \text{time\_required}_{m,p} \cdot x_p )
\]

######### Constraints
1. Machine availability constraints:
   \[
   \sum_{p=1}^{P} ( \text{time\_required}_{m,p} \cdot x_p ) \leq \text{available}_{m}, \quad \forall m = 1, 2, \ldots, M
   \]
2. Minimum batch production requirement:
   \[
   x_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P
   \]
3. Non-negativity constraints:
   \[
   x_p \geq 0, \quad \forall p = 1, 2, \ldots, P
   \]

Here's the complete mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_p & : \text{Number of batches of part } p \text{ produced per month.} \\
\end{align*}

\subsection*{Objective Function}
\[
\text{Maximize} \quad \sum_{p=1}^{P} (\text{price}_{p} \cdot x_p) - \sum_{m=1}^{M} \sum_{p=1}^{P} (\text{cost}_{m} \cdot \text{time\_required}_{m,p} \cdot x_p)
\]

\subsection*{Constraints}
\begin{align*}
\text{Machine Availability:} \quad & \sum_{p=1}^{P} (\text{time\_required}_{m,p} \cdot x_p) \leq \text{available}_{m}, & \forall m = 1, 2, \ldots, M \\
\text{Minimum Batch Requirement:} \quad & x_p \geq \text{min\_batches}_{p}, & \forall p = 1, 2, \ldots, P \\
\text{Non-negativity:} \quad & x_p \geq 0, & \forall p = 1, 2, \ldots, P
\end{align*}

\end{document}
```

This model provides a framework to solve the problem using a linear programming solver by defining the objective and constraints appropriately based on the given input data.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_p & : \text{Number of batches of part } p \text{ produced per month.} \\
\end{align*}

\subsection*{Objective Function}
\[
\text{Maximize} \quad \sum_{p=1}^{P} (\text{price}_{p} \cdot x_p) - \sum_{m=1}^{M} \sum_{p=1}^{P} (\text{cost}_{m} \cdot \text{time\_required}_{m,p} \cdot x_p)
\]

\subsection*{Constraints}
\begin{align*}
\text{Machine Availability:} \quad & \sum_{p=1}^{P} (\text{time\_required}_{m,p} \cdot x_p) \leq \text{available}_{m}, & \forall m = 1, 2, \ldots, M \\
\text{Minimum Batch Requirement:} \quad & x_p \geq \text{min\_batches}_{p}, & \forall p = 1, 2, \ldots, P \\
\text{Non-negativity:} \quad & x_p \geq 0, & \forall p = 1, 2, \ldots, P
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
num_parts = len(data['prices'])
x = pulp.LpVariable.dicts('Batch', range(num_parts), lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(num_parts))
costs = pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * x[p]
                   for m in range(len(data['machine_costs'])) for p in range(num_parts))
problem += profit - costs

#### Constraints
#### Machine Availability Constraints
for m in range(len(data['availability'])):
    problem += (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(num_parts)) <= data['availability'][m])

#### Minimum Batch Requirement Constraints
for p in range(num_parts):
    problem += (x[p] >= data['min_batches'][p])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

