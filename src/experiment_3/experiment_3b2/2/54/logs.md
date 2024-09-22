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
To create the mathematical model for this linear programming problem, we need to establish the decision variables, objective function, and constraints. The decision variables are the number of batches of each part produced. We will maximize the profit by deciding how many batches of each part to produce.

######### Decision Variables
- Let \( x_p \) be the number of batches of part \( p \) to produce, where \( p = 1, 2, \ldots, P \).

######### Objective Function
- The objective is to maximize the total profit, defined as the revenue from selling the parts minus the cost of machine time and labor.
- Revenue from part \( p \) is \( \text{price}_{p} \times x_p \).
- The cost of using machine \( m \) is \(\text{cost}_{m} \times \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \).
- For machine 1, we add labor costs, which include regular and overtime costs.
  
######### Constraints
1. Demand constraints: \( x_p \geq \text{min_batches}_{p} \) for each part \( p \).
2. Machine availability (excluding machine 1, which is outsourced):
   - \(\sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_{m} \) for each machine \( m = 2, 3, \ldots, M \).
3. The labor cost constraint for machine 1 (outsourced):
   - Initial standard and overtime cost modeling needs consideration of piecewise functions.

Here is the complete linear programming model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Production Planning}

\subsection*{Decision Variables}
Let:
\[
x_p \quad \text{be the number of batches of part } p \text{ produced, where } p = 1, 2, \ldots, P.
\]

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} \left( \text{price}_{p} \times x_p \right) - \sum_{m=2}^{M} \left( \text{cost}_{m} \times \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right) - C_1
\]

Where \( C_1 \) is the cost related to machine 1's labor:
\[
C_1 = \begin{cases}
\text{standard\_cost} \times \sum_{p=1}^{P} \text{time}_{1,p} \times x_p, & \text{if } \sum_{p=1}^{P} \text{time}_{1,p} \times x_p \leq \text{overtime\_hour} \\
\text{standard\_cost} \times \text{overtime\_hour} + \text{overtime\_cost} \times \left( \sum_{p=1}^{P} \text{time}_{1,p} \times x_p - \text{overtime\_hour} \right), & \text{otherwise}
\end{cases}
\]

\subsection*{Constraints}

1. Demand constraints:
\[
x_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P.
\]

2. Machine availability constraints for \( m = 2, 3, \ldots, M \):
\[
\sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_{m}, \quad \forall m = 2, 3, \ldots, M.
\]

3. Non-negativity constraints:
\[
x_p \geq 0, \quad \forall p = 1, 2, \ldots, P.
\]

\end{document}
```

This model will help in determining the optimal production plan to maximize profits while meeting all constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Production Planning}

\subsection*{Decision Variables}
Let:
\[
x_p \quad \text{be the number of batches of part } p \text{ produced, where } p = 1, 2, \ldots, P.
\]

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} \left( \text{price}_{p} \times x_p \right) - \sum_{m=2}^{M} \left( \text{cost}_{m} \times \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right) - C_1
\]

Where \( C_1 \) is the cost related to machine 1's labor:
\[
C_1 = \begin{cases}
\text{standard\_cost} \times \sum_{p=1}^{P} \text{time}_{1,p} \times x_p, & \text{if } \sum_{p=1}^{P} \text{time}_{1,p} \times x_p \leq \text{overtime\_hour} \\
\text{standard\_cost} \times \text{overtime\_hour} + \text{overtime\_cost} \times \left( \sum_{p=1}^{P} \text{time}_{1,p} \times x_p - \text{overtime\_hour} \right), & \text{otherwise}
\end{cases}
\]

\subsection*{Constraints}

1. Demand constraints:
\[
x_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P.
\]

2. Machine availability constraints for \( m = 2, 3, \ldots, M \):
\[
\sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_{m}, \quad \forall m = 2, 3, \ldots, M.
\]

3. Non-negativity constraints:
\[
x_p \geq 0, \quad \forall p = 1, 2, \ldots, P.
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

#### Parameters
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

#### Decision variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Problem definition
problem = pulp.LpProblem("Production_Planning", pulp.LpMaximize)

#### Objective Function
C1 = pulp.LpVariable("C1", lowBound=0)
overtime_hours = [pulp.lpSum(time_required[m-1][p] * x[p] for p in range(P)) - overtime_hour[m-2] for m in range(2, M+1)]
problem += pulp.lpSum(prices[p] * x[p] for p in range(P)) - pulp.lpSum(machine_costs[m-1] * pulp.lpSum(time_required[m-1][p] * x[p] for p in range(P)) for m in range(2, M+1)) - \
    (pulp.lpSum(standard_cost * pulp.lpSum(time_required[0][p] * x[p] for p in range(P)) if pulp.lpSum(time_required[0][p] * x[p] for p in range(P)) <= overtime_hour[0] else \
    (standard_cost * overtime_hour[0] + overtime_cost * overtime_hours[0]) for m in range(2, M+1)))

#### Constraints
for p in range(P):
    problem += x[p] >= min_batches[p], f"MinBatches_Constraint_{p+1}"
    
for m in range(2, M + 1):
    problem += pulp.lpSum(time_required[m-1][p] * x[p] for p in range(P)) <= availability[m-1], f"Machine_Availability_Constraint_{m-1}"

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

