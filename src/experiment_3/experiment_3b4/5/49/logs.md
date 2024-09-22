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

\section*{Mathematical Model for the Problem}

\subsection*{Decision Variables}
Let $x_p$ be the number of batches of part $p$ produced each month, for $p = 1, 2, \ldots, P$.

\subsection*{Objective Function}
The objective is to maximize the total profit, which is the difference between the total revenue and the total cost of machine usage. The total revenue is given by the sum of the revenue from each part, and the total cost is the sum of the costs of using each machine. The objective function can be expressed as:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (\text{price}_{p} \cdot x_p) - \sum_{m=1}^{M} (\text{cost}_{m} \cdot \sum_{p=1}^{P} (\text{time}_{m,p} \cdot x_p))
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Machine Availability Constraints:} For machines $1$ to $M-2$, the machine cannot be used beyond its availability.

    \[
    \sum_{p=1}^{P} (\text{time}_{m,p} \cdot x_p) \leq \text{available}_{m}, \quad \text{for } m = 1, 2, \ldots, M-2
    \]

    For machines $M-1$ and $M$, they share their availability jointly, thus:

    \[
    \sum_{p=1}^{P} (\text{time}_{M-1,p} \cdot x_p) + \sum_{p=1}^{P} (\text{time}_{M,p} \cdot x_p) \leq \text{available}_{M-1} + \text{available}_{M}
    \]

    \item \textbf{Minimum Production Requirement:} The number of batches produced for each part must meet the minimum required batches due to contractual obligations.

    \[
    x_p \geq \text{min_batches}_{p}, \quad \text{for } p = 1, 2, \ldots, P
    \]

    \item \textbf{Non-negativity Constraints:} The number of batches produced cannot be negative.

    \[
    x_p \geq 0, \quad \text{for } p = 1, 2, \ldots, P
    \]

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

\section*{Mathematical Model for the Problem}

\subsection*{Decision Variables}
Let $x_p$ be the number of batches of part $p$ produced each month, for $p = 1, 2, \ldots, P$.

\subsection*{Objective Function}
The objective is to maximize the total profit, which is the difference between the total revenue and the total cost of machine usage. The total revenue is given by the sum of the revenue from each part, and the total cost is the sum of the costs of using each machine. The objective function can be expressed as:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (\text{price}_{p} \cdot x_p) - \sum_{m=1}^{M} (\text{cost}_{m} \cdot \sum_{p=1}^{P} (\text{time}_{m,p} \cdot x_p))
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Machine Availability Constraints:} For machines $1$ to $M-2$, the machine cannot be used beyond its availability.

    \[
    \sum_{p=1}^{P} (\text{time}_{m,p} \cdot x_p) \leq \text{available}_{m}, \quad \text{for } m = 1, 2, \ldots, M-2
    \]

    For machines $M-1$ and $M$, they share their availability jointly, thus:

    \[
    \sum_{p=1}^{P} (\text{time}_{M-1,p} \cdot x_p) + \sum_{p=1}^{P} (\text{time}_{M,p} \cdot x_p) \leq \text{available}_{M-1} + \text{available}_{M}
    \]

    \item \textbf{Minimum Production Requirement:} The number of batches produced for each part must meet the minimum required batches due to contractual obligations.

    \[
    x_p \geq \text{min_batches}_{p}, \quad \text{for } p = 1, 2, \ldots, P
    \]

    \item \textbf{Non-negativity Constraints:} The number of batches produced cannot be negative.

    \[
    x_p \geq 0, \quad \text{for } p = 1, 2, \ldots, P
    \]

\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


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
    'min_batches': [10, 10, 10, 10]
}

P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function
revenue = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
costs = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M))
profit = revenue - costs
problem += profit

#### Constraints

#### Machine Availability Constraints
for m in range(M-2):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

#### Shared Availability for Machines M-1 and M
problem += (
    pulp.lpSum(data['time_required'][M-2][p] * x[p] for p in range(P)) +
    pulp.lpSum(data['time_required'][M-1][p] * x[p] for p in range(P))
    <= data['availability'][M-2] + data['availability'][M-1]
)

#### Minimum Production Requirement
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

#### Solve the problem
problem.solve()

#### Print the results
for p in range(P):
    print(f"Batches of part {p+1} produced: {x[p].varValue}")
    
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

