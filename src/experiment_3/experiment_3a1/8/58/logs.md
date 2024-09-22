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

\textbf{Parameters:}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required on machine $m$ to produce one batch of part $p$ (in hours)
    \item $cost_{m}$: Cost per hour for using machine $m$
    \item $available_{m}$: Availability of machine $m$ (in hours per month)
    \item $price_{p}$: Selling price per batch of part $p$
    \item $setup\_time_{p}$: Setup time required for part $p$ on machine 1 (in hours)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $batches_{p}$: Number of batches produced for part $p$
    \item $setup\_flag_{p} \in \{0, 1\}$: Indicates whether part $p$ is set up (1) or not (0)
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize } \quad & total\_profit = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \text{hours\_used}_{m}) \\
    \text{where } & hours\_used_{m} = \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p} \cdot setup\_flag_{p}) + \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \text{ (for $m=1$ only)} 
\end{align*}

\textbf{Constraints:}
\begin{align*}
    \text{1. Machine Availability:} \quad & \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m \in \{1, 2, \ldots, M\} \\
    \text{2. Setup Time for Machine 1:} \quad & setup\_flag_{p} \cdot setup\_time_{p} + \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) \leq available_{1} \\
    \text{3. Non-negativity:} \quad & batches_{p} \geq 0, \quad \forall p \in \{1, 2, \ldots, P\} \\
    \text{4. Setup Flag Binary:} \quad & setup\_flag_{p} \in \{0, 1\}, \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $batches$: The number of batches of each part produced
    \item $setup\_flags$: Indicates whether part $p$ is set up or not
    \item $total\_profit$: The total profit obtained for the month
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

\textbf{Parameters:}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required on machine $m$ to produce one batch of part $p$ (in hours)
    \item $cost_{m}$: Cost per hour for using machine $m$
    \item $available_{m}$: Availability of machine $m$ (in hours per month)
    \item $price_{p}$: Selling price per batch of part $p$
    \item $setup\_time_{p}$: Setup time required for part $p$ on machine 1 (in hours)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $batches_{p}$: Number of batches produced for part $p$
    \item $setup\_flag_{p} \in \{0, 1\}$: Indicates whether part $p$ is set up (1) or not (0)
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize } \quad & total\_profit = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \text{hours\_used}_{m}) \\
    \text{where } & hours\_used_{m} = \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p} \cdot setup\_flag_{p}) + \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \text{ (for $m=1$ only)} 
\end{align*}

\textbf{Constraints:}
\begin{align*}
    \text{1. Machine Availability:} \quad & \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m \in \{1, 2, \ldots, M\} \\
    \text{2. Setup Time for Machine 1:} \quad & setup\_flag_{p} \cdot setup\_time_{p} + \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) \leq available_{1} \\
    \text{3. Non-negativity:} \quad & batches_{p} \geq 0, \quad \forall p \in \{1, 2, \ldots, P\} \\
    \text{4. Setup Flag Binary:} \quad & setup\_flag_{p} \in \{0, 1\}, \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $batches$: The number of batches of each part produced
    \item $setup\_flags$: Indicates whether part $p$ is set up or not
    \item $total\_profit$: The total profit obtained for the month
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}")

#### Parameters
P = len(data['setup_time'])
M = len(data['time_required'])

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

#### Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - pulp.lpSum([machine_costs[m] * (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + (setup_flags[p] * setup_time[p] if m == 0 else 0)) for m in range(M)])
problem += profit

#### Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Constraint_m{m}"

problem += setup_flags[0] * setup_time[0] + pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) <= availability[0], "Setup_Time_Constraint_m1"

#### Solve the problem
problem.solve()

#### Output results
batches_result = {f'batches_{p}': batches[p].varValue for p in range(P)}
setup_flags_result = {f'setup_flag_{p}': setup_flags[p].varValue for p in range(P)}
total_profit = pulp.value(problem.objective)

print(batches_result)
print(setup_flags_result)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

