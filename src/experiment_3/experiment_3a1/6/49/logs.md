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

\subsection*{Decision Variables}
Let \(batches_{p}\) be the number of batches of part \(p\) produced for \(p = 1, \ldots, P\).

\subsection*{Parameters}
\begin{itemize}
    \item \(time_{m,p}\): Time required on machine \(m\) to produce one batch of part \(p\) (in hours).
    \item \(cost_{m}\): Cost per hour for using machine \(m\).
    \item \(available_{m}\): Availability of machine \(m\) (in hours per month).
    \item \(price_{p}\): Selling price per batch of part \(p\).
    \item \(min\_batches_{p}\): Minimum batches of part \(p\) that must be produced to fulfill contracts.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \right)
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{m=1}^{M} \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq \sum_{m=1}^{M} available_{m}
\]

2. Minimum production requirements:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:
\[
batches_{p} \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Output}
The output consists of:
\begin{itemize}
    \item The number of batches produced for each part: \(batches = [batches_{1}, batches_{2}, \ldots, batches_{P}]\)
    \item The total profit obtained for the month: \(total\_profit = Z\)
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
Let \(batches_{p}\) be the number of batches of part \(p\) produced for \(p = 1, \ldots, P\).

\subsection*{Parameters}
\begin{itemize}
    \item \(time_{m,p}\): Time required on machine \(m\) to produce one batch of part \(p\) (in hours).
    \item \(cost_{m}\): Cost per hour for using machine \(m\).
    \item \(available_{m}\): Availability of machine \(m\) (in hours per month).
    \item \(price_{p}\): Selling price per batch of part \(p\).
    \item \(min\_batches_{p}\): Minimum batches of part \(p\) that must be produced to fulfill contracts.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \right)
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{m=1}^{M} \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq \sum_{m=1}^{M} available_{m}
\]

2. Minimum production requirements:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:
\[
batches_{p} \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Output}
The output consists of:
\begin{itemize}
    \item The number of batches produced for each part: \(batches = [batches_{1}, batches_{2}, \ldots, batches_{P}]\)
    \item The total profit obtained for the month: \(total\_profit = Z\)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in the JSON format
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10]
}'''
data = json.loads(data_json)

#### Parameters
time_required = data['time_required']  #### Time required on each machine for each part
machine_costs = data['machine_costs']  #### Cost of using each machine per hour
availability = data['availability']  #### Available hours for each machine
prices = data['prices']  #### Selling price per batch of each part
min_batches = data['min_batches']  #### Minimum batches to produce for each part

#### Number of machines and parts
num_machines = len(machine_costs)
num_parts = len(prices)

#### Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Continuous')

#### Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) for m in range(num_machines))

problem += profit, "Total_Profit"

#### Constraints
#### Machine availability constraints
for m in range(num_machines):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m], 
                   f"Machine_Availability_Constraint_{m}")

#### Minimum production requirements
for p in range(num_parts):
    problem += (batches[p] >= min_batches[p], f"Min_Production_Requirement_{p}")

#### Solve the problem
problem.solve()

#### Output results
batches_produced = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced for each part: {batches_produced}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

