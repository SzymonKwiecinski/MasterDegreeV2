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

\section*{Mathematical Model for Auto Parts Production}

\textbf{Sets:}
\begin{itemize}
    \item $P$: Set of parts, indexed by $p = 1, \ldots, P$.
    \item $M$: Set of machines, indexed by $m = 1, \ldots, M$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce one batch of part $p$.
    \item $cost_{m}$: Cost (in currency per hour) of using machine $m$.
    \item $available_{m}$: Availability (in hours) of machine $m$ per month.
    \item $price_{p}$: Selling price (in currency) per batch of part $p$.
    \item $setup\_time_{p}$: Setup time (in hours) required on machine 1 for part $p$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $batches_{p}$: Number of batches produced for part $p$.
    \item $setup\_flag_{p}$: Binary variable indicating whether part $p$ is set up ($1$ if set up, $0$ otherwise).
    \item $total\_profit$: Total profit for the month.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } total\_profit = \sum_{p=1}^{P} price_{p} \cdot batches_{p} - \sum_{m=1}^{M} cost_{m} \cdot \left( \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} + \sum_{p=1}^{P} setup\_flag_{p} \cdot setup\_time_{p} \cdot \delta_{m,1} \right)
\]
where $\delta_{m,1}$ is the Kronecker delta function that equals 1 if $m=1$, and 0 otherwise.

\textbf{Constraints:}
\begin{align*}
\sum_{p=1}^{P} time_{m,p} \cdot batches_{p} + \sum_{p=1}^{P} setup\_flag_{p} \cdot setup\_time_{p} \cdot \delta_{m,1} & \leq available_{m}, & \forall m \in M \\
batches_{p} & \geq 0, & \forall p \in P \\
setup\_flag_{p} & \in \{0, 1\}, & \forall p \in P 
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item Number of batches produced for each part, $batches_{p}$.
    \item Setup flags for each part, $setup\_flag_{p}$.
    \item Total profit for the month, $total\_profit$.
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

\section*{Mathematical Model for Auto Parts Production}

\textbf{Sets:}
\begin{itemize}
    \item $P$: Set of parts, indexed by $p = 1, \ldots, P$.
    \item $M$: Set of machines, indexed by $m = 1, \ldots, M$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce one batch of part $p$.
    \item $cost_{m}$: Cost (in currency per hour) of using machine $m$.
    \item $available_{m}$: Availability (in hours) of machine $m$ per month.
    \item $price_{p}$: Selling price (in currency) per batch of part $p$.
    \item $setup\_time_{p}$: Setup time (in hours) required on machine 1 for part $p$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $batches_{p}$: Number of batches produced for part $p$.
    \item $setup\_flag_{p}$: Binary variable indicating whether part $p$ is set up ($1$ if set up, $0$ otherwise).
    \item $total\_profit$: Total profit for the month.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } total\_profit = \sum_{p=1}^{P} price_{p} \cdot batches_{p} - \sum_{m=1}^{M} cost_{m} \cdot \left( \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} + \sum_{p=1}^{P} setup\_flag_{p} \cdot setup\_time_{p} \cdot \delta_{m,1} \right)
\]
where $\delta_{m,1}$ is the Kronecker delta function that equals 1 if $m=1$, and 0 otherwise.

\textbf{Constraints:}
\begin{align*}
\sum_{p=1}^{P} time_{m,p} \cdot batches_{p} + \sum_{p=1}^{P} setup\_flag_{p} \cdot setup\_time_{p} \cdot \delta_{m,1} & \leq available_{m}, & \forall m \in M \\
batches_{p} & \geq 0, & \forall p \in P \\
setup\_flag_{p} & \in \{0, 1\}, & \forall p \in P 
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item Number of batches produced for each part, $batches_{p}$.
    \item Setup flags for each part, $setup\_flag_{p}$.
    \item Total profit for the month, $total\_profit$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
setup_time = [12, 8, 4, 0]

P = range(len(prices))  #### Number of parts
M = range(len(machine_costs))  #### Number of machines

#### Problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

#### Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in P]
setup_flag = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in P]

#### Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in P)
cost = pulp.lpSum(
    machine_costs[m] * (sum(time_required[m][p] * batches[p] for p in P) +
                        sum(setup_flag[p] * setup_time[p] for p in P if m == 0))
    for m in M
)
problem += profit - cost

#### Constraints
for m in M:
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in P) + \
               pulp.lpSum(setup_flag[p] * setup_time[p] for p in P if m == 0) <= availability[m]

#### Solve
problem.solve()

#### Output
for p in P:
    print(f'Batches produced for part {p+1}: {batches[p].varValue}')
    print(f'Setup flag for part {p+1}: {setup_flag[p].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

