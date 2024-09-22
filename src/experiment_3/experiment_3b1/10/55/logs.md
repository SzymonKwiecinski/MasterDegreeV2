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
- The desired profit should surpass \var{min_profit}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour,
    "min_profit": min_profit
}

OBJECTIVE: Determine the quantity of batches for each part the manufacturer should produce every month, ensuring all constraints are met.

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
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the hours required on machine \( m \) to produce a batch of 100 parts \( p \).
    \item Let \( \text{cost}_{m} \) be the charge per hour for using machine \( m \).
    \item Let \( \text{available}_{m} \) be the availability of machine \( m \) in hours per month.
    \item Let \( \text{price}_{p} \) be the selling price per batch of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) to be produced to fulfill a contract.
    \item Let \( \text{standard\_cost} \) be the labor cost per hour up to a limit.
    \item Let \( \text{overtime\_cost} \) be the labor cost per hour after the limit.
    \item Let \( \text{overtime\_hour} \) be the maximum hours before overtime charges apply.
    \item Let \( \text{min\_profit} \) be the minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
Let \( x_{p} \) be the number of batches of part \( p \) produced.

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot x_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_{p} \right) \right) - \text{Labor Costs}
\]

\subsection*{Labor Costs}
\[
\text{Labor Costs} = 
\begin{cases} 
\text{standard\_cost} \cdot \text{overtime\_hour} & \text{if } \sum_{p=1}^{P} \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_{p} \leq \text{overtime\_hour} \\ 
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left( \sum_{p=1}^{P} \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_{p} - \text{overtime\_hour} \right) & \text{if } \sum_{p=1}^{P} \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_{p} > \text{overtime\_hour}
\end{cases}
\]

\subsection*{Constraints}
1. Machine Availability Constraints:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_{p} \leq \text{available}_{m} \quad \text{for all } m = 1, \ldots, M
\]

2. Minimum Batches Requirement:
\[
x_{p} \geq \text{min\_batches}_{p} \quad \text{for all } p = 1, \ldots, P
\]

3. Minimum Profit Requirement:
\[
\text{Total Profit} \geq \text{min\_profit}
\]

4. Non-negativity Constraints:
\[
x_{p} \geq 0 \quad \text{for all } p = 1, \ldots, P
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
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the hours required on machine \( m \) to produce a batch of 100 parts \( p \).
    \item Let \( \text{cost}_{m} \) be the charge per hour for using machine \( m \).
    \item Let \( \text{available}_{m} \) be the availability of machine \( m \) in hours per month.
    \item Let \( \text{price}_{p} \) be the selling price per batch of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) to be produced to fulfill a contract.
    \item Let \( \text{standard\_cost} \) be the labor cost per hour up to a limit.
    \item Let \( \text{overtime\_cost} \) be the labor cost per hour after the limit.
    \item Let \( \text{overtime\_hour} \) be the maximum hours before overtime charges apply.
    \item Let \( \text{min\_profit} \) be the minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
Let \( x_{p} \) be the number of batches of part \( p \) produced.

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot x_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_{p} \right) \right) - \text{Labor Costs}
\]

\subsection*{Labor Costs}
\[
\text{Labor Costs} = 
\begin{cases} 
\text{standard\_cost} \cdot \text{overtime\_hour} & \text{if } \sum_{p=1}^{P} \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_{p} \leq \text{overtime\_hour} \\ 
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left( \sum_{p=1}^{P} \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_{p} - \text{overtime\_hour} \right) & \text{if } \sum_{p=1}^{P} \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_{p} > \text{overtime\_hour}
\end{cases}
\]

\subsection*{Constraints}
1. Machine Availability Constraints:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_{p} \leq \text{available}_{m} \quad \text{for all } m = 1, \ldots, M
\]

2. Minimum Batches Requirement:
\[
x_{p} \geq \text{min\_batches}_{p} \quad \text{for all } p = 1, \ldots, P
\]

3. Minimum Profit Requirement:
\[
\text{Total Profit} \geq \text{min\_profit}
\]

4. Non-negativity Constraints:
\[
x_{p} \geq 0 \quad \text{for all } p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load the data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

#### Problem setup
problem = pulp.LpProblem("Auto_Parts_Manufacturer_Problem", pulp.LpMaximize)

#### Decision Variables
P = len(data['prices'])  #### Number of different parts
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))

#### Calculate total production time
total_time = pulp.lpSum(
    data['time_required'][m][p] * x[p] for m in range(len(data['time_required'])) for p in range(P)
)

#### Labor cost calculation
labor_cost = pulp.lpSum([
    data['standard_cost'] * data['overtime_hour'] if total_time <= data['overtime_hour'] 
    else data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (total_time - data['overtime_hour'])
])

#### Full objective
total_profit = profit - pulp.lpSum(data['machine_costs'][m] * total_time for m in range(len(data['machine_costs']))) - labor_cost
problem += total_profit

#### Constraints

#### Machine Availability Constraints
M = len(data['availability'])  #### Number of different machines
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m], f"Availability_Constraint_{m}"

#### Minimum Batches Requirement
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

#### Minimum Profit Requirement
problem += total_profit >= data['min_profit'], "Min_Profit_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

