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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \), where \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): Time required (in hours) on machine \( m \) to produce one batch of part \( p \).
    \item \( cost_{m} \): Cost per hour for using machine \( m \).
    \item \( available_{m} \): Available hours per month for machine \( m \).
    \item \( price_{p} \): Selling price per batch of part \( p \).
    \item \( min\_batches_{p} \): Minimum batches of part \( p \) that must be produced to fulfill a contract.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{p=1}^{P} (price_{p} \cdot b_p) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \right)
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_{m}, \quad \forall m = 1, 2, \ldots, M
\]

2. Minimum production requirements:
\[
b_p \geq min\_batches_{p}, \quad \forall p = 1, 2, \ldots, P
\]

3. Non-negativity:
\[
b_p \geq 0, \quad \forall p = 1, 2, \ldots, P
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The number of batches of each part produced (\( b_p \) for \( p = 1, \ldots, P \)).
    \item The total profit for the month.
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
    \item \( time_{m,p} \): Time required (in hours) on machine \( m \) to produce one batch of part \( p \).
    \item \( cost_{m} \): Cost per hour for using machine \( m \).
    \item \( available_{m} \): Available hours per month for machine \( m \).
    \item \( price_{p} \): Selling price per batch of part \( p \).
    \item \( min\_batches_{p} \): Minimum batches of part \( p \) that must be produced to fulfill a contract.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{p=1}^{P} (price_{p} \cdot b_p) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \right)
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_{m}, \quad \forall m = 1, 2, \ldots, M
\]

2. Minimum production requirements:
\[
b_p \geq min\_batches_{p}, \quad \forall p = 1, 2, \ldots, P
\]

3. Non-negativity:
\[
b_p \geq 0, \quad \forall p = 1, 2, \ldots, P
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The number of batches of each part produced (\( b_p \) for \( p = 1, \ldots, P \)).
    \item The total profit for the month.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

#### Constraints
#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m+1}"

#### Minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_Constraint_{p+1}"

#### Solve the problem
problem.solve()

#### Output the results
for p in range(P):
    print(f'Batches of part {p + 1} produced: {batches[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

