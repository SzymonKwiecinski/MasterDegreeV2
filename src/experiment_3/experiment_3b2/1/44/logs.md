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
To solve this problem, we need to create a linear programming model to maximize the profit for the manufacturer. We'll define the decision variables, constraints, and objective function based on the given problem inputs. Let's express this in LaTeX using the provided information.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:} \\
Let \( x_p \) represent the number of batches produced for part \( p \), where \( p = 1, 2, \ldots, P \).

\textbf{Objective Function:} \\
Maximize the total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_p \times x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \left( \text{time}_{m,p} \times x_p \right) \right)
\]

\textbf{Constraints:} \\
1. Machine availability constraint for each machine \( m \):

\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \times x_p \right) \leq \text{available}_m, \quad \text{for } m = 1, 2, \ldots, M
\]

2. Minimum production constraint for each part \( p \):

\[
x_p \geq \text{min\_batches}_p, \quad \text{for } p = 1, 2, \ldots, P
\]

3. Non-negativity constraint:

\[
x_p \geq 0, \quad \text{for } p = 1, 2, \ldots, P
\]

\textbf{Given Parameters:} \\
- \(\text{time}_{m,p}\): The time required on machine \( m \) for part \( p \).
- \(\text{cost}_m\): The cost per hour for using machine \( m \).
- \(\text{available}_m\): The available hours per month for machine \( m \).
- \(\text{price}_p\): The selling price per batch of part \( p \).
- \(\text{min\_batches}_p\): The minimum number of batches needed for part \( p \).

\end{document}
```

This model will allow us to determine the optimal number of batches for each part to maximize profit, subject to machine availability and contractual obligations.

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

\textbf{Decision Variables:} \\
Let \( x_p \) represent the number of batches produced for part \( p \), where \( p = 1, 2, \ldots, P \).

\textbf{Objective Function:} \\
Maximize the total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_p \times x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \left( \text{time}_{m,p} \times x_p \right) \right)
\]

\textbf{Constraints:} \\
1. Machine availability constraint for each machine \( m \):

\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \times x_p \right) \leq \text{available}_m, \quad \text{for } m = 1, 2, \ldots, M
\]

2. Minimum production constraint for each part \( p \):

\[
x_p \geq \text{min\_batches}_p, \quad \text{for } p = 1, 2, \ldots, P
\]

3. Non-negativity constraint:

\[
x_p \geq 0, \quad \text{for } p = 1, 2, \ldots, P
\]

\textbf{Given Parameters:} \\
- \(\text{time}_{m,p}\): The time required on machine \( m \) for part \( p \).
- \(\text{cost}_m\): The cost per hour for using machine \( m \).
- \(\text{available}_m\): The available hours per month for machine \( m \).
- \(\text{price}_p\): The selling price per batch of part \( p \).
- \(\text{min\_batches}_p\): The minimum number of batches needed for part \( p \).

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

#### Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("batch", range(P), lowBound=0)

#### Objective Function
profit = pulp.lpSum([prices[p] * x[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) for m in range(M)])

problem += profit

#### Constraints
#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) <= availability[m]

#### Minimum production constraints
for p in range(P):
    problem += x[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

