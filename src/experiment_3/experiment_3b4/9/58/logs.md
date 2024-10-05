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
To model this problem as a Mixed-Integer Programming (MIP), we need to consider both the decision variables for production quantities and setup flags. Below is the mathematical model formulated in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item $P$: Set of parts, indexed by $p = 1, 2, \ldots, P$.
    \item $M$: Set of machines, indexed by $m = 1, 2, \ldots, M$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $time_{m,p}$: Time required for machine $m$ to process a batch of part $p$ (in hours).
    \item $cost_{m}$: Operating cost per hour for machine $m$.
    \item $available_{m}$: Available hours for machine $m$ per month.
    \item $price_{p}$: Selling price per batch of part $p$.
    \item $setup\_time_{p}$: Setup time required on machine 1 for part $p$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches to produce for part $p$ (integer).
    \item $setup\_flag_{p}$: Binary variable indicating whether setup is performed for part $p$ on machine 1.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit, which is the difference between the sales revenue and the production cost:

\[
\text{Maximize} \quad \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) - \sum_{m=1}^{M} \sum_{p=1}^{P} \left( cost_{m} \times time_{m,p} \times batches_{p} \right) - \sum_{p=1}^{P} \left( cost_{1} \times setup\_time_{p} \times setup\_flag_{p} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine availability constraints for each machine $m$:
    \[
    \sum_{p=1}^{P} \left( time_{m,p} \times batches_{p} \right) + \delta_{m,1} \sum_{p=1}^{P} \left( setup\_time_{p} \times setup\_flag_{p} \right) \leq available_{m}, \quad \forall m \in M
    \]

    \item Setup flags constraint for machine 1 (only applicable to machine 1):
    \[
    batches_{p} \leq M \times setup\_flag_{p}, \quad \forall p \in P
    \]
    
    \item Non-negativity and integrality:
    \[
    batches_{p} \geq 0 \quad \text{and integer}, \quad \forall p \in P
    \]
    \[
    setup\_flag_{p} \in \{0,1\}, \quad \forall p \in P
    \]
\end{itemize}

\end{document}
```

This model maximizes profit by considering the revenue from selling parts and the costs associated with machine hours and setup times. The constraints ensure that machine availability is not exceeded and setup flags are correctly used. Here, $\delta_{m,1}$ is an indicator function that is 1 if $m=1$ (only applicable for setup time on machine 1) and 0 otherwise.

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item $P$: Set of parts, indexed by $p = 1, 2, \ldots, P$.
    \item $M$: Set of machines, indexed by $m = 1, 2, \ldots, M$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $time_{m,p}$: Time required for machine $m$ to process a batch of part $p$ (in hours).
    \item $cost_{m}$: Operating cost per hour for machine $m$.
    \item $available_{m}$: Available hours for machine $m$ per month.
    \item $price_{p}$: Selling price per batch of part $p$.
    \item $setup\_time_{p}$: Setup time required on machine 1 for part $p$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches to produce for part $p$ (integer).
    \item $setup\_flag_{p}$: Binary variable indicating whether setup is performed for part $p$ on machine 1.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit, which is the difference between the sales revenue and the production cost:

\[
\text{Maximize} \quad \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) - \sum_{m=1}^{M} \sum_{p=1}^{P} \left( cost_{m} \times time_{m,p} \times batches_{p} \right) - \sum_{p=1}^{P} \left( cost_{1} \times setup\_time_{p} \times setup\_flag_{p} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine availability constraints for each machine $m$:
    \[
    \sum_{p=1}^{P} \left( time_{m,p} \times batches_{p} \right) + \delta_{m,1} \sum_{p=1}^{P} \left( setup\_time_{p} \times setup\_flag_{p} \right) \leq available_{m}, \quad \forall m \in M
    \]

    \item Setup flags constraint for machine 1 (only applicable to machine 1):
    \[
    batches_{p} \leq M \times setup\_flag_{p}, \quad \forall p \in P
    \]
    
    \item Non-negativity and integrality:
    \[
    batches_{p} \geq 0 \quad \text{and integer}, \quad \forall p \in P
    \]
    \[
    setup\_flag_{p} \in \{0,1\}, \quad \forall p \in P
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

#### Unpacking data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

#### Sets
parts = range(len(prices))
machines = range(len(machine_costs))

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("Batches", parts, lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("SetupFlag", parts, cat='Binary')

#### Objective Function
profit = (
    pulp.lpSum(prices[p] * batches[p] for p in parts) -
    pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] for m in machines for p in parts) -
    pulp.lpSum(machine_costs[0] * setup_time[p] * setup_flag[p] for p in parts)
)
problem += profit

#### Constraints
#### Machine availability constraints
for m in machines:
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in parts) +
        (pulp.lpSum(setup_time[p] * setup_flag[p] for p in parts) if m == 0 else 0) <= availability[m]
    )

#### Setup flags constraint for machine 1
for p in parts:
    problem += batches[p] <= len(machines) * setup_flag[p]

#### Solve
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

