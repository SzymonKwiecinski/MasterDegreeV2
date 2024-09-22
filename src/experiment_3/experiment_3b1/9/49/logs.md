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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\textbf{Sets:}
\begin{itemize}
    \item Let $P$ be the number of different parts.
    \item Let $M$ be the number of different machines.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce one batch of part $p$.
    \item $cost_m$: Cost (in currency units) per hour for using machine $m$.
    \item $available_m$: Availability (in hours) of machine $m$ per month.
    \item $price_p$: Selling price (in currency units) per batch of part $p$.
    \item $min\_batches_p$: Minimum number of batches of part $p$ that must be produced per month.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $batches_p$: Number of batches of part $p$ produced per month.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize} \quad & total\_profit = \sum_{p=1}^{P} (price_p \cdot batches_p) - \sum_{m=1}^{M} (cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_p))
\end{align*}

\textbf{Constraints:}
\begin{align*}
    \text{Machine Availability Constraints:} \quad & \sum_{p=1}^{P} (time_{m,p} \cdot batches_p) \leq available_m, \quad \forall m \in \{1, \ldots, M\} \\
    \text{Shared Availability for M and M-1:} \quad & \sum_{p=1}^{P} (time_{M,p} \cdot batches_p) + \sum_{p=1}^{P} (time_{M-1,p} \cdot batches_p) \leq available_M + available_{M-1} \\
    \text{Minimum Production Requirements:} \quad & batches_p \geq min\_batches_p, \quad \forall p \in \{1, \ldots, P\} \\
    \text{Non-negativity Constraints:} \quad & batches_p \geq 0, \quad \forall p \in \{1, \ldots, P\}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item The output should provide the number of batches produced for each part: $batches_p$ for $p = 1, \ldots, P$.
    \item The total profit should be calculated as $total\_profit$.
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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\textbf{Sets:}
\begin{itemize}
    \item Let $P$ be the number of different parts.
    \item Let $M$ be the number of different machines.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce one batch of part $p$.
    \item $cost_m$: Cost (in currency units) per hour for using machine $m$.
    \item $available_m$: Availability (in hours) of machine $m$ per month.
    \item $price_p$: Selling price (in currency units) per batch of part $p$.
    \item $min\_batches_p$: Minimum number of batches of part $p$ that must be produced per month.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $batches_p$: Number of batches of part $p$ produced per month.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize} \quad & total\_profit = \sum_{p=1}^{P} (price_p \cdot batches_p) - \sum_{m=1}^{M} (cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_p))
\end{align*}

\textbf{Constraints:}
\begin{align*}
    \text{Machine Availability Constraints:} \quad & \sum_{p=1}^{P} (time_{m,p} \cdot batches_p) \leq available_m, \quad \forall m \in \{1, \ldots, M\} \\
    \text{Shared Availability for M and M-1:} \quad & \sum_{p=1}^{P} (time_{M,p} \cdot batches_p) + \sum_{p=1}^{P} (time_{M-1,p} \cdot batches_p) \leq available_M + available_{M-1} \\
    \text{Minimum Production Requirements:} \quad & batches_p \geq min\_batches_p, \quad \forall p \in \{1, \ldots, P\} \\
    \text{Non-negativity Constraints:} \quad & batches_p \geq 0, \quad \forall p \in \{1, \ldots, P\}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item The output should provide the number of batches produced for each part: $batches_p$ for $p = 1, \ldots, P$.
    \item The total profit should be calculated as $total\_profit$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

#### Initialize model
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Sets
P = len(data['prices'])       #### Number of different parts
M = len(data['machine_costs']) #### Number of different machines

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective Function
total_profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - \
               pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += total_profit, "Total Profit"

#### Constraints - Machine Availability
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m], f"Machine_Availability_Constraint_{m}"

#### Shared Availability for M and M-1
problem += pulp.lpSum([data['time_required'][M-1][p] * batches[p] for p in range(P)]) + \
           pulp.lpSum([data['time_required'][M-2][p] * batches[p] for p in range(P)]) <= data['availability'][M-1] + data['availability'][M-2], "Shared_Availability_Constraint"

#### Minimum Production Requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Production_Requirement_{p}"

#### Solve the problem
problem.solve()

#### Output results
batches_produced = {f'Part_{p + 1}': batches[p].varValue for p in range(P)}
total_profit_value = pulp.value(problem.objective)
print(f'Batches produced: {batches_produced}')
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')
```

