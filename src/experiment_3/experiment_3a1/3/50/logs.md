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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Decision Variables}
Let 
\begin{align*}
batches_{p} & : \text{ number of batches produced for part } p \text{ for } p = 1, \ldots, P \\
extra_{m} & : \text{ extra time purchased for machine } m \text{ for } m = 1, \ldots, M
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left(c_{m} \cdot (available_{m} + extra_{m})\right)
\]

\subsection*{Constraints}
1. Time constraints for each machine:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m} + extra_{m}, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P
\]

3. Extra time purchase limits:
\[
0 \leq extra_{m} \leq max\_extra_{m}, \quad \forall m = 1, \ldots, M
\]

4. Non-negativity constraints:
\[
batches_{p} \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Summary of Parameters}
\begin{itemize}
    \item $time_{m,p}$: hours required on machine $m$ to produce a batch of part $p$
    \item $cost_{m}$: charge per hour for using machine $m$
    \item $available_{m}$: availability of machine $m$ in hours per month
    \item $price_{p}$: selling price per batch of part $p$
    \item $min\_batches_{p}$: minimum required batches of part $p$ to fulfill contracts
    \item $extra\_cost_{m}$: cost per hour of extra time for machine $m$
    \item $max\_extra_{m}$: maximum extra hours that can be purchased for machine $m$
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

\subsection*{Decision Variables}
Let 
\begin{align*}
batches_{p} & : \text{ number of batches produced for part } p \text{ for } p = 1, \ldots, P \\
extra_{m} & : \text{ extra time purchased for machine } m \text{ for } m = 1, \ldots, M
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left(c_{m} \cdot (available_{m} + extra_{m})\right)
\]

\subsection*{Constraints}
1. Time constraints for each machine:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m} + extra_{m}, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P
\]

3. Extra time purchase limits:
\[
0 \leq extra_{m} \leq max\_extra_{m}, \quad \forall m = 1, \ldots, M
\]

4. Non-negativity constraints:
\[
batches_{p} \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Summary of Parameters}
\begin{itemize}
    \item $time_{m,p}$: hours required on machine $m$ to produce a batch of part $p$
    \item $cost_{m}$: charge per hour for using machine $m$
    \item $available_{m}$: availability of machine $m$ in hours per month
    \item $price_{p}$: selling price per batch of part $p$
    \item $min\_batches_{p}$: minimum required batches of part $p$ to fulfill contracts
    \item $extra\_cost_{m}$: cost per hour of extra time for machine $m$
    \item $max\_extra_{m}$: maximum extra hours that can be purchased for machine $m$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data in JSON format
data = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10],
    "extra_costs": [0, 15, 22.5],
    "max_extra": [0, 80, 80]
}'''

#### Load the data
params = json.loads(data)

#### Set up the problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

#### Decision Variables
P = len(params['prices'])  #### Number of parts
M = len(params['machine_costs'])  #### Number of machines

batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra = pulp.LpVariable.dicts("extra", range(M), lowBound=0)

#### Objective Function
profit = pulp.lpSum(params['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(params['extra_costs'][m] * extra[m] for m in range(M))
problem += profit, "Total_Profit"

#### Constraints

#### Time constraints for each machine
for m in range(M):
    problem += (pulp.lpSum(params['time_required'][m][p] * batches[p] for p in range(P)) <=
                 params['availability'][m] + extra[m]), f"Time_Constraint_{m}"

#### Minimum production requirements
for p in range(P):
    problem += (batches[p] >= params['min_batches'][p]), f"Min_Production_{p}"

#### Extra time purchase limits
for m in range(M):
    problem += (extra[m] <= params['max_extra'][m]), f"Max_Extra_{m}"

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

