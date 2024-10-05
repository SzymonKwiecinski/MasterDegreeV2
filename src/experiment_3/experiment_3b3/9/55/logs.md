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

\subsection*{Sets}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): time required (in hours) on machine \( m \) for producing a batch of part \( p \).
    \item \( \text{cost}_{m} \): cost per hour for using machine \( m \).
    \item \( \text{available}_{m} \): available hours per month for machine \( m \).
    \item \( \text{price}_{p} \): price received for each batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): minimum batches of part \( p \) to be produced each month.
    \item \( \text{standard\_cost} \): standard labor cost per hour for machine 1.
    \item \( \text{overtime\_cost} \): overtime labor cost per hour for machine 1.
    \item \( \text{overtime\_hour} \): hours before overtime applies.
    \item \( \text{min\_profit} \): minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_{p} \) be the number of batches produced for part \( p \) (for \( p = 1, \ldots, P \)).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot x_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_{p} \right) - \text{Labor Cost}
\]

Where the Labor Cost for machine 1 is defined as follows:

\[
\text{Labor Cost} = 
\begin{cases}
\text{standard\_cost} \cdot \text{total\_time}_{1} & \text{if } \text{total\_time}_{1} \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{total\_time}_{1} - \text{overtime\_hour}) & \text{otherwise}
\end{cases}
\]

Where:

\[
\text{total\_time}_{1} = \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_{p}
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_{p} \leq \text{available}_{m} & \text{for } m = 1, \ldots, M \\
2. & \quad x_{p} \geq \text{min\_batches}_{p} & \text{for } p = 1, \ldots, P \\
3. & \quad \text{Total Profit} \geq \text{min\_profit} \\
4. & \quad x_{p} \geq 0 \quad \text{(non-negativity)} & \text{for } p = 1, \ldots, P
\end{align*}

\subsection*{Output}
The output should provide:
\begin{itemize}
    \item Batches produced for each part: \( \{ x_{p} \}_{p=1}^{P} \)
    \item Total profit: \( \text{Total Profit} \)
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

\subsection*{Sets}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): time required (in hours) on machine \( m \) for producing a batch of part \( p \).
    \item \( \text{cost}_{m} \): cost per hour for using machine \( m \).
    \item \( \text{available}_{m} \): available hours per month for machine \( m \).
    \item \( \text{price}_{p} \): price received for each batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): minimum batches of part \( p \) to be produced each month.
    \item \( \text{standard\_cost} \): standard labor cost per hour for machine 1.
    \item \( \text{overtime\_cost} \): overtime labor cost per hour for machine 1.
    \item \( \text{overtime\_hour} \): hours before overtime applies.
    \item \( \text{min\_profit} \): minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_{p} \) be the number of batches produced for part \( p \) (for \( p = 1, \ldots, P \)).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot x_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_{p} \right) - \text{Labor Cost}
\]

Where the Labor Cost for machine 1 is defined as follows:

\[
\text{Labor Cost} = 
\begin{cases}
\text{standard\_cost} \cdot \text{total\_time}_{1} & \text{if } \text{total\_time}_{1} \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{total\_time}_{1} - \text{overtime\_hour}) & \text{otherwise}
\end{cases}
\]

Where:

\[
\text{total\_time}_{1} = \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_{p}
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_{p} \leq \text{available}_{m} & \text{for } m = 1, \ldots, M \\
2. & \quad x_{p} \geq \text{min\_batches}_{p} & \text{for } p = 1, \ldots, P \\
3. & \quad \text{Total Profit} \geq \text{min\_profit} \\
4. & \quad x_{p} \geq 0 \quad \text{(non-negativity)} & \text{for } p = 1, \ldots, P
\end{align*}

\subsection*{Output}
The output should provide:
\begin{itemize}
    \item Batches produced for each part: \( \{ x_{p} \}_{p=1}^{P} \)
    \item Total profit: \( \text{Total Profit} \)
\end{itemize}

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

P = len(data['prices'])
M = len(data['machine_costs'])

#### Decision Variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Objective Function
total_time_1 = pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(P))
labor_cost = (
    data['standard_cost'] * total_time_1
    if total_time_1 <= data['overtime_hour']
    else data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (total_time_1 - data['overtime_hour'])
)

total_profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - pulp.lpSum(
    data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M)
) - labor_cost

problem += total_profit

#### Constraints
#### Machine availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

#### Minimum batches
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

#### Minimum profit
problem += total_profit >= data['min_profit']

#### Solve
problem.solve()

#### Output
for p in range(P):
    print(f'Batches produced for part {p+1}: {x[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

