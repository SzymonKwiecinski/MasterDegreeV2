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
- Machine \var{M} and Machine \var{M-1} can share availability.
- Individual availability conditions for Machine \var{M} and Machine \var{M-1} can be disregarded.
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

\title{Linear Programming Formulation for Auto Parts Manufacturer}
\author{}
\date{}
\maketitle

\section*{Problem Description}

A division of an auto parts manufacturer produces $P$ different parts using $M$ different machines. Each part $p$ is manufactured in batches of 100 units. The production of each part $p$ on machine $m$ requires a certain amount of time, incurs specific costs, and is bound by the machine's availability.

\section*{Model Formulation}

Define the decision variables:
\[
batches_p \quad \text{for all } p = 1, \ldots, P
\]
where $batches_p$ represents the number of batches of part $p$ to produce.

\subsection*{Objective Function}

The aim is to maximize profit. The profit is the revenue from selling parts minus the cost of using machines. The objective function is:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \times batches_p \right) - \sum_{m=1}^{M} \left( cost_{m} \times \sum_{p=1}^{P} time_{m,p} \times batches_p \right)
\]

\subsection*{Constraints}

1. **Machine Time Constraints:**
   \[
   \sum_{p=1}^{P} \left( time_{m,p} \times batches_p \right) \leq available_{m} \quad \text{for all } m = 1, \ldots, M-2
   \]

2. **Shared Availability for Machine $M$ and Machine $M-1$:**
   \[
   \sum_{p=1}^{P} \left( time_{M,p} \times batches_p \right) + \sum_{p=1}^{P} \left( time_{M-1,p} \times batches_p \right) \leq available_{M} + available_{M-1}
   \]

3. **Minimum Batch Constraints:**
   \[
   batches_p \geq min\_batches_{p} \quad \text{for all } p = 1, \ldots, P
   \]

4. **Non-negativity Constraints:**
   \[
   batches_p \geq 0 \quad \text{for all } p = 1, \ldots, P
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

\title{Linear Programming Formulation for Auto Parts Manufacturer}
\author{}
\date{}
\maketitle

\section*{Problem Description}

A division of an auto parts manufacturer produces $P$ different parts using $M$ different machines. Each part $p$ is manufactured in batches of 100 units. The production of each part $p$ on machine $m$ requires a certain amount of time, incurs specific costs, and is bound by the machine's availability.

\section*{Model Formulation}

Define the decision variables:
\[
batches_p \quad \text{for all } p = 1, \ldots, P
\]
where $batches_p$ represents the number of batches of part $p$ to produce.

\subsection*{Objective Function}

The aim is to maximize profit. The profit is the revenue from selling parts minus the cost of using machines. The objective function is:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \times batches_p \right) - \sum_{m=1}^{M} \left( cost_{m} \times \sum_{p=1}^{P} time_{m,p} \times batches_p \right)
\]

\subsection*{Constraints}

1. **Machine Time Constraints:**
   \[
   \sum_{p=1}^{P} \left( time_{m,p} \times batches_p \right) \leq available_{m} \quad \text{for all } m = 1, \ldots, M-2
   \]

2. **Shared Availability for Machine $M$ and Machine $M-1$:**
   \[
   \sum_{p=1}^{P} \left( time_{M,p} \times batches_p \right) + \sum_{p=1}^{P} \left( time_{M-1,p} \times batches_p \right) \leq available_{M} + available_{M-1}
   \]

3. **Minimum Batch Constraints:**
   \[
   batches_p \geq min\_batches_{p} \quad \text{for all } p = 1, \ldots, P
   \]

4. **Non-negativity Constraints:**
   \[
   batches_p \geq 0 \quad \text{for all } p = 1, \ldots, P
   \]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data input from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

#### Extracting data
time_required = data['time_required']  #### time_required[m][p]
machine_costs = data['machine_costs']  #### cost for each machine
availability = data['availability']      #### available time for each machine
prices = data['prices']                  #### selling price for each part
min_batches = data['min_batches']        #### minimum batches for each part

#### Define the number of parts and machines
P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit

#### Constraints
#### Machine Time Constraints
for m in range(M - 1):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

#### Shared Availability for Machine M and Machine M-1
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + \
           pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1] + availability[M-2]

#### Minimum Batch Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

