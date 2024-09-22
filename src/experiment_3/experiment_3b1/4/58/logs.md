# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- Machine \var{1} requires a setup time of \var{setup_time_{p}} hours before it can be used for each part \var{p}.
- Other machines do not require a setup time.
- There are no minimum production quantities for any part.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "setup_time": [setup_time_{p} for p in 1, ..., P]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{setup_flags_{p}} indicates whether \var{part_{p}} is set up or not.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "setup_flags": [setup_flag_{p} for p in 1, ..., P],
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

\subsection*{Variables}
Let:
\begin{align*}
    &batches_{p} \quad \text{= number of batches produced of part } p \quad \text{for } p = 1, \ldots, P \\
    &setup\_flags_{p} \quad \text{= binary variable indicating if part } p \text{ is set up (1) or not (0)} \\
    &total\_profit \quad \text{= total profit obtained for the month}
\end{align*}

\subsection*{Parameters}
\begin{align*}
    &time_{m,p} \quad \text{= time required on machine } m \text{ to produce one batch of part } p \quad \text{for } m = 1, \ldots, M, \; p = 1, \ldots, P \\
    &cost_{m} \quad \text{= cost per hour of machine } m \quad \text{for } m = 1, \ldots, M \\
    &available_{m} \quad \text{= available hours of machine } m \text{ per month} \quad \text{for } m = 1, \ldots, M \\
    &price_{p} \quad \text{= selling price per batch of part } p \quad \text{for } p = 1, \ldots, P \\
    &setup\_time_{p} \quad \text{= setup time required for part } p \text{ on machine 1} \quad \text{for } p = 1, \ldots, P
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
    total\_profit &= \sum_{p=1}^{P} price_{p} \cdot batches_{p} - \sum_{m=1}^{M} \left( cost_{m} \cdot \left( \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} + \sum_{p=1}^{P} setup\_flags_{p} \cdot setup\_time_{p} \cdot \delta_{m,1} \right) \right)
\end{align*}
where $\delta_{m,1}$ is 1 if $m=1$ (indicating machine 1), and 0 otherwise.

\subsection*{Constraints}
1. Machine availability constraints:
\begin{align*}
    \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} + setup\_flags_{p} \cdot setup\_time_{p} \cdot \delta_{m,1} \leq available_{m} \quad \text{for } m = 1, \ldots, M
\end{align*}

2. Non-negativity and binary constraints:
\begin{align*}
    &batches_{p} \geq 0 \quad \text{for } p = 1, \ldots, P \\
    &setup\_flags_{p} \in \{0, 1\} \quad \text{for } p = 1, \ldots, P
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

\section*{Mathematical Model}

\subsection*{Variables}
Let:
\begin{align*}
    &batches_{p} \quad \text{= number of batches produced of part } p \quad \text{for } p = 1, \ldots, P \\
    &setup\_flags_{p} \quad \text{= binary variable indicating if part } p \text{ is set up (1) or not (0)} \\
    &total\_profit \quad \text{= total profit obtained for the month}
\end{align*}

\subsection*{Parameters}
\begin{align*}
    &time_{m,p} \quad \text{= time required on machine } m \text{ to produce one batch of part } p \quad \text{for } m = 1, \ldots, M, \; p = 1, \ldots, P \\
    &cost_{m} \quad \text{= cost per hour of machine } m \quad \text{for } m = 1, \ldots, M \\
    &available_{m} \quad \text{= available hours of machine } m \text{ per month} \quad \text{for } m = 1, \ldots, M \\
    &price_{p} \quad \text{= selling price per batch of part } p \quad \text{for } p = 1, \ldots, P \\
    &setup\_time_{p} \quad \text{= setup time required for part } p \text{ on machine 1} \quad \text{for } p = 1, \ldots, P
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
    total\_profit &= \sum_{p=1}^{P} price_{p} \cdot batches_{p} - \sum_{m=1}^{M} \left( cost_{m} \cdot \left( \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} + \sum_{p=1}^{P} setup\_flags_{p} \cdot setup\_time_{p} \cdot \delta_{m,1} \right) \right)
\end{align*}
where $\delta_{m,1}$ is 1 if $m=1$ (indicating machine 1), and 0 otherwise.

\subsection*{Constraints}
1. Machine availability constraints:
\begin{align*}
    \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} + setup\_flags_{p} \cdot setup\_time_{p} \cdot \delta_{m,1} \leq available_{m} \quad \text{for } m = 1, \ldots, M
\end{align*}

2. Non-negativity and binary constraints:
\begin{align*}
    &batches_{p} \geq 0 \quad \text{for } p = 1, \ldots, P \\
    &setup\_flags_{p} \in \{0, 1\} \quad \text{for } p = 1, \ldots, P
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "setup_time": [12, 8, 4, 0]
}'''

data = json.loads(data)

#### Define parameters
time_required = data['time_required']  #### M x P matrix
machine_costs = data['machine_costs']  #### M array
availability = data['availability']      #### M array
prices = data['prices']                  #### P array
setup_time = data['setup_time']          #### P array

M = len(machine_costs)  #### Number of machines
P = len(prices)         #### Number of parts

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)  #### Number of batches produced
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')  #### Setup flags

#### Objective function
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
               pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
               pulp.lpSum(setup_flags[p] * setup_time[p] * (1 if m == 0 else 0) for p in range(P))) for m in range(M))

problem += total_profit

#### Constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                 pulp.lpSum(setup_flags[p] * setup_time[p] * (1 if m == 0 else 0) for p in range(P)) <= 
                 availability[m])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

