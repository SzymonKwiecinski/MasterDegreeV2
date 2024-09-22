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

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \), where \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): time required on machine \( m \) for part \( p \) (in hours).
    \item \( cost_{m} \): cost per hour for using machine \( m \).
    \item \( available_{m} \): available hours of machine \( m \) per month.
    \item \( price_{p} \): selling price per batch of part \( p \).
    \item \( min\_batches_{p} \): minimum batches required for part \( p \) to fulfill a contract.
    \item \( standard\_cost \): standard cost of labor per hour for machine 1.
    \item \( overtime\_cost \): overtime cost of labor per hour for machine 1.
    \item \( overtime\_hour \): number of hours after which overtime cost applies.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{p=1}^{P} (price_{p} \cdot b_p) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p))
\]

\subsection*{Constraints}
\begin{align*}
\sum_{p=1}^{P} (time_{m,p} \cdot b_p) & \leq available_{m} \quad \text{for } m = 2, \ldots, M \\
\sum_{p=1}^{P} (time_{1,p} \cdot b_p) & \leq O \quad \text{where } O = overtime\_hour \\
\sum_{p=1}^{P} (time_{1,p} \cdot b_p) & > O \Rightarrow \text{Cost for machine 1} = (standard\_cost \cdot O) + (overtime\_cost \cdot (\sum_{p=1}^{P} (time_{1,p} \cdot b_p) - O)) \\
b_p & \geq min\_batches_{p} \quad \text{for } p = 1, \ldots, P \\
b_p & \geq 0 \quad \text{for } p = 1, \ldots, P \\
\end{align*}

\subsection*{Output}
The output will signify:
\begin{itemize}
    \item \( batches = [b_1, b_2, \ldots, b_P] \)
    \item \( total\_profit = Z \)
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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \), where \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): time required on machine \( m \) for part \( p \) (in hours).
    \item \( cost_{m} \): cost per hour for using machine \( m \).
    \item \( available_{m} \): available hours of machine \( m \) per month.
    \item \( price_{p} \): selling price per batch of part \( p \).
    \item \( min\_batches_{p} \): minimum batches required for part \( p \) to fulfill a contract.
    \item \( standard\_cost \): standard cost of labor per hour for machine 1.
    \item \( overtime\_cost \): overtime cost of labor per hour for machine 1.
    \item \( overtime\_hour \): number of hours after which overtime cost applies.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{p=1}^{P} (price_{p} \cdot b_p) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p))
\]

\subsection*{Constraints}
\begin{align*}
\sum_{p=1}^{P} (time_{m,p} \cdot b_p) & \leq available_{m} \quad \text{for } m = 2, \ldots, M \\
\sum_{p=1}^{P} (time_{1,p} \cdot b_p) & \leq O \quad \text{where } O = overtime\_hour \\
\sum_{p=1}^{P} (time_{1,p} \cdot b_p) & > O \Rightarrow \text{Cost for machine 1} = (standard\_cost \cdot O) + (overtime\_cost \cdot (\sum_{p=1}^{P} (time_{1,p} \cdot b_p) - O)) \\
b_p & \geq min\_batches_{p} \quad \text{for } p = 1, \ldots, P \\
b_p & \geq 0 \quad \text{for } p = 1, \ldots, P \\
\end{align*}

\subsection*{Output}
The output will signify:
\begin{itemize}
    \item \( batches = [b_1, b_2, \ldots, b_P] \)
    \item \( total\_profit = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load the data
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

#### Extract data from the loaded json
NumMachines = data['NumMachines']
NumParts = data['NumParts']
TimeRequired = data['TimeRequired']
MachineCosts = data['MachineCosts']
Availability = data['Availability']
Prices = data['Prices']
MinBatches = data['MinBatches']
StandardCost = data['StandardCost']
OvertimeCost = data['OvertimeCost']
OvertimeHour = data['OvertimeHour']

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=0) for p in range(NumParts)]

#### Define the objective function
profit_expr = pulp.lpSum([Prices[p] * batches[p] for p in range(NumParts)]) \
               - pulp.lpSum([MachineCosts[m] * (pulp.lpSum([TimeRequired[m][p] * batches[p] for p in range(NumParts)])) for m in range(NumMachines)])

problem += profit_expr, "Total_Profit"

#### Constraints for each machine
for m in range(1, NumMachines):
    problem += (pulp.lpSum([TimeRequired[m][p] * batches[p] for p in range(NumParts)]) <= Availability[m]), f"Machine_{m}_Availability"

#### Constraint for machine 1
problem += (pulp.lpSum([TimeRequired[0][p] * batches[p] for p in range(NumParts)]) <= OvertimeHour[0]), "Machine_1_Overtime"

#### Handle overtime cost for machine 1
overtime_expr = pulp.lpSum([TimeRequired[0][p] * batches[p] for p in range(NumParts)]) - OvertimeHour[0]
problem += (overtime_expr >= 0), "Overtime_Condition"

#### Minimum batches constraints
for p in range(NumParts):
    problem += (batches[p] >= MinBatches[p]), f"Min_Batches_{p}"

#### Solve the problem
problem.solve()

#### Extract results
batches_result = [pulp.value(batch) for batch in batches]
total_profit = pulp.value(problem.objective)

#### Output results
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

