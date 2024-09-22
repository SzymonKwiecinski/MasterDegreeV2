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

\subsection*{Parameters}
\begin{align*}
& P \quad \text{(Number of different parts)} \\
& M \quad \text{(Number of different machines)} \\
& \text{time}_{m,p} \quad \text{(Time required in hours on machine } m \text{ for part } p) \\
& \text{cost}_{m} \quad \text{(Cost per hour for using machine } m) \\
& \text{available}_{m} \quad \text{(Availability of machine } m \text{ in hours per month)} \\
& \text{price}_{p} \quad \text{(Selling price per batch of part } p) \\
& \text{min\_batches}_{p} \quad \text{(Minimum batches of part } p \text{ to be produced)} \\
& \text{standard\_cost} \quad \text{(Standard labor cost per hour)} \\
& \text{overtime\_cost} \quad \text{(Overtime labor cost per hour)} \\
& \text{overtime\_hour} \quad \text{(Hours up to which standard cost is charged)}
\end{align*}

\subsection*{Decision Variables}
Let \( \text{batches}_{p} \) be the number of batches produced for part \( p \), where \( p = 1, \ldots, P \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{total\_profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \frac{\text{time}_{m,p}}{100} \cdot \text{batches}_{p} \right) \right) \right)
\]

\subsection*{Constraints}
1. Time availability for each machine:
\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot \text{batches}_{p} \right) \leq \text{available}_{m} \quad \forall m = 1, \ldots, M
\]
2. Minimum production requirement for each part:
\[
\text{batches}_{p} \geq \text{min\_batches}_{p} \quad \forall p = 1, \ldots, P
\]
3. Labor cost constraints for machine 1:
\begin{align*}
& \text{labor\_hours} = \sum_{p=1}^{P} \left( \frac{\text{time}_{1,p}}{100} \cdot \text{batches}_{p} \right) \\
& \text{if } \text{labor\_hours} \leq \text{overtime\_hour}: \quad \text{cost}_{labor} = \text{labor\_hours} \cdot \text{standard\_cost} \\
& \text{if } \text{labor\_hours} > \text{overtime\_hour}: \quad \text{cost}_{labor} = \text{overtime\_hour} \cdot \text{standard\_cost} + (\text{labor\_hours} - \text{overtime\_hour}) \cdot \text{overtime\_cost}
\end{align*}

\subsection*{Non-negativity Constraints}
\[
\text{batches}_{p} \geq 0 \quad \forall p = 1, \ldots, P
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

\subsection*{Parameters}
\begin{align*}
& P \quad \text{(Number of different parts)} \\
& M \quad \text{(Number of different machines)} \\
& \text{time}_{m,p} \quad \text{(Time required in hours on machine } m \text{ for part } p) \\
& \text{cost}_{m} \quad \text{(Cost per hour for using machine } m) \\
& \text{available}_{m} \quad \text{(Availability of machine } m \text{ in hours per month)} \\
& \text{price}_{p} \quad \text{(Selling price per batch of part } p) \\
& \text{min\_batches}_{p} \quad \text{(Minimum batches of part } p \text{ to be produced)} \\
& \text{standard\_cost} \quad \text{(Standard labor cost per hour)} \\
& \text{overtime\_cost} \quad \text{(Overtime labor cost per hour)} \\
& \text{overtime\_hour} \quad \text{(Hours up to which standard cost is charged)}
\end{align*}

\subsection*{Decision Variables}
Let \( \text{batches}_{p} \) be the number of batches produced for part \( p \), where \( p = 1, \ldots, P \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{total\_profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \frac{\text{time}_{m,p}}{100} \cdot \text{batches}_{p} \right) \right) \right)
\]

\subsection*{Constraints}
1. Time availability for each machine:
\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot \text{batches}_{p} \right) \leq \text{available}_{m} \quad \forall m = 1, \ldots, M
\]
2. Minimum production requirement for each part:
\[
\text{batches}_{p} \geq \text{min\_batches}_{p} \quad \forall p = 1, \ldots, P
\]
3. Labor cost constraints for machine 1:
\begin{align*}
& \text{labor\_hours} = \sum_{p=1}^{P} \left( \frac{\text{time}_{1,p}}{100} \cdot \text{batches}_{p} \right) \\
& \text{if } \text{labor\_hours} \leq \text{overtime\_hour}: \quad \text{cost}_{labor} = \text{labor\_hours} \cdot \text{standard\_cost} \\
& \text{if } \text{labor\_hours} > \text{overtime\_hour}: \quad \text{cost}_{labor} = \text{overtime\_hour} \cdot \text{standard\_cost} + (\text{labor\_hours} - \text{overtime\_hour}) \cdot \text{overtime\_cost}
\end{align*}

\subsection*{Non-negativity Constraints}
\[
\text{batches}_{p} \geq 0 \quad \forall p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
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
time = data['TimeRequired']
costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

#### Objective Function
profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(P))  #### Total revenue
cost_expr = pulp.lpSum(
    costs[m] * (pulp.lpSum(time[m][p] * batches[p] for p in range(P)) / 100) 
    for m in range(M))  #### Total cost
problem += profit_expr - cost_expr, "Total_Profit"

#### Constraints
#### Time availability for each machine
for m in range(M):
    problem += pulp.lpSum(time[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m}"

#### Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

#### Labor cost constraints for machine 1
labor_hours = pulp.lpSum((time[0][p] / 100) * batches[p] for p in range(P))
cost_labor = pulp.lpSum(
    (standard_cost * labor_hours if labor_hours <= overtime_hour[0] else 
     (standard_cost * overtime_hour[0]) + 
     ((labor_hours - overtime_hour[0]) * overtime_cost))
)

problem += cost_labor <= (labor_hours / 100) * (standard_cost + overtime_cost), "Labor_Cost_Constraint"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

