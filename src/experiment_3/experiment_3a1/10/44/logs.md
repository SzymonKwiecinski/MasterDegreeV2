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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Auto Parts Manufacturer}

Let:
\begin{itemize}
    \item \( P \) be the number of different parts.
    \item \( M \) be the number of different machines.
    \item \( time_{m,p} \) be the time required in hours on machine \( m \) to produce a batch of part \( p \).
    \item \( cost_{m} \) be the charge per hour for using machine \( m \).
    \item \( available_{m} \) be the availability of machine \( m \) in hours per month.
    \item \( price_{p} \) be the selling price for a batch of part \( p \).
    \item \( min\_batches_{p} \) be the minimum number of batches of part \( p \) that must be produced each month.
    \item \( batches_{p} \) be the number of batches of part \( p \) produced.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \text{time used by machine } m)
\]

Where the time used by machine \( m \) is given by:
\[
\text{time used by machine } m = \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m \in \{1, 2, \ldots, M\}
\]

2. Minimum production constraints:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, 2, \ldots, P\}
\]

3. Non-negativity constraints:
\[
batches_{p} \geq 0, \quad \forall p \in \{1, 2, \ldots, P\}
\]

\subsection*{Output Format}
The output will be:
\begin{itemize}
    \item \( batches \): the number of batches of each part produced \([batches_{p} \text{ for } p = 1, \ldots, P]\).
    \item \( total\_profit \): the total profit obtained for the month.
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

\section*{Mathematical Model for Auto Parts Manufacturer}

Let:
\begin{itemize}
    \item \( P \) be the number of different parts.
    \item \( M \) be the number of different machines.
    \item \( time_{m,p} \) be the time required in hours on machine \( m \) to produce a batch of part \( p \).
    \item \( cost_{m} \) be the charge per hour for using machine \( m \).
    \item \( available_{m} \) be the availability of machine \( m \) in hours per month.
    \item \( price_{p} \) be the selling price for a batch of part \( p \).
    \item \( min\_batches_{p} \) be the minimum number of batches of part \( p \) that must be produced each month.
    \item \( batches_{p} \) be the number of batches of part \( p \) produced.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \text{time used by machine } m)
\]

Where the time used by machine \( m \) is given by:
\[
\text{time used by machine } m = \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m \in \{1, 2, \ldots, M\}
\]

2. Minimum production constraints:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, 2, \ldots, P\}
\]

3. Non-negativity constraints:
\[
batches_{p} \geq 0, \quad \forall p \in \{1, 2, \ldots, P\}
\]

\subsection*{Output Format}
The output will be:
\begin{itemize}
    \item \( batches \): the number of batches of each part produced \([batches_{p} \text{ for } p = 1, \ldots, P]\).
    \item \( total\_profit \): the total profit obtained for the month.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

#### Number of parts and machines
P = len(data['prices'])  #### Number of different parts
M = len(data['machine_costs'])  #### Number of different machines

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

#### Objective function: Maximize total profit
total_profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - \
               pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += total_profit

#### Constraints: Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]

#### Constraints: Minimum production constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

#### Solve the problem
problem.solve()

#### Output the results
batches_result = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

print(f' (Batches Produced): {batches_result}')
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')
```

