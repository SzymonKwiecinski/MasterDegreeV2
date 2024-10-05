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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts produced.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the time required (in hours) on machine \( m \) to produce a batch of 100 part \( p \).
    \item Let \( \text{cost}_{m} \) be the cost per hour for using machine \( m \).
    \item Let \( \text{available}_{m} \) be the availability of machine \( m \) (in hours) per month.
    \item Let \( \text{price}_{p} \) be the price per batch of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) that must be produced per month.
    \item Let \( \text{standard\_cost} \) be the standard labor cost per hour.
    \item Let \( \text{overtime\_cost} \) be the labor cost per hour after \( \text{overtime\_hour} \).
    \item Let \( \text{overtime\_hour} \) be the number of hours up to which the standard cost applies.
    \item Let \( \text{min\_profit} \) be the minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{batches}_{p} \) be the number of batches produced for part \( p \).

\subsection*{Objective Function}
Maximize total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} - \sum_{m=1}^{M} \text{cost}_{m} \cdot \frac{\text{time}_{m,p} \cdot \text{batches}_{p}}{100} \right) - \text{labor\_cost}
\]

where \( \text{labor\_cost} \) considers standard and overtime labor costs.

\subsection*{Constraints}
\begin{itemize}
    \item Availability Constraints for each machine:
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m} \quad \text{for each } m = 1, \ldots, M
    \]

    \item Minimum Batches Requirement:
    \[
    \text{batches}_{p} \geq \text{min\_batches}_{p} \quad \text{for each } p = 1, \ldots, P
    \]

    \item Minimum Profit Constraint:
    \[
    \text{Total Profit} \geq \text{min\_profit}
    \]

    \item Labor Cost Calculation:
    \[
    \text{labor\_cost} = \begin{cases} 
    \text{standard\_cost} \cdot \text{time} & \text{if } \text{time} \leq \text{overtime\_hour} \\
    \text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{time} - \text{overtime\_hour}) & \text{if } \text{time} > \text{overtime\_hour}
    \end{cases}
    \]
    where \( \text{time} = \sum_{m=1}^{M} \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \).
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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts produced.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the time required (in hours) on machine \( m \) to produce a batch of 100 part \( p \).
    \item Let \( \text{cost}_{m} \) be the cost per hour for using machine \( m \).
    \item Let \( \text{available}_{m} \) be the availability of machine \( m \) (in hours) per month.
    \item Let \( \text{price}_{p} \) be the price per batch of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) that must be produced per month.
    \item Let \( \text{standard\_cost} \) be the standard labor cost per hour.
    \item Let \( \text{overtime\_cost} \) be the labor cost per hour after \( \text{overtime\_hour} \).
    \item Let \( \text{overtime\_hour} \) be the number of hours up to which the standard cost applies.
    \item Let \( \text{min\_profit} \) be the minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{batches}_{p} \) be the number of batches produced for part \( p \).

\subsection*{Objective Function}
Maximize total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} - \sum_{m=1}^{M} \text{cost}_{m} \cdot \frac{\text{time}_{m,p} \cdot \text{batches}_{p}}{100} \right) - \text{labor\_cost}
\]

where \( \text{labor\_cost} \) considers standard and overtime labor costs.

\subsection*{Constraints}
\begin{itemize}
    \item Availability Constraints for each machine:
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m} \quad \text{for each } m = 1, \ldots, M
    \]

    \item Minimum Batches Requirement:
    \[
    \text{batches}_{p} \geq \text{min\_batches}_{p} \quad \text{for each } p = 1, \ldots, P
    \]

    \item Minimum Profit Constraint:
    \[
    \text{Total Profit} \geq \text{min\_profit}
    \]

    \item Labor Cost Calculation:
    \[
    \text{labor\_cost} = \begin{cases} 
    \text{standard\_cost} \cdot \text{time} & \text{if } \text{time} \leq \text{overtime\_hour} \\
    \text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{time} - \text{overtime\_hour}) & \text{if } \text{time} > \text{overtime\_hour}
    \end{cases}
    \]
    where \( \text{time} = \sum_{m=1}^{M} \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \).
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

#### Parameters
P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Problem
problem = pulp.LpProblem("AutoPartsProfitMaximization", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Objective Function: Maximize Total Profit
profits = [
    data['prices'][p] * batches[p] - pulp.lpSum(
        data['machine_costs'][m] * data['time_required'][m][p] * batches[p] / 100 for m in range(M)
    ) for p in range(P)
]

total_time = pulp.lpSum(data['time_required'][m][p] * batches[p] for m in range(M) for p in range(P))
labor_cost = pulp.LpVariable("labor_cost", lowBound=0, cat='Continuous')
problem += pulp.lpSum(profits) - labor_cost

#### Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

problem += pulp.lpSum(profits) - labor_cost >= data['min_profit']

#### Labor cost calculation based on overtime
problem += labor_cost == (
    data['standard_cost'] * total_time
    if total_time <= data['overtime_hour']
    else data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (total_time - data['overtime_hour'])
)

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


