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
- Machine \var{M} and Machine \var{M-1} can share availability.
- Individual availability conditions for Machine \var{M} and Machine \var{M-1} can be disregarded.
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
To create a linear programming model for the problem described, we will define the variables, objective function, and constraints needed to maximize the profit for the auto parts manufacturer. 

Let's denote:
- \( x_p \) as the number of batches of part \( p \) to be produced.
- \( t_{m,p} \) as the time required for machine \( m \) to produce a batch of part \( p \).
- \( c_m \) as the cost per hour for machine \( m \).
- \( a_m \) as the availability of machine \( m \).
- \( pr_p \) as the price per batch of part \( p \).
- \( \text{min\_batches}_p \) as the minimum number of batches required for part \( p \).

The linear programming model can be formulated as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the profit:

\[
\text{Profit} = \sum_{p=1}^{P} \left( pr_p \cdot x_p \right) - \sum_{m=1}^{M} \left( c_m \cdot \sum_{p=1}^{P} t_{m,p} \cdot x_p \right)
\]

\textbf{Subject to the constraints:}

1. Machine availability constraints for \( m = 1, \ldots, M-2 \):

\[
\sum_{p=1}^{P} t_{m,p} \cdot x_p \leq a_m \quad \text{for } m = 1, \ldots, M-2
\]

2. Combined availability constraint for Machine \( M \) and Machine \( M-1 \):

\[
\sum_{p=1}^{P} t_{M,p} \cdot x_p + \sum_{p=1}^{P} t_{M-1,p} \cdot x_p \leq a_M + a_{M-1}
\]

3. Minimum production requirements:

\[
x_p \geq \text{min\_batches}_p \quad \text{for } p = 1, \ldots, P
\]

4. Non-negativity constraints:

\[
x_p \geq 0 \quad \text{for } p = 1, \ldots, P
\]

\end{document}
```

This linear program will provide the optimal number of batches for each part such that the total profit is maximized, while satisfying machine usage and contract constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the profit:

\[
\text{Profit} = \sum_{p=1}^{P} \left( pr_p \cdot x_p \right) - \sum_{m=1}^{M} \left( c_m \cdot \sum_{p=1}^{P} t_{m,p} \cdot x_p \right)
\]

\textbf{Subject to the constraints:}

1. Machine availability constraints for \( m = 1, \ldots, M-2 \):

\[
\sum_{p=1}^{P} t_{m,p} \cdot x_p \leq a_m \quad \text{for } m = 1, \ldots, M-2
\]

2. Combined availability constraint for Machine \( M \) and Machine \( M-1 \):

\[
\sum_{p=1}^{P} t_{M,p} \cdot x_p + \sum_{p=1}^{P} t_{M-1,p} \cdot x_p \leq a_M + a_{M-1}
\]

3. Minimum production requirements:

\[
x_p \geq \text{min\_batches}_p \quad \text{for } p = 1, \ldots, P
\]

4. Non-negativity constraints:

\[
x_p \geq 0 \quad \text{for } p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data Parsing
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

#### Variables
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  #### Number of products
M = len(machine_costs)  #### Number of machines

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

#### Objective Function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M))
problem += profit

#### Constraints
#### Machine availability constraints for m = 1, ..., M-2
for m in range(M-2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

#### Combined availability constraint for Machine M and Machine M-1
problem += (pulp.lpSum(time_required[M-1][p] * x[p] for p in range(P)) + 
            pulp.lpSum(time_required[M-2][p] * x[p] for p in range(P))) <= (availability[M-1] + availability[M-2])

#### Minimum production requirements
for p in range(P):
    problem += x[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

