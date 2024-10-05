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
To solve this linear programming problem, we need to set up an optimization model with the objective of maximizing profit, which is calculated as the total revenue from selling parts minus the total operating costs of using machines. Here is the mathematical formulation using LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts.
    \item $M$: Number of different machines.
    \item $time_{m,p}$: Hours required of machine $m$ to produce a batch of part $p$.
    \item $cost_{m}$: Cost per hour of using machine $m$.
    \item $available_{m}$: Available machine-hours for machine $m$ per month.
    \item $price_{p}$: Selling price per batch of part $p$.
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ required to be produced each month.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to be produced (integer).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) - \sum_{m=1}^{M} \left( cost_{m} \times \sum_{p=1}^{P} \left( time_{m,p} \times batches_{p} \right) \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine availability constraint for each machine $m$:
    \[
    \sum_{p=1}^{P} \left( time_{m,p} \times batches_{p} \right) \leq available_{m}, \quad \forall m = 1, \ldots, M
    \]
    \item Minimum production constraint for each part $p$:
    \[
    batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P
    \]
    \item Non-negativity and integer constraints:
    \[
    batches_{p} \geq 0, \quad batches_{p} \in \mathbb{Z}, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\end{document}
```

This model will help determine the optimal number of batches of each part to produce in order to maximize the profit, subject to machine availability and contractual obligations. The decision variable values for $batches_{p}$ will provide the output for the optimal number of batches for each part, and the objective function value will give the total profit.

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
    \item $P$: Number of different parts.
    \item $M$: Number of different machines.
    \item $time_{m,p}$: Hours required of machine $m$ to produce a batch of part $p$.
    \item $cost_{m}$: Cost per hour of using machine $m$.
    \item $available_{m}$: Available machine-hours for machine $m$ per month.
    \item $price_{p}$: Selling price per batch of part $p$.
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ required to be produced each month.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to be produced (integer).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) - \sum_{m=1}^{M} \left( cost_{m} \times \sum_{p=1}^{P} \left( time_{m,p} \times batches_{p} \right) \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine availability constraint for each machine $m$:
    \[
    \sum_{p=1}^{P} \left( time_{m,p} \times batches_{p} \right) \leq available_{m}, \quad \forall m = 1, \ldots, M
    \]
    \item Minimum production constraint for each part $p$:
    \[
    batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P
    \]
    \item Non-negativity and integer constraints:
    \[
    batches_{p} \geq 0, \quad batches_{p} \in \mathbb{Z}, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

P = len(data['prices'])  #### Number of different parts
M = len(data['machine_costs'])  #### Number of different machines

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

#### Objective Function
profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)])
cost = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit - cost

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

