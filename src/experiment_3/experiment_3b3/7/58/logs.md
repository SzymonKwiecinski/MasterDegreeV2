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

\section*{Mathematical Model for the Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required (in hours) on machine $m$ for part $p$ (for $m = 1, \ldots, M$ and $p = 1, \ldots, P$)
    \item $cost_{m}$: Cost per hour of using machine $m$ (for $m = 1, \ldots, M$)
    \item $available_{m}$: Availability of machine $m$ (in hours) per month (for $m = 1, \ldots, M$)
    \item $price_{p}$: Selling price per batch of part $p$ (for $p = 1, \ldots, P$)
    \item $setup\_time_{p}$: Setup time required (in hours) before machine 1 can be used for part $p$ (for $p = 1, \ldots, P$)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches produced for part $p$ (for $p = 1, \ldots, P$)
    \item $setup\_flag_{p}$: Binary variable indicating whether part $p$ is set up ($1$ if set up, $0$ otherwise)
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} \right) - \sum_{m=1}^{M} \left( cost_{m} \cdot \left( \sum_{p=1}^{P} \left( time_{m,p} \cdot batches_{p} \right) + \sum_{p=1}^{P} setup\_time_{p} \cdot setup\_flag_{p} \right) \right)
\]

\subsection*{Constraints}
1. Machine Time Availability:
\[
\sum_{p=1}^{P} \left( time_{m,p} \cdot batches_{p} \right) + \sum_{p=1}^{P} (setup\_time_{p} \cdot setup\_flag_{p}) \leq available_{m}, \quad \forall m \in \{1, \ldots, M\}
\]

2. Setup Flags:
\[
setup\_flag_{p} \in \{0, 1\}, \quad \forall p \in \{1, \ldots, P\}
\]

3. Non-negativity of batches:
\[
batches_{p} \geq 0, \quad \forall p \in \{1, \ldots, P\}
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

\section*{Mathematical Model for the Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required (in hours) on machine $m$ for part $p$ (for $m = 1, \ldots, M$ and $p = 1, \ldots, P$)
    \item $cost_{m}$: Cost per hour of using machine $m$ (for $m = 1, \ldots, M$)
    \item $available_{m}$: Availability of machine $m$ (in hours) per month (for $m = 1, \ldots, M$)
    \item $price_{p}$: Selling price per batch of part $p$ (for $p = 1, \ldots, P$)
    \item $setup\_time_{p}$: Setup time required (in hours) before machine 1 can be used for part $p$ (for $p = 1, \ldots, P$)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches produced for part $p$ (for $p = 1, \ldots, P$)
    \item $setup\_flag_{p}$: Binary variable indicating whether part $p$ is set up ($1$ if set up, $0$ otherwise)
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} \right) - \sum_{m=1}^{M} \left( cost_{m} \cdot \left( \sum_{p=1}^{P} \left( time_{m,p} \cdot batches_{p} \right) + \sum_{p=1}^{P} setup\_time_{p} \cdot setup\_flag_{p} \right) \right)
\]

\subsection*{Constraints}
1. Machine Time Availability:
\[
\sum_{p=1}^{P} \left( time_{m,p} \cdot batches_{p} \right) + \sum_{p=1}^{P} (setup\_time_{p} \cdot setup\_flag_{p}) \leq available_{m}, \quad \forall m \in \{1, \ldots, M\}
\]

2. Setup Flags:
\[
setup\_flag_{p} \in \{0, 1\}, \quad \forall p \in \{1, \ldots, P\}
\]

3. Non-negativity of batches:
\[
batches_{p} \geq 0, \quad \forall p \in \{1, \ldots, P\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


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
    'setup_time': [12, 8, 4, 0]
}

P = len(data['prices'])
M = len(data['machine_costs'])

#### Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

#### Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer_Problem", pulp.LpMaximize)

#### Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flag = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

#### Objective Function
total_revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
total_costs = pulp.lpSum(machine_costs[m] * (
    pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
    pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P))
) for m in range(M))
profit = total_revenue - total_costs
problem += profit

#### Constraints
#### Machine Time Availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + \
               pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P)) <= availability[m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

