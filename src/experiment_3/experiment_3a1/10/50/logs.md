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
- Extra available time for machine \var{m} can be acquired at $\var{extra_costs_{m}}/hour. 
- Up to \var{max_extra_{m}} hours can be purchased for each machine \var{m}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "extra_costs": [extra_cost_{m} for m in 1, ..., M],
    "max_extra": [max_extra_{m} for m in 1, ..., M]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{extra_time} denotes the additional hours purchased for each machine \var{m}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "extra_time": [extra_time_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Auto Parts Manufacturing}
\author{}
\date{}
\maketitle

\section*{Variables}
Let:
\begin{itemize}
    \item \( b_p \): Number of batches of part \( p \) produced (for \( p = 1, \ldots, P \))
    \item \( e_m \): Extra hours purchased for machine \( m \) (for \( m = 1, \ldots, M \))
    \item \( total\_profit \): Total profit obtained for the month
\end{itemize}

\section*{Parameters}
Given:
\begin{itemize}
    \item \( time_{m,p} \): Time (in hours) required on machine \( m \) to produce one batch of part \( p \)
    \item \( cost_{m} \): Cost per hour for using machine \( m \)
    \item \( available_{m} \): Availability (in hours) of machine \( m \) per month
    \item \( price_{p} \): Selling price per batch of part \( p \)
    \item \( min\_batches_{p} \): Minimum number of batches of part \( p \) that must be produced each month
    \item \( extra\_costs_{m} \): Cost per hour for purchasing extra hours for machine \( m \)
    \item \( max\_extra_{m} \): Maximum extra hours that can be purchased for machine \( m \)
\end{itemize}

\section*{Objective Function}
Maximize total profit:
\[
total\_profit = \sum_{p=1}^{P} (price_{p} \cdot b_p) - \sum_{m=1}^{M} (cost_{m} \cdot (availability_{m} + e_m)) - \sum_{m=1}^{M} (extra\_costs_{m} \cdot e_m)
\]

\section*{Constraints}

1. **Machine Hour Constraints**:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot b_p) + e_m \leq available_{m} + max\_extra_{m} \quad \forall m \in \{1, \ldots, M\}
\]

2. **Production Minimum Requirements**:
\[
b_p \geq min\_batches_{p} \quad \forall p \in \{1, \ldots, P\}
\]

3. **Extra Time Limits**:
\[
0 \leq e_m \leq max\_extra_{m} \quad \forall m \in \{1, \ldots, M\}
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

\title{Linear Programming Model for Auto Parts Manufacturing}
\author{}
\date{}
\maketitle

\section*{Variables}
Let:
\begin{itemize}
    \item \( b_p \): Number of batches of part \( p \) produced (for \( p = 1, \ldots, P \))
    \item \( e_m \): Extra hours purchased for machine \( m \) (for \( m = 1, \ldots, M \))
    \item \( total\_profit \): Total profit obtained for the month
\end{itemize}

\section*{Parameters}
Given:
\begin{itemize}
    \item \( time_{m,p} \): Time (in hours) required on machine \( m \) to produce one batch of part \( p \)
    \item \( cost_{m} \): Cost per hour for using machine \( m \)
    \item \( available_{m} \): Availability (in hours) of machine \( m \) per month
    \item \( price_{p} \): Selling price per batch of part \( p \)
    \item \( min\_batches_{p} \): Minimum number of batches of part \( p \) that must be produced each month
    \item \( extra\_costs_{m} \): Cost per hour for purchasing extra hours for machine \( m \)
    \item \( max\_extra_{m} \): Maximum extra hours that can be purchased for machine \( m \)
\end{itemize}

\section*{Objective Function}
Maximize total profit:
\[
total\_profit = \sum_{p=1}^{P} (price_{p} \cdot b_p) - \sum_{m=1}^{M} (cost_{m} \cdot (availability_{m} + e_m)) - \sum_{m=1}^{M} (extra\_costs_{m} \cdot e_m)
\]

\section*{Constraints}

1. **Machine Hour Constraints**:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot b_p) + e_m \leq available_{m} + max\_extra_{m} \quad \forall m \in \{1, \ldots, M\}
\]

2. **Production Minimum Requirements**:
\[
b_p \geq min\_batches_{p} \quad \forall p \in \{1, \ldots, P\}
\]

3. **Extra Time Limits**:
\[
0 \leq e_m \leq max\_extra_{m} \quad \forall m \in \{1, \ldots, M\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

#### Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  #### Number of parts
M = len(availability)  #### Number of machines

#### Create the linear programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Define decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_hours = pulp.LpVariable.dicts("extra_hours", range(M), lowBound=0)

#### Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (availability[m] + extra_hours[m]) for m in range(M)) - \
         pulp.lpSum(extra_costs[m] * extra_hours[m] for m in range(M))

problem += profit

#### Constraints
#### Machine Hour Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_hours[m] <= availability[m] + max_extra[m]

#### Production Minimum Requirements
for p in range(P):
    problem += batches[p] >= min_batches[p]

#### Extra Time Limits
for m in range(M):
    problem += extra_hours[m] <= max_extra[m]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

