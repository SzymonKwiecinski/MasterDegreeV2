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

\subsection*{Parameters}

\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( time_{m,p} \) be the time required (in hours) for machine \( m \) to produce 100 batches of part \( p \).
    \item Let \( cost_{m} \) be the cost (in dollars per hour) for using machine \( m \).
    \item Let \( available_{m} \) be the available hours per month for machine \( m \).
    \item Let \( price_{p} \) be the selling price (in dollars per batch of 100) for part \( p \).
    \item Let \( min\_batches_{p} \) be the minimum number of batches that must be produced for part \( p \).
\end{itemize}

\subsection*{Decision Variables}

Let \( batches_{p} \) be the number of batches produced for part \( p \).

\subsection*{Objective Function}

Maximize the total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} (price_{p} \times batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \times \sum_{p=1}^{P} (time_{m,p} \times \frac{batches_{p}}{100}) \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Machine availability constraint:
    \[
    \sum_{p=1}^{P} (time_{m,p} \times \frac{batches_{p}}{100}) \leq available_{m} \quad \forall m = 1, \ldots, M
    \]

    \item Minimum production requirement:
    \[
    batches_{p} \geq min\_batches_{p} \quad \forall p = 1, \ldots, P
    \]
    
    \item Non-negativity constraint:
    \[
    batches_{p} \geq 0 \quad \forall p = 1, \ldots, P
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

\subsection*{Parameters}

\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( time_{m,p} \) be the time required (in hours) for machine \( m \) to produce 100 batches of part \( p \).
    \item Let \( cost_{m} \) be the cost (in dollars per hour) for using machine \( m \).
    \item Let \( available_{m} \) be the available hours per month for machine \( m \).
    \item Let \( price_{p} \) be the selling price (in dollars per batch of 100) for part \( p \).
    \item Let \( min\_batches_{p} \) be the minimum number of batches that must be produced for part \( p \).
\end{itemize}

\subsection*{Decision Variables}

Let \( batches_{p} \) be the number of batches produced for part \( p \).

\subsection*{Objective Function}

Maximize the total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} (price_{p} \times batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \times \sum_{p=1}^{P} (time_{m,p} \times \frac{batches_{p}}{100}) \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Machine availability constraint:
    \[
    \sum_{p=1}^{P} (time_{m,p} \times \frac{batches_{p}}{100}) \leq available_{m} \quad \forall m = 1, \ldots, M
    \]

    \item Minimum production requirement:
    \[
    batches_{p} \geq min\_batches_{p} \quad \forall p = 1, \ldots, P
    \]
    
    \item Non-negativity constraint:
    \[
    batches_{p} \geq 0 \quad \forall p = 1, \ldots, P
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

#### Parameters
P = len(data['prices'])  #### number of different parts
M = len(data['machine_costs'])  #### number of different machines
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Problem Definition
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

#### Objective Function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * (batches[p] / 100) for p in range(P)) for m in range(M))

#### Constraints
#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * (batches[p] / 100) for p in range(P)) <= availability[m]

#### Minimum production requirement constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

