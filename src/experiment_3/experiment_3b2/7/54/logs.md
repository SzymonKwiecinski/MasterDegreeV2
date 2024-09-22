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
To formulate this linear programming problem, we need to set up the objective function and constraints based on the information provided.

**Objective Function:**
Maximize the total profit, which is calculated as the total revenue from selling the batches minus the total machine operation costs and labor costs for Machine 1. The revenue is the sum of the products of the number of batches produced and their respective prices. The machine operation costs are determined by the time each part requires on each machine and the respective hourly machine costs.

**Constraints:**
1. Each machine has a time capacity which should not be exceeded (except for machine 1, as it is outsourced, and costs are defined differently).
2. A minimum number of batches must be produced for each part to satisfy the contract.
3. Labor cost conditions for Machine 1.

Let's represent this in a mathematical form using LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $x_p$ be the number of batches of part $p$ produced.
    \item Let $h_1$ be the standard hours used on Machine 1.
    \item Let $h_1^{\text{overtime}}$ be the overtime hours used on Machine 1.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=2}^{M} \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_m - \text{standard_cost} \cdot h_1 - \text{overtime_cost} \cdot h_1^{\text{overtime}}
\]

\textbf{Subject to:}
\begin{align*}
    &\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_{m} \quad \text{for} \; m = 2, \ldots, M \quad &\text{(Machine availability)}\\
    &\sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p = h_1 + h_1^{\text{overtime}} \quad &\text{(Machine 1 time allocation)}\\
    &h_1 \leq \text{overtime_hour} \quad &\text{(Standard time limit for Machine 1)}\\
    &x_p \geq \text{min_batches}_{p} \quad \text{for} \; p = 1, \ldots, P \quad &\text{(Minimum batch requirement)}
\end{align*}

\textbf{Variables:}
\begin{align*}
    &x_p \geq 0 \quad &\text{(Non-negative batch production)}\\
    &h_1 \geq 0, \quad h_1^{\text{overtime}} \geq 0 \quad &\text{(Non-negative time usage for Machine 1)}
\end{align*}

\end{document}
```

This linear programming model captures the optimization problem of determining the number of batches of each part that should be produced to maximize profit, given machine availability, costs, and contractual obligations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $x_p$ be the number of batches of part $p$ produced.
    \item Let $h_1$ be the standard hours used on Machine 1.
    \item Let $h_1^{\text{overtime}}$ be the overtime hours used on Machine 1.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=2}^{M} \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_m - \text{standard_cost} \cdot h_1 - \text{overtime_cost} \cdot h_1^{\text{overtime}}
\]

\textbf{Subject to:}
\begin{align*}
    &\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_{m} \quad \text{for} \; m = 2, \ldots, M \quad &\text{(Machine availability)}\\
    &\sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p = h_1 + h_1^{\text{overtime}} \quad &\text{(Machine 1 time allocation)}\\
    &h_1 \leq \text{overtime_hour} \quad &\text{(Standard time limit for Machine 1)}\\
    &x_p \geq \text{min_batches}_{p} \quad \text{for} \; p = 1, \ldots, P \quad &\text{(Minimum batch requirement)}
\end{align*}

\textbf{Variables:}
\begin{align*}
    &x_p \geq 0 \quad &\text{(Non-negative batch production)}\\
    &h_1 \geq 0, \quad h_1^{\text{overtime}} \geq 0 \quad &\text{(Non-negative time usage for Machine 1)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

#### Problem setup
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['NumParts']), lowBound=0, cat='Continuous')
h1 = pulp.LpVariable("h1", lowBound=0)
h1_overtime = pulp.LpVariable("h1_overtime", lowBound=0)

#### Objective Function
profit = pulp.lpSum([data['Prices'][p] * x[p] for p in range(data['NumParts'])])
cost = pulp.lpSum([data['MachineCosts'][m] * pulp.lpSum([data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])]) for m in range(1, data['NumMachines'])])
standard_cost = data['StandardCost'] * h1
overtime_cost = data['OvertimeCost'] * h1_overtime
problem += profit - cost - standard_cost - overtime_cost

#### Constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum([data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])]) <= data['Availability'][m], f"Machine_{m}_availability"

problem += pulp.lpSum([data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])]) == h1 + h1_overtime, "Machine_1_time_allocation"
problem += h1 <= data['OvertimeHour'][0], "Standard_time_limit_Machine_1"

for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p], f"Min_batches_part_{p}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

