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

\textbf{Indices:}
\begin{itemize}
    \item $p$: index for parts, where $p = 1, \ldots, P$
    \item $m$: index for machines, where $m = 1, \ldots, M$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{m,p}$: time required (in hours) on machine $m$ to produce a batch of part $p$
    \item $cost_{m}$: cost per hour of using machine $m$
    \item $available_{m}$: availability of machine $m$ (in hours) per month
    \item $price_{p}$: selling price of a batch of part $p$
    \item $min\_batches_{p}$: minimum number of batches of part $p$ required
    \item $standard\_cost$: standard labor cost per hour
    \item $overtime\_cost$: overtime labor cost per hour
    \item $overtime\_hour$: threshold hours for standard labor cost
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $batches_{p}$: number of batches of part $p$ produced
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})) - \text{Labor Cost}
\]

\textbf{Labor Cost Calculation:}
\[
\text{Labor Cost} = 
\begin{cases} 
    standard\_cost \cdot hours & \text{if } hours \leq overtime\_hour \\
    standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (hours - overtime\_hour) & \text{if } hours > overtime\_hour 
\end{cases}
\]
where $hours = \sum_{m=1}^{M}(time_{m,p} \cdot batches_{p})$.

\textbf{Constraints:}
\begin{align*}
    & \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m \in \{2, \ldots, M\} \\
    & batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, \ldots, P\} \\
    & batches_{p} \geq 0, \quad \forall p \in \{1, \ldots, P\} \\
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $batches$: [batches$_{p}$ for $p$ in 1, ..., $P$]
    \item total\_profit: $Z$
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

\textbf{Indices:}
\begin{itemize}
    \item $p$: index for parts, where $p = 1, \ldots, P$
    \item $m$: index for machines, where $m = 1, \ldots, M$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{m,p}$: time required (in hours) on machine $m$ to produce a batch of part $p$
    \item $cost_{m}$: cost per hour of using machine $m$
    \item $available_{m}$: availability of machine $m$ (in hours) per month
    \item $price_{p}$: selling price of a batch of part $p$
    \item $min\_batches_{p}$: minimum number of batches of part $p$ required
    \item $standard\_cost$: standard labor cost per hour
    \item $overtime\_cost$: overtime labor cost per hour
    \item $overtime\_hour$: threshold hours for standard labor cost
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $batches_{p}$: number of batches of part $p$ produced
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})) - \text{Labor Cost}
\]

\textbf{Labor Cost Calculation:}
\[
\text{Labor Cost} = 
\begin{cases} 
    standard\_cost \cdot hours & \text{if } hours \leq overtime\_hour \\
    standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (hours - overtime\_hour) & \text{if } hours > overtime\_hour 
\end{cases}
\]
where $hours = \sum_{m=1}^{M}(time_{m,p} \cdot batches_{p})$.

\textbf{Constraints:}
\begin{align*}
    & \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m \in \{2, \ldots, M\} \\
    & batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, \ldots, P\} \\
    & batches_{p} \geq 0, \quad \forall p \in \{1, \ldots, P\} \\
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $batches$: [batches$_{p}$ for $p$ in 1, ..., $P$]
    \item total\_profit: $Z$
\end{itemize}

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

#### Model initialization
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(data['NumParts']), lowBound=0, cat='Continuous')

#### Objective Function
total_revenue = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts']))
total_cost = pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines']))
hours = pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for m in range(data['NumMachines']) for p in range(data['NumParts']))
labor_cost = pulp.lpSum(data['StandardCost'] * pulp.lpMin(hours[m], data['OvertimeHour'][m]) for m in range(data['NumMachines'])) + \
             pulp.lpSum(data['OvertimeCost'] * (hours[m] - data['OvertimeHour'][m]) for m in range(data['NumMachines']) if hours[m] > data['OvertimeHour'][m])
objective_function = total_revenue - total_cost - labor_cost

problem += objective_function

#### Constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]

for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p]

#### Solve the problem
problem.solve()

#### Output results
batches_result = [batches[p].varValue for p in range(data['NumParts'])]
print(f'Batches: {batches_result}')
print(f'Total Profit: <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

