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

\section*{Linear Programming Model for Auto Parts Production}

\subsection*{Variables}
\begin{itemize}
    \item Let \( b_p \) = Number of batches produced for part \( p \) (for \( p = 1, \ldots, P \))
    \item Let \( extra_m \) = Additional hours purchased for machine \( m \) (for \( m = 1, \ldots, M \))
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \) = Time required on machine \( m \) to produce a batch of part \( p \)
    \item \( cost_m \) = Cost per hour for using machine \( m \)
    \item \( available_m \) = Available hours per month for machine \( m \)
    \item \( price_p \) = Selling price per batch of part \( p \)
    \item \( min\_batches_p \) = Minimum batches required for part \( p \) to fulfill contract
    \item \( extra\_cost_m \) = Cost per hour for extra time on machine \( m \)
    \item \( max\_extra_m \) = Maximum extra hours that can be purchased for machine \( m \)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} \left( (cost_m \cdot \sum_{p=1}^{P} time_{m,p} \cdot b_p) + extra\_cost_m \cdot extra_m \right)
\]

\subsection*{Constraints}
1. Machine availability:
\[
\sum_{p=1}^{P} time_{m,p} \cdot b_p + extra_m \leq available_m + max\_extra_m \quad \text{for } m = 1, \ldots, M
\]

2. Minimum production requirements:
\[
b_p \geq min\_batches_p \quad \text{for } p = 1, \ldots, P
\]

3. Extra time constraints:
\[
0 \leq extra_m \leq max\_extra_m \quad \text{for } m = 1, \ldots, M
\]

4. Non-negativity constraints:
\[
b_p \geq 0 \quad \text{for } p = 1, \ldots, P
\]
\[
extra_m \geq 0 \quad \text{for } m = 1, \ldots, M
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

\section*{Linear Programming Model for Auto Parts Production}

\subsection*{Variables}
\begin{itemize}
    \item Let \( b_p \) = Number of batches produced for part \( p \) (for \( p = 1, \ldots, P \))
    \item Let \( extra_m \) = Additional hours purchased for machine \( m \) (for \( m = 1, \ldots, M \))
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \) = Time required on machine \( m \) to produce a batch of part \( p \)
    \item \( cost_m \) = Cost per hour for using machine \( m \)
    \item \( available_m \) = Available hours per month for machine \( m \)
    \item \( price_p \) = Selling price per batch of part \( p \)
    \item \( min\_batches_p \) = Minimum batches required for part \( p \) to fulfill contract
    \item \( extra\_cost_m \) = Cost per hour for extra time on machine \( m \)
    \item \( max\_extra_m \) = Maximum extra hours that can be purchased for machine \( m \)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} \left( (cost_m \cdot \sum_{p=1}^{P} time_{m,p} \cdot b_p) + extra\_cost_m \cdot extra_m \right)
\]

\subsection*{Constraints}
1. Machine availability:
\[
\sum_{p=1}^{P} time_{m,p} \cdot b_p + extra_m \leq available_m + max\_extra_m \quad \text{for } m = 1, \ldots, M
\]

2. Minimum production requirements:
\[
b_p \geq min\_batches_p \quad \text{for } p = 1, \ldots, P
\]

3. Extra time constraints:
\[
0 \leq extra_m \leq max\_extra_m \quad \text{for } m = 1, \ldots, M
\]

4. Non-negativity constraints:
\[
b_p \geq 0 \quad \text{for } p = 1, \ldots, P
\]
\[
extra_m \geq 0 \quad \text{for } m = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10], 
    "extra_costs": [0, 15, 22.5], 
    "max_extra": [0, 80, 80]
}'''

#### Load data
data = json.loads(data_json)

#### Define sets
P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  #### batches for parts
extra = pulp.LpVariable.dicts("extra", range(M), lowBound=0)  #### extra hours for machines

#### Objective function
profit = pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) \
         - pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(M)) \
         - pulp.lpSum(data['extra_costs'][m] * extra[m] for m in range(M))

problem += profit, "Total_Profit"

#### Constraints
#### Machine availability
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) + extra[m] <= data['availability'][m] + data['max_extra'][m]), f"Availability_Constraint_{m}"

#### Minimum production requirements
for p in range(P):
    problem += (b[p] >= data['min_batches'][p]), f"Min_Production_Constraint_{p}"

#### Extra time constraints
for m in range(M):
    problem += (extra[m] >= 0, f"Extra_Nonnegativity_Constraint_{m}")
    problem += (extra[m] <= data['max_extra'][m], f"Max_Extra_Constraint_{m}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

