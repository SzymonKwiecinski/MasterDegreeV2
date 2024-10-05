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
- Machine \var{1} is being outsourced so that the manufacturer must pay for the labor.
- The labor costs $\var{standard_cost}/h up to \var{overtime_hour} hours, after which it costs $\var{overtime_cost}/h due to overtime.
- Individual availability conditions for Machine \var{1} can be disregarded.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour
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

\section*{Linear Programming Model}

\textbf{Indices:}
\begin{itemize}
    \item \( p \): Index for parts, where \( p = 1, 2, \ldots, P \)
    \item \( m \): Index for machines, where \( m = 1, 2, \ldots, M \)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{time}_{m,p} \): Time required (in hours) on machine \( m \) to produce one batch of part \( p \)
    \item \( \text{cost}_{m} \): Cost per hour for using machine \( m \)
    \item \( \text{available}_{m} \): Available hours per month for machine \( m \)
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \)
    \item \( \text{min\_batches}_{p} \): Minimum number of batches of part \( p \) that must be produced
    \item \( \text{standard\_cost} \): Standard labor cost per hour for machine 1
    \item \( \text{overtime\_cost} \): Overtime labor cost per hour for machine 1
    \item \( \text{overtime\_hour} \): Number of hours after which overtime cost applies
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item \( \text{batches}_{p} \): Number of batches of part \( p \) produced
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \right) \right) - \text{Labor Cost}
\]

\textbf{Subject to:}

1. Machine time constraints:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, 2, \ldots, M
\]

2. Minimum batches requirement:
\[
\text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P
\]

3. Labor cost calculation for Machine 1:
Let \( T_1 = \sum_{p=1}^{P} \text{time}_{1,p} \cdot \text{batches}_{p} \) be the total hours used on Machine 1.

\[
\text{Labor Cost} =
\begin{cases}
\text{standard\_cost} \cdot T_1 & \text{if } T_1 \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (T_1 - \text{overtime\_hour}) & \text{if } T_1 > \text{overtime\_hour}
\end{cases}
\]

4. Non-negativity constraints:
\[
\text{batches}_{p} \geq 0, \quad \forall p = 1, 2, \ldots, P
\]

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

\section*{Linear Programming Model}

\textbf{Indices:}
\begin{itemize}
    \item \( p \): Index for parts, where \( p = 1, 2, \ldots, P \)
    \item \( m \): Index for machines, where \( m = 1, 2, \ldots, M \)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{time}_{m,p} \): Time required (in hours) on machine \( m \) to produce one batch of part \( p \)
    \item \( \text{cost}_{m} \): Cost per hour for using machine \( m \)
    \item \( \text{available}_{m} \): Available hours per month for machine \( m \)
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \)
    \item \( \text{min\_batches}_{p} \): Minimum number of batches of part \( p \) that must be produced
    \item \( \text{standard\_cost} \): Standard labor cost per hour for machine 1
    \item \( \text{overtime\_cost} \): Overtime labor cost per hour for machine 1
    \item \( \text{overtime\_hour} \): Number of hours after which overtime cost applies
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item \( \text{batches}_{p} \): Number of batches of part \( p \) produced
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \right) \right) - \text{Labor Cost}
\]

\textbf{Subject to:}

1. Machine time constraints:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, 2, \ldots, M
\]

2. Minimum batches requirement:
\[
\text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P
\]

3. Labor cost calculation for Machine 1:
Let \( T_1 = \sum_{p=1}^{P} \text{time}_{1,p} \cdot \text{batches}_{p} \) be the total hours used on Machine 1.

\[
\text{Labor Cost} =
\begin{cases}
\text{standard\_cost} \cdot T_1 & \text{if } T_1 \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (T_1 - \text{overtime\_hour}) & \text{if } T_1 > \text{overtime\_hour}
\end{cases}
\]

4. Non-negativity constraints:
\[
\text{batches}_{p} \geq 0, \quad \forall p = 1, 2, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data
data = {
    'NumMachines': 3,
    'NumParts': 4,
    'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'MachineCosts': [160, 10, 15],
    'Availability': [200, 300, 500],
    'Prices': [570, 250, 585, 430],
    'MinBatches': [10, 10, 10, 10],
    'StandardCost': 20,
    'OvertimeCost': 30,
    'OvertimeHour': [400, 400, 300]
}

#### Parameters
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

#### Define the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision variables: batches of each part
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

#### Objective function components
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
production_cost = pulp.lpSum(costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

#### Labor cost calculation for machine 1
T1 = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
labor_cost = pulp.LpVariable("LaborCost", lowBound=0, cat='Continuous')

#### Labor cost constraints for machine 1
problem += labor_cost >= standard_cost * T1
problem += labor_cost >= standard_cost * overtime_hour[0] + overtime_cost * (T1 - overtime_hour[0])

#### Objective function
problem += revenue - production_cost - labor_cost

#### Constraints
#### 1. Machine time constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

#### 2. Minimum batches requirement
for p in range(P):
    problem += batches[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

