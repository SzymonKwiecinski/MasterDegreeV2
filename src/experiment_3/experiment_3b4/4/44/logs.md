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

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P]
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

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the time in hours required to produce a batch of 100 of part \( p \) on machine \( m \).
    \item Let \( \text{cost}_{m} \) be the cost per hour for using machine \( m \).
    \item Let \( \text{available}_{m} \) be the available hours per month for machine \( m \).
    \item Let \( \text{price}_{p} \) be the selling price per batch of 100 of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) that must be produced each month to fulfill a contract.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{batches}_{p} \) be the number of batches of part \( p \) to be produced each month.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit, which is the total revenue minus the total cost of machine usage:
\[
\text{Maximize} \quad \text{total\_profit} = \sum_{p=1}^{P} \text{price}_{p} \times \text{batches}_{p} - \sum_{m=1}^{M} \text{cost}_{m} \times \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_{p}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine availability constraints for each machine \( m \):
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
    \]
    \item Minimum production constraints for each part \( p \):
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

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the time in hours required to produce a batch of 100 of part \( p \) on machine \( m \).
    \item Let \( \text{cost}_{m} \) be the cost per hour for using machine \( m \).
    \item Let \( \text{available}_{m} \) be the available hours per month for machine \( m \).
    \item Let \( \text{price}_{p} \) be the selling price per batch of 100 of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) that must be produced each month to fulfill a contract.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{batches}_{p} \) be the number of batches of part \( p \) to be produced each month.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit, which is the total revenue minus the total cost of machine usage:
\[
\text{Maximize} \quad \text{total\_profit} = \sum_{p=1}^{P} \text{price}_{p} \times \text{batches}_{p} - \sum_{m=1}^{M} \text{cost}_{m} \times \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_{p}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine availability constraints for each machine \( m \):
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
    \]
    \item Minimum production constraints for each part \( p \):
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
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


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
    'min_batches': [10, 10, 10, 10]
}

#### Parameters
P = len(data['prices'])  #### number of parts
M = len(data['machine_costs'])  #### number of machines

#### Initialize problem
problem = pulp.LpProblem("MaximizeProfit", pulp.LpMaximize)

#### Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function
total_profit = (
    pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - 
    pulp.lpSum([data['machine_costs'][m] * 
                pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) 
                for m in range(M)])
)

problem += total_profit

#### Constraints
#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]

#### Minimum production constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

