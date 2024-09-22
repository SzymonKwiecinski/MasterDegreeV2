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

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce a batch of 100 part $p$
    \item $cost_{m}$: Cost (in dollars per hour) for using machine $m$
    \item $available_{m}$: Availability (in hours) of machine $m$ per month
    \item $price_{p}$: Price (in dollars) per batch of part $p$
    \item $min\_batches_{p}$: Minimum required batches of part $p$ per month
    \item $standard\_cost$: Labor cost (in dollars per hour) for up to $overtime\_hour$ hours
    \item $overtime\_cost$: Labor cost (in dollars per hour) for overtime
    \item $overtime\_hour$: Maximum hours before overtime costs apply
    \item $min\_profit$: Minimum desired profit
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches produced for part $p$, for $p = 1, \ldots, P$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P}(time_{m,p} \cdot batches_{p}))
\]

\subsection*{Constraints}

\begin{align*}
\text{Machine Availability Constraints:} \quad & \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m = 1, \ldots, M \\
\text{Minimum Batches Constraints:} \quad & batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P \\
\text{Labor Costs for Machine 1:} \quad & \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) \leq \text{Allocated Hours for Machine 1} \\
& \text{if within } overtime\_hour: \quad \text{Labor Cost} = standard\_cost \cdot \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) \\
& \text{if exceeding } overtime\_hour: \\
& \quad \text{Labor Cost} = \left( standard\_cost \cdot overtime\_hour \right) + \left( overtime\_cost \cdot \left(\sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) - overtime\_hour \right) \right) \\
\text{Profit Requirement:} \quad & Z \geq min\_profit
\end{align*}

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

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce a batch of 100 part $p$
    \item $cost_{m}$: Cost (in dollars per hour) for using machine $m$
    \item $available_{m}$: Availability (in hours) of machine $m$ per month
    \item $price_{p}$: Price (in dollars) per batch of part $p$
    \item $min\_batches_{p}$: Minimum required batches of part $p$ per month
    \item $standard\_cost$: Labor cost (in dollars per hour) for up to $overtime\_hour$ hours
    \item $overtime\_cost$: Labor cost (in dollars per hour) for overtime
    \item $overtime\_hour$: Maximum hours before overtime costs apply
    \item $min\_profit$: Minimum desired profit
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches produced for part $p$, for $p = 1, \ldots, P$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P}(time_{m,p} \cdot batches_{p}))
\]

\subsection*{Constraints}

\begin{align*}
\text{Machine Availability Constraints:} \quad & \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m = 1, \ldots, M \\
\text{Minimum Batches Constraints:} \quad & batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P \\
\text{Labor Costs for Machine 1:} \quad & \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) \leq \text{Allocated Hours for Machine 1} \\
& \text{if within } overtime\_hour: \quad \text{Labor Cost} = standard\_cost \cdot \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) \\
& \text{if exceeding } overtime\_hour: \\
& \quad \text{Labor Cost} = \left( standard\_cost \cdot overtime\_hour \right) + \left( overtime\_cost \cdot \left(\sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) - overtime\_hour \right) \right) \\
\text{Profit Requirement:} \quad & Z \geq min\_profit
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Integer') for p in range(P)]

#### Objective function components
total_revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
total_cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

#### Total profit
profit = total_revenue - total_cost

#### Set the objective
problem += profit

#### Constraints
#### Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m])

#### Minimum profit constraint
problem += profit >= data['min_profit']

#### Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

