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

\subsection*{Indices}
\begin{itemize}
    \item \( p \): index for parts, where \( p = 1, \ldots, P \)
    \item \( m \): index for machines, where \( m = 1, \ldots, M \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): time required (in hours) on machine \( m \) to produce a batch of part \( p \)
    \item \( \text{cost}_{m} \): cost (in dollars) per hour for using machine \( m \)
    \item \( \text{available}_{m} \): availability (in hours) of machine \( m \) per month
    \item \( \text{price}_{p} \): selling price (in dollars) per batch of part \( p \)
    \item \( \text{min\_batches}_{p} \): minimum number of batches of part \( p \) that must be produced
    \item \( \text{standard\_cost} \): standard labor cost (in dollars per hour) for machine 1
    \item \( \text{overtime\_cost} \): overtime labor cost (in dollars per hour) for machine 1
    \item \( \text{overtime\_hour} \): number of hours after which overtime cost applies
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{batches}_{p} \): number of batches of part \( p \) produced each month
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total\_Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \text{time}_{m,p} \cdot \text{batches}_{p} \right) - \text{Labor\_Costs}_{\text{machine\_1}}
\]

Where the labor costs for machine 1 are given by:
\[
\text{Labor\_Costs}_{\text{machine\_1}} = 
\begin{cases} 
\text{standard\_cost} \cdot \text{time}_{1,p} \cdot \text{batches}_{p} & \text{if } \text{time}_{1,p} \cdot \text{batches}_{p} \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left( \text{time}_{1,p} \cdot \text{batches}_{p} - \text{overtime\_hour} \right) & \text{if } \text{time}_{1,p} \cdot \text{batches}_{p} > \text{overtime\_hour}
\end{cases}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine availability constraints:
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
    \]

    \item Minimum production requirements:
    \[
    \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
    \]

    \item Non-negativity constraints:
    \[
    \text{batches}_{p} \geq 0, \quad \forall p = 1, \ldots, P
    \]
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

\subsection*{Indices}
\begin{itemize}
    \item \( p \): index for parts, where \( p = 1, \ldots, P \)
    \item \( m \): index for machines, where \( m = 1, \ldots, M \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): time required (in hours) on machine \( m \) to produce a batch of part \( p \)
    \item \( \text{cost}_{m} \): cost (in dollars) per hour for using machine \( m \)
    \item \( \text{available}_{m} \): availability (in hours) of machine \( m \) per month
    \item \( \text{price}_{p} \): selling price (in dollars) per batch of part \( p \)
    \item \( \text{min\_batches}_{p} \): minimum number of batches of part \( p \) that must be produced
    \item \( \text{standard\_cost} \): standard labor cost (in dollars per hour) for machine 1
    \item \( \text{overtime\_cost} \): overtime labor cost (in dollars per hour) for machine 1
    \item \( \text{overtime\_hour} \): number of hours after which overtime cost applies
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{batches}_{p} \): number of batches of part \( p \) produced each month
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total\_Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \text{time}_{m,p} \cdot \text{batches}_{p} \right) - \text{Labor\_Costs}_{\text{machine\_1}}
\]

Where the labor costs for machine 1 are given by:
\[
\text{Labor\_Costs}_{\text{machine\_1}} = 
\begin{cases} 
\text{standard\_cost} \cdot \text{time}_{1,p} \cdot \text{batches}_{p} & \text{if } \text{time}_{1,p} \cdot \text{batches}_{p} \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left( \text{time}_{1,p} \cdot \text{batches}_{p} - \text{overtime\_hour} \right) & \text{if } \text{time}_{1,p} \cdot \text{batches}_{p} > \text{overtime\_hour}
\end{cases}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine availability constraints:
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
    \]

    \item Minimum production requirements:
    \[
    \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
    \]

    \item Non-negativity constraints:
    \[
    \text{batches}_{p} \geq 0, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

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

#### Indices
P = data['NumParts']
M = data['NumMachines']

#### Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective Function
profit_terms = [data['Prices'][p] * batches[p] - 
                data['MachineCosts'][m] * data['TimeRequired'][m][p] * batches[p]
                for m in range(M) for p in range(P)]
labor_cost_machine_1_terms = [
    pulp.lpSum(
        data['StandardCost'] * data['TimeRequired'][0][p] * batches[p]
        if data['TimeRequired'][0][p] * batches[p] <= data['OvertimeHour'][0]
        else data['StandardCost'] * data['OvertimeHour'][0] + 
             data['OvertimeCost'] * (data['TimeRequired'][0][p] * batches[p] - data['OvertimeHour'][0])
    )
    for p in range(P)
]

problem += pulp.lpSum(profit_terms) - pulp.lpSum(labor_cost_machine_1_terms)

#### Constraints
#### Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(P)) <= data['Availability'][m]

#### Minimum Production Requirements
for p in range(P):
    problem += batches[p] >= data['MinBatches'][p]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

