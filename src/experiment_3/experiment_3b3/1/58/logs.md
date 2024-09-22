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

\section*{Mathematical Model for Auto Parts Manufacturer}

\subsection*{Sets}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): time required (in hours) on machine \( m \) to produce a batch of part \( p \).
    \item \( cost_{m} \): cost (in currency units) per hour for using machine \( m \).
    \item \( available_{m} \): availability (in hours) of machine \( m \) per month.
    \item \( price_{p} \): selling price (in currency units) of part \( p \) per batch.
    \item \( setup\_time_{p} \): setup time (in hours) required for machine 1 before producing part \( p \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( batches_{p} \): number of batches of part \( p \) produced (for \( p = 1, \ldots, P \)).
    \item \( setup\_flag_{p} \): binary variable indicating whether part \( p \) is set up (\( setup\_flag_{p} = 1 \)) or not (\( setup\_flag_{p} = 0 \)).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \text{hours\_used}_{m})
\]
where 
\[
\text{hours\_used}_{m} = \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) + \sum_{p=1}^{P} (setup\_time_{p} \cdot setup\_flag_{p}) \text{ for } m = 1
\]
and 
\[
\text{hours\_used}_{m} = \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \text{ for } m \neq 1
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) + \sum_{p=1}^{P} (setup\_time_{p} \cdot setup\_flag_{p}) \leq available_{m} \quad \forall m \in \{1, 2, \ldots, M\}
\]

2. Non-negativity constraints:
\[
batches_{p} \geq 0 \quad \forall p \in \{1, 2, \ldots, P\}
\]

3. Binary setup flag constraints:
\[
setup\_flag_{p} \in \{0, 1\} \quad \forall p \in \{1, 2, \ldots, P\}
\]

\subsection*{Output}
The output will include:
\begin{itemize}
    \item \( batches_{p} \): the number of batches of each part produced.
    \item \( setup\_flag_{p} \): indicates whether part \( p \) is set up.
    \item \( total\_profit \): representing the total profit obtained for the month.
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

\subsection*{Sets}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): time required (in hours) on machine \( m \) to produce a batch of part \( p \).
    \item \( cost_{m} \): cost (in currency units) per hour for using machine \( m \).
    \item \( available_{m} \): availability (in hours) of machine \( m \) per month.
    \item \( price_{p} \): selling price (in currency units) of part \( p \) per batch.
    \item \( setup\_time_{p} \): setup time (in hours) required for machine 1 before producing part \( p \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( batches_{p} \): number of batches of part \( p \) produced (for \( p = 1, \ldots, P \)).
    \item \( setup\_flag_{p} \): binary variable indicating whether part \( p \) is set up (\( setup\_flag_{p} = 1 \)) or not (\( setup\_flag_{p} = 0 \)).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \text{hours\_used}_{m})
\]
where 
\[
\text{hours\_used}_{m} = \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) + \sum_{p=1}^{P} (setup\_time_{p} \cdot setup\_flag_{p}) \text{ for } m = 1
\]
and 
\[
\text{hours\_used}_{m} = \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \text{ for } m \neq 1
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) + \sum_{p=1}^{P} (setup\_time_{p} \cdot setup\_flag_{p}) \leq available_{m} \quad \forall m \in \{1, 2, \ldots, M\}
\]

2. Non-negativity constraints:
\[
batches_{p} \geq 0 \quad \forall p \in \{1, 2, \ldots, P\}
\]

3. Binary setup flag constraints:
\[
setup\_flag_{p} \in \{0, 1\} \quad \forall p \in \{1, 2, \ldots, P\}
\]

\subsection*{Output}
The output will include:
\begin{itemize}
    \item \( batches_{p} \): the number of batches of each part produced.
    \item \( setup\_flag_{p} \): indicates whether part \( p \) is set up.
    \item \( total\_profit \): representing the total profit obtained for the month.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

#### Indices
P = len(data['prices'])
M = len(data['machine_costs'])

#### Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

#### Problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", (range(P)), lowBound=0, cat=pulp.LpContinuous)
setup_flag = pulp.LpVariable.dicts("setup_flag", (range(P)), cat=pulp.LpBinary)

#### Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost = pulp.lpSum(
    machine_costs[m] * (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
        (pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P)) if m == 0 else 0)
    ) for m in range(M))
problem += profit - cost

#### Constraints
#### Machine availability constraints
for m in range(M):
    if m == 0:
        machine_hours = pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + \
                        pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P))
    else:
        machine_hours = pulp.lpSum(time_required[m][p] * batches[p] for p in range(P))
    problem += machine_hours <= availability[m]

#### Solve
problem.solve()

#### Output results
print("Batches Produced:")
for p in range(P):
    print(f"Part {p+1}: {pulp.value(batches[p])} batches")

print("Setup Flags:")
for p in range(P):
    print(f"Part {p+1}: {'Set up' if pulp.value(setup_flag[p]) else 'Not set up'}")

print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

