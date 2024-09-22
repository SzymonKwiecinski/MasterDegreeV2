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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Decision Variables}
Let \( b_p \) represent the number of batches of part \( p \) produced, where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
The objective is to maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \text{time}_{m,p} \cdot b_p)
\]
where \( \text{time}_{m,p} \) is the time required on machine \( m \) for part \( p \).

\subsection*{Constraints}

1. **Machine Availability Constraint**: 
   For each machine \( m \) (where \( m = 1, 2, \ldots, M \)):
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot b_p \leq available_m
   \]

2. **Minimum Batches Requirement**:
   For each part \( p \):
   \[
   b_p \geq min\_batches_p
   \]

3. **Labor Cost Constraints on Machine 1**:
   For machine 1, the labor cost structure applies:
   \[
   \text{time}_{1,p} \cdot b_p \leq \text{max\_hours}
   \]
   Where \(\text{max\_hours}\) is the number of hours available, which may include overtime hours.

4. **Additional Overtime Constraints**:
   If the total required hours on machine 1 exceed available hours, then:
   \[
   \text{time}_{1,p} \cdot b_p \leq available_1 + overtime\_hour \quad \text{(within standard cost)}
   \]
   and for hours exceeding this limit, the overtime cost applies.

\subsection*{Non-negativity Constraints}
\[
b_p \geq 0 \quad \text{for all } p
\]

\subsection*{Output}
The solution will yield:
\[
\text{Output: } \{ \text{batches} = [b_p \text{ for } p = 1, \ldots, P], \text{ total\_profit} = Z \} 
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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Decision Variables}
Let \( b_p \) represent the number of batches of part \( p \) produced, where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
The objective is to maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \text{time}_{m,p} \cdot b_p)
\]
where \( \text{time}_{m,p} \) is the time required on machine \( m \) for part \( p \).

\subsection*{Constraints}

1. **Machine Availability Constraint**: 
   For each machine \( m \) (where \( m = 1, 2, \ldots, M \)):
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot b_p \leq available_m
   \]

2. **Minimum Batches Requirement**:
   For each part \( p \):
   \[
   b_p \geq min\_batches_p
   \]

3. **Labor Cost Constraints on Machine 1**:
   For machine 1, the labor cost structure applies:
   \[
   \text{time}_{1,p} \cdot b_p \leq \text{max\_hours}
   \]
   Where \(\text{max\_hours}\) is the number of hours available, which may include overtime hours.

4. **Additional Overtime Constraints**:
   If the total required hours on machine 1 exceed available hours, then:
   \[
   \text{time}_{1,p} \cdot b_p \leq available_1 + overtime\_hour \quad \text{(within standard cost)}
   \]
   and for hours exceeding this limit, the overtime cost applies.

\subsection*{Non-negativity Constraints}
\[
b_p \geq 0 \quad \text{for all } p
\]

\subsection*{Output}
The solution will yield:
\[
\text{Output: } \{ \text{batches} = [b_p \text{ for } p = 1, \ldots, P], \text{ total\_profit} = Z \} 
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

#### Parameters
num_machines = data['NumMachines']
num_parts = data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("Batch", range(num_parts), lowBound=0, cat='Continuous')

#### Objective Function
profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) \
               - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) for m in range(num_machines))

problem += profit_expr, "Total_Profit"

#### Constraints
#### Machine Availability Constraints
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m], f"Machine_Availability_{m+1}"

#### Minimum Batches Requirement
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p+1}"

#### Labor Cost Constraints on Machine 1
for p in range(num_parts):
    problem += time_required[0][p] * batches[p] <= availability[0], f"Labor_Cost_Machine1_{p+1}"

#### Additional Overtime Constraints
for p in range(num_parts):
    problem += time_required[0][p] * batches[p] <= availability[0] + overtime_hour[0], f"Overtime_Cost_Machine1_{p+1}"

#### Solve the problem
problem.solve()

#### Output the results
batches_output = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

print(f'Batches: {batches_output}, Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

