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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Decision Variables}
Let \( x_p \) be the number of batches of part \( p \) produced per month, where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
The objective is to maximize the total profit, which is the difference between the revenue from selling the parts and the costs of using the machines. The objective function can be expressed as:

\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} (\text{price}_p \times x_p) - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) \times \text{cost}_m \right)
\]

\subsection*{Constraints}

1. \textbf{Machine Availability Constraint:}
   \[
   \sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) \leq \text{available}_m \quad \text{for } m = 1, 2, \ldots, M-2
   \]

2. \textbf{Combined Availability for Machines \( M \) and \( M-1 \):}
   \[
   \sum_{p=1}^{P} (\text{time}_{M,p} \times x_p) + \sum_{p=1}^{P} (\text{time}_{M-1,p} \times x_p) \leq \text{available}_M + \text{available}_{M-1}
   \]

3. \textbf{Contractual Obligations:}
   \[
   x_p \geq \text{min\_batches}_p \quad \text{for } p = 1, 2, \ldots, P
   \]

4. \textbf{Non-negativity:}
   \[
   x_p \geq 0 \quad \text{for } p = 1, 2, \ldots, P
   \]

\subsection*{Solution}
By solving the above linear programming model, you will obtain the number of batches of each part that should be produced in order to maximize the profit while satisfying all constraints.

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Decision Variables}
Let \( x_p \) be the number of batches of part \( p \) produced per month, where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
The objective is to maximize the total profit, which is the difference between the revenue from selling the parts and the costs of using the machines. The objective function can be expressed as:

\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} (\text{price}_p \times x_p) - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) \times \text{cost}_m \right)
\]

\subsection*{Constraints}

1. \textbf{Machine Availability Constraint:}
   \[
   \sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) \leq \text{available}_m \quad \text{for } m = 1, 2, \ldots, M-2
   \]

2. \textbf{Combined Availability for Machines \( M \) and \( M-1 \):}
   \[
   \sum_{p=1}^{P} (\text{time}_{M,p} \times x_p) + \sum_{p=1}^{P} (\text{time}_{M-1,p} \times x_p) \leq \text{available}_M + \text{available}_{M-1}
   \]

3. \textbf{Contractual Obligations:}
   \[
   x_p \geq \text{min\_batches}_p \quad \text{for } p = 1, 2, \ldots, P
   \]

4. \textbf{Non-negativity:}
   \[
   x_p \geq 0 \quad \text{for } p = 1, 2, \ldots, P
   \]

\subsection*{Solution}
By solving the above linear programming model, you will obtain the number of batches of each part that should be produced in order to maximize the profit while satisfying all constraints.

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Extracting values
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

#### Number of parts and machines
P = len(prices)
M = len(machine_costs)

#### Problem definition
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

#### Objective function
revenue = pulp.lpSum(prices[p] * x[p] for p in range(P))
machine_cost = pulp.lpSum(
    pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) * machine_costs[m] for m in range(M)
)
problem += revenue - machine_cost

#### Constraints
#### Machine availability constraint
for m in range(M-2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

#### Combined availability for machines M and M-1
problem += (pulp.lpSum(time_required[M-1][p] * x[p] for p in range(P)) +
            pulp.lpSum(time_required[M-2][p] * x[p] for p in range(P)) <= 
            availability[M-1] + availability[M-2])

#### Solving the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

