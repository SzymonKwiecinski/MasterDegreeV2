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
To solve this linear programming problem, we need to model it mathematically in terms of an objective function and constraints. We want to maximize profit, which is the revenue from selling the parts minus the costs associated with producing them, including machine costs and labor costs for machine 1.

Below is the mathematical model written in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Problem Formulation}

\subsection*{Indices}
\begin{itemize}
    \item $p$: Index for parts, $p = 1, \ldots, P$.
    \item $m$: Index for machines, $m = 1, \ldots, M$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $time_{m,p}$: Hours required on machine $m$ to produce 100 parts of type $p$.
    \item $cost_{m}$: Operational cost per hour for machine $m$.
    \item $available_{m}$: Availability of machine $m$ in hours per month.
    \item $price_{p}$: Selling price per batch of 100 parts of type $p$.
    \item $min\_batches_{p}$: Minimum batches of part $p$ required to be produced each month.
    \item $standard\_cost$: Labor cost per hour up to $overtime\_hour$ hours for machine 1.
    \item $overtime\_cost$: Overtime labor cost per hour for machine 1.
    \item $overtime\_hour$: Threshold for overtime hours for machine 1.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to produce.
    \item $x_{1}$: Standard labor hours used on machine 1.
    \item $y_{1}$: Overtime labor hours used on machine 1.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
    \text{Maximize} \quad & \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) \\
    & - \sum_{m=2}^{M} \left( cost_{m} \times \sum_{p=1}^{P} time_{m,p} \times batches_{p} \right) \\
    & - \left( standard\_cost \times x_{1} + overtime\_cost \times y_{1} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
    & \sum_{p=1}^{P} time_{m,p} \times batches_{p} \leq available_{m}, & \forall m = 2, \ldots, M \\
    & x_{1} + y_{1} \geq \sum_{p=1}^{P} time_{1,p} \times batches_{p} & \text{(labor hours for machine 1)} \\
    & x_{1} \leq overtime\_hour & \text{(standard hours constraint)} \\
    & y_{1} \geq 0, \quad x_{1} \geq 0 & \text{(non-negativity of hours)} \\
    & batches_{p} \geq min\_batches_{p}, & \forall p = 1, \ldots, P \\
    & batches_{p} \geq 0 & \text{(non-negativity of batches)}
\end{align*}

\end{document}
```

This model includes:
- The objective function reflecting revenue minus all costs.
- Constraints ensuring machine availabilities (except Machine 1), production requirements, and non-negativity.
- Labor allocation on Machine 1, considering standard and overtime costs.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Problem Formulation}

\subsection*{Indices}
\begin{itemize}
    \item $p$: Index for parts, $p = 1, \ldots, P$.
    \item $m$: Index for machines, $m = 1, \ldots, M$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $time_{m,p}$: Hours required on machine $m$ to produce 100 parts of type $p$.
    \item $cost_{m}$: Operational cost per hour for machine $m$.
    \item $available_{m}$: Availability of machine $m$ in hours per month.
    \item $price_{p}$: Selling price per batch of 100 parts of type $p$.
    \item $min\_batches_{p}$: Minimum batches of part $p$ required to be produced each month.
    \item $standard\_cost$: Labor cost per hour up to $overtime\_hour$ hours for machine 1.
    \item $overtime\_cost$: Overtime labor cost per hour for machine 1.
    \item $overtime\_hour$: Threshold for overtime hours for machine 1.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to produce.
    \item $x_{1}$: Standard labor hours used on machine 1.
    \item $y_{1}$: Overtime labor hours used on machine 1.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
    \text{Maximize} \quad & \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) \\
    & - \sum_{m=2}^{M} \left( cost_{m} \times \sum_{p=1}^{P} time_{m,p} \times batches_{p} \right) \\
    & - \left( standard\_cost \times x_{1} + overtime\_cost \times y_{1} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
    & \sum_{p=1}^{P} time_{m,p} \times batches_{p} \leq available_{m}, & \forall m = 2, \ldots, M \\
    & x_{1} + y_{1} \geq \sum_{p=1}^{P} time_{1,p} \times batches_{p} & \text{(labor hours for machine 1)} \\
    & x_{1} \leq overtime\_hour & \text{(standard hours constraint)} \\
    & y_{1} \geq 0, \quad x_{1} \geq 0 & \text{(non-negativity of hours)} \\
    & batches_{p} \geq min\_batches_{p}, & \forall p = 1, \ldots, P \\
    & batches_{p} \geq 0 & \text{(non-negativity of batches)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
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

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(data['NumParts']), lowBound=0, cat='Continuous')
x1 = pulp.LpVariable("x1", lowBound=0, cat='Continuous')  #### Standard labor hours for machine 1
y1 = pulp.LpVariable("y1", lowBound=0, cat='Continuous')  #### Overtime labor hours for machine 1

#### Objective Function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) \
        - pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(1, data['NumMachines'])) \
        - (data['StandardCost'] * x1 + data['OvertimeCost'] * y1)

problem += profit

#### Constraints
#### Machine availability constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]

#### Labor hours constraint for machine 1
problem += x1 + y1 >= pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(data['NumParts']))

#### Standard hours constraint for machine 1
problem += x1 <= data['OvertimeHour'][0]

#### Minimum batches constraints
for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

