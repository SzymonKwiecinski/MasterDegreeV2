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

\textbf{Variables:}
\begin{itemize}
    \item Let \( b_p \) be the number of batches produced of part \( p \) for \( p = 1, 2, \ldots, P \).
    \end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize } Z & = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \frac{1}{100} \sum_{p=1}^{P} (time_{m,p} \cdot b_p)) \\
    & - \text{Labor Cost for Machine 1}
\end{align*}
Where the labor cost for Machine 1 is calculated based on standard and overtime costs.

\textbf{Labor Cost for Machine 1:}
\begin{align*}
    \text{Labor Cost} = 
    \begin{cases} 
    standard\_cost \cdot (time_{1,p} \cdot b_p) & \text{if } (time_{1,p} \cdot b_p) \leq overtime\_hour \\
    standard\_cost \cdot overtime\_hour + overtime\_cost \cdot ((time_{1,p} \cdot b_p) - overtime\_hour) & \text{if } (time_{1,p} \cdot b_p) > overtime\_hour 
    \end{cases}
\end{align*}

\textbf{Constraints:}
\begin{align*}
    \sum_{p=1}^{P} (time_{m,p} \cdot b_p) & \leq available_m \quad \forall m = 2, \ldots, M \\
    \sum_{p=1}^{P} (time_{1,p} \cdot b_p) & \leq \infty \\
    b_p & \geq min\_batches_p \quad \forall p = 1, 2, \ldots, P \\
    b_p & \geq 0 \quad \forall p = 1, 2, \ldots, P \\
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item The number of batches produced for each part: \( b_p \) for \( p = 1, \ldots, P \)
    \item Total profit: \( Z \)
\end{itemize}

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

\textbf{Variables:}
\begin{itemize}
    \item Let \( b_p \) be the number of batches produced of part \( p \) for \( p = 1, 2, \ldots, P \).
    \end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize } Z & = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \frac{1}{100} \sum_{p=1}^{P} (time_{m,p} \cdot b_p)) \\
    & - \text{Labor Cost for Machine 1}
\end{align*}
Where the labor cost for Machine 1 is calculated based on standard and overtime costs.

\textbf{Labor Cost for Machine 1:}
\begin{align*}
    \text{Labor Cost} = 
    \begin{cases} 
    standard\_cost \cdot (time_{1,p} \cdot b_p) & \text{if } (time_{1,p} \cdot b_p) \leq overtime\_hour \\
    standard\_cost \cdot overtime\_hour + overtime\_cost \cdot ((time_{1,p} \cdot b_p) - overtime\_hour) & \text{if } (time_{1,p} \cdot b_p) > overtime\_hour 
    \end{cases}
\end{align*}

\textbf{Constraints:}
\begin{align*}
    \sum_{p=1}^{P} (time_{m,p} \cdot b_p) & \leq available_m \quad \forall m = 2, \ldots, M \\
    \sum_{p=1}^{P} (time_{1,p} \cdot b_p) & \leq \infty \\
    b_p & \geq min\_batches_p \quad \forall p = 1, 2, \ldots, P \\
    b_p & \geq 0 \quad \forall p = 1, 2, \ldots, P \\
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item The number of batches produced for each part: \( b_p \) for \( p = 1, \ldots, P \)
    \item Total profit: \( Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
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

#### Problem Initialization
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

#### Variables
b = pulp.LpVariable.dicts("b", range(data['NumParts']), lowBound=0)

#### Objective Function
profit = pulp.lpSum(data['Prices'][p] * b[p] for p in range(data['NumParts']))
costs = pulp.lpSum(data['MachineCosts'][m] * (1/100) * pulp.lpSum(data['TimeRequired'][m][p] * b[p] for p in range(data['NumParts'])) for m in range(data['NumMachines']))
labor_cost_machine_1 = pulp.lpSum(pulp.lpSum(data['StandardCost'] * (data['TimeRequired'][0][p] * b[p]) if (data['TimeRequired'][0][p] * b[p]) <= data['OvertimeHour'][0] else 
                                                  (data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * ((data['TimeRequired'][0][p] * b[p]) - data['OvertimeHour'][0])) for p in range(data['NumParts']))

#### Combine objective components
problem += profit - costs - labor_cost_machine_1, "TotalProfit"

#### Constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * b[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Availability_Constraint_Machine_{m+1}"

for p in range(data['NumParts']):
    problem += b[p] >= data['MinBatches'][p], f"MinBatches_Constraint_Part_{p+1}"

#### Solve the problem
problem.solve()

#### Output
for p in range(data['NumParts']):
    print(f'Number of batches produced for part {p+1}: {b[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

