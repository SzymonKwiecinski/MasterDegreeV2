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

\section*{Linear Programming Formulation}

Let \( P \) be the number of different parts and \( M \) be the number of different machines. Define the following variables:

\begin{itemize}
    \item \( batches_{p} \): number of batches of part \( p \) produced (for \( p = 1, \ldots, P \)).
    \item \( extra\_time_{m} \): additional hours purchased for machine \( m \) (for \( m = 1, \ldots, M \)).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} - \sum_{m=1}^{M} (cost_{m} \cdot \left( \frac{time_{m,p}}{100} \cdot batches_{p} \right) + extra\_costs_{m} \cdot extra\_time_{m}) \right)
\]

\subsection*{Constraints}
1. **Machine Time Availability**:

\[
\sum_{p=1}^{P} \left( time_{m,p} \cdot batches_{p} \right) \leq available_{m} + extra\_time_{m}, \quad \forall m = 1, \ldots, M
\]

2. **Minimum Batch Production**:

\[
batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P
\]

3. **Maximum Extra Time**:

\[
extra\_time_{m} \leq max\_extra_{m}, \quad \forall m = 1, \ldots, M
\]

4. **Non-negativity**:

\[
batches_{p} \geq 0 \quad \text{and} \quad extra\_time_{m} \geq 0, \quad \forall p = 1, \ldots, P, \forall m = 1, \ldots, M
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item \( batches \): List of \( batches_{p} \) for \( p = 1, \ldots, P \).
    \item \( extra\_time \): List of \( extra\_time_{m} \) for \( m = 1, \ldots, M \).
    \item \( total\_profit \): Total profit obtained for the month.
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

\section*{Linear Programming Formulation}

Let \( P \) be the number of different parts and \( M \) be the number of different machines. Define the following variables:

\begin{itemize}
    \item \( batches_{p} \): number of batches of part \( p \) produced (for \( p = 1, \ldots, P \)).
    \item \( extra\_time_{m} \): additional hours purchased for machine \( m \) (for \( m = 1, \ldots, M \)).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} - \sum_{m=1}^{M} (cost_{m} \cdot \left( \frac{time_{m,p}}{100} \cdot batches_{p} \right) + extra\_costs_{m} \cdot extra\_time_{m}) \right)
\]

\subsection*{Constraints}
1. **Machine Time Availability**:

\[
\sum_{p=1}^{P} \left( time_{m,p} \cdot batches_{p} \right) \leq available_{m} + extra\_time_{m}, \quad \forall m = 1, \ldots, M
\]

2. **Minimum Batch Production**:

\[
batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P
\]

3. **Maximum Extra Time**:

\[
extra\_time_{m} \leq max\_extra_{m}, \quad \forall m = 1, \ldots, M
\]

4. **Non-negativity**:

\[
batches_{p} \geq 0 \quad \text{and} \quad extra\_time_{m} \geq 0, \quad \forall p = 1, \ldots, P, \forall m = 1, \ldots, M
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item \( batches \): List of \( batches_{p} \) for \( p = 1, \ldots, P \).
    \item \( extra\_time \): List of \( extra\_time_{m} \) for \( m = 1, \ldots, M \).
    \item \( total\_profit \): Total profit obtained for the month.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


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
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

#### Parameters
P = len(data['prices'])  #### number of parts
M = len(data['availability'])  #### number of machines

#### Create a problem instance
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

#### Objective Function
profit_terms = [
    data['prices'][p] * batches[p]
    - sum(data['machine_costs'][m] * (data['time_required'][m][p] / 100) * batches[p] for m in range(M))
    - sum(data['extra_costs'][m] * extra_time[m] for m in range(M)) for p in range(P)
]

problem += pulp.lpSum(profit_terms)

#### Constraints

#### Machine Time Availability Constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P))
        <= data['availability'][m] + extra_time[m], f"Machine_Time_Constraint_{m}"
    )

#### Minimum Batch Production Constraints
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}")

#### Maximum Extra Time Constraints
for m in range(M):
    problem += (extra_time[m] <= data['max_extra'][m], f"Max_Extra_Time_Constraint_{m}")

#### Solve the problem
problem.solve()

#### Printing results
print("Batches produced for each part:")
for p in range(P):
    print(f" - Part {p + 1}: {batches[p].varValue}")

print("Extra time purchased for each machine:")
for m in range(M):
    print(f" - Machine {m + 1}: {extra_time[m].varValue}")

print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

