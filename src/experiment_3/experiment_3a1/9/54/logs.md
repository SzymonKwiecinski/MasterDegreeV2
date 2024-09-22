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

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \), where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot b_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left(\frac{\text{time}_{m,p}}{100}\right) b_p \right) - \text{LaborCosts}
\]

Where the labor costs are given by:
\[
\text{LaborCosts} = 
\begin{cases} 
\text{standard\_cost} \cdot (b_1 \cdot \frac{\text{time}_{1,1}}{100} \text{ if } (b_1 \cdot \frac{\text{time}_{1,1}}{100} \leq \text{overtime\_hour}) \\ 
\text{overtime\_cost} \cdot (b_1 \cdot \frac{\text{time}_{1,1}}{100} - \text{overtime\_hour}) + \text{standard\_cost} \cdot \text{overtime\_hour} \text{ otherwise}
\end{cases}
\]

\subsection*{Constraints}

1. **Production Requirement**:
   \[
   b_p \geq \text{min\_batches}_p \quad \forall p
   \]

2. **Machine Availability**:
   For \( m = 1, 2, \ldots, M \):
   \[
   \sum_{p=1}^{P} \left(\frac{\text{time}_{m,p}}{100} \cdot b_p\right) \leq \text{available}_m \quad \forall m
   \]

3. **Non-negativity**:
   \[
   b_p \geq 0 \quad \forall p
   \]

\subsection*{Output Format}
The solution provides the number of batches of each part produced:
\[
\text{Output: } \{ b_p \, \text{for } p = 1, \ldots, P, \, \text{total\_profit} = Z \}
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

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \), where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot b_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left(\frac{\text{time}_{m,p}}{100}\right) b_p \right) - \text{LaborCosts}
\]

Where the labor costs are given by:
\[
\text{LaborCosts} = 
\begin{cases} 
\text{standard\_cost} \cdot (b_1 \cdot \frac{\text{time}_{1,1}}{100} \text{ if } (b_1 \cdot \frac{\text{time}_{1,1}}{100} \leq \text{overtime\_hour}) \\ 
\text{overtime\_cost} \cdot (b_1 \cdot \frac{\text{time}_{1,1}}{100} - \text{overtime\_hour}) + \text{standard\_cost} \cdot \text{overtime\_hour} \text{ otherwise}
\end{cases}
\]

\subsection*{Constraints}

1. **Production Requirement**:
   \[
   b_p \geq \text{min\_batches}_p \quad \forall p
   \]

2. **Machine Availability**:
   For \( m = 1, 2, \ldots, M \):
   \[
   \sum_{p=1}^{P} \left(\frac{\text{time}_{m,p}}{100} \cdot b_p\right) \leq \text{available}_m \quad \forall m
   \]

3. **Non-negativity**:
   \[
   b_p \geq 0 \quad \forall p
   \]

\subsection*{Output Format}
The solution provides the number of batches of each part produced:
\[
\text{Output: } \{ b_p \, \text{for } p = 1, \ldots, P, \, \text{total\_profit} = Z \}
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

#### Define problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

#### Variables
b = pulp.LpVariable.dicts("b", range(data['NumParts']), lowBound=data['MinBatches'], cat='Continuous')

#### Objective function
profit = pulp.lpSum(data['Prices'][p] * b[p] for p in range(data['NumParts'])) - \
         pulp.lpSum(data['MachineCosts'][m] * (pulp.lpSum((data['TimeRequired'][m][p] / 100) * b[p] for p in range(data['NumParts']))) for m in range(data['NumMachines']))

labor_costs = []
for p in range(data['NumParts']):
    labor_expr = pulp.lpSum(b[p] * (data['TimeRequired'][0][p] / 100))
    labor_costs.append(pulp.lpSum((data['StandardCost'] * labor_expr, 
                                    data['OvertimeCost'] * (labor_expr - data['OvertimeHour'][0]) + data['StandardCost'] * data['OvertimeHour'][0])))

#### Add labor costs to the objective
problem += profit - pulp.lpSum(labor_costs)

#### Constraints
#### Machine Availability constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum((data['TimeRequired'][m][p] / 100) * b[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Machine_Availability_{m}"

#### Solve problem
problem.solve()

#### Output result
result = {f'b_{p}': b[p].varValue for p in range(data['NumParts'])}
result['total_profit'] = pulp.value(problem.objective)

#### Print the objective value
print(f' (Objective Value): <OBJ>{result["total_profit"]}</OBJ>')
```

