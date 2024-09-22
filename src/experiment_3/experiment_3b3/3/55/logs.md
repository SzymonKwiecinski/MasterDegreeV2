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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} \left( cost_m \cdot \left( \sum_{p=1}^{P} time_{m,p} \cdot b_p \right) \right) - \sum_{p=1}^{P} \text{Labor Cost}
\]

The labor cost can be calculated as:
\[
\text{Labor Cost} = \begin{cases}
    \text{standard\_cost} \cdot \text{overtime\_hour} & \text{if } \sum_{p=1}^{P} time_{1,p} \cdot b_p \leq \text{overtime\_hour} \\
    \text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left( \sum_{p=1}^{P} time_{1,p} \cdot b_p - \text{overtime\_hour} \right) & \text{otherwise }
\end{cases}
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} time_{m,p} \cdot b_p \leq available_m \quad \forall m \in \{2, \ldots, M\}
\]
2. Minimum production requirement for each part:
\[
b_p \geq min\_batches_p \quad \forall p \in \{1, \ldots, P\}
\]
3. Profit constraint:
\[
Z \geq min\_profit
\]
4. Non-negativity constraints:
\[
b_p \geq 0 \quad \forall p \in \{1, \ldots, P\}
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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} \left( cost_m \cdot \left( \sum_{p=1}^{P} time_{m,p} \cdot b_p \right) \right) - \sum_{p=1}^{P} \text{Labor Cost}
\]

The labor cost can be calculated as:
\[
\text{Labor Cost} = \begin{cases}
    \text{standard\_cost} \cdot \text{overtime\_hour} & \text{if } \sum_{p=1}^{P} time_{1,p} \cdot b_p \leq \text{overtime\_hour} \\
    \text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left( \sum_{p=1}^{P} time_{1,p} \cdot b_p - \text{overtime\_hour} \right) & \text{otherwise }
\end{cases}
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} time_{m,p} \cdot b_p \leq available_m \quad \forall m \in \{2, \ldots, M\}
\]
2. Minimum production requirement for each part:
\[
b_p \geq min\_batches_p \quad \forall p \in \{1, \ldots, P\}
\]
3. Profit constraint:
\[
Z \geq min\_profit
\]
4. Non-negativity constraints:
\[
b_p \geq 0 \quad \forall p \in \{1, \ldots, P\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
batches = [pulp.LpVariable(f'b_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

#### Objective Function

#### Labor Cost Calculation
labor_cost_expr = (
    pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
)
labor_cost = (data['standard_cost'] * data['overtime_hour'] +
              data['overtime_cost'] * (labor_cost_expr - data['overtime_hour']))

#### Total Cost
total_machine_cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(1, M))
total_revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))

#### Profit Objective
problem += total_revenue - total_machine_cost - labor_cost, "Total_Profit"

#### Constraints

#### Machine availability constraints
for m in range(1, M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f'Machine_{m}_availability'

#### Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f'Min_batches_{p}'

#### Profit constraint
problem += total_revenue - total_machine_cost - labor_cost >= data['min_profit'], "Minimum_Profit"

#### Solve
problem.solve()

#### Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

