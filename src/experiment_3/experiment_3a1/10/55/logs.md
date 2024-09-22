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
- Machine \var{1} is being outsourced so that the manufacturer must pay for the labor.
- The labor costs $\var{standard_cost}/h up to \var{overtime_hour} hours, after which it costs $\var{overtime_cost}/h due to overtime.
- Individual availability conditions for Machine \var{1} can be disregarded.
- The desired profit should surpass \var{min_profit}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour,
    "min_profit": min_profit
}

OBJECTIVE: Determine the quantity of batches for each part the manufacturer should produce every month, ensuring all constraints are met.

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

\textbf{Problem Definition:}

Let:
\begin{itemize}
    \item $P$ = Number of different parts
    \item $M$ = Number of different machines
    \item $batches_p$ = Number of batches produced for part $p$ (for $p = 1, \ldots, P$)
    \item $time_{m,p}$ = Time required on machine $m$ for part $p$ (in hours)
    \item $cost_m$ = Hourly cost of machine $m$
    \item $available_m$ = Available hours of machine $m$ per month
    \item $price_p$ = Selling price of part $p$ (per batch)
    \item $min\_batches_p$ = Minimum batches required for part $p$
    \item $standard\_cost$ = Standard labor cost (per hour)
    \item $overtime\_cost$ = Overtime labor cost (per hour)
    \item $overtime\_hour$ = Maximum hours before overtime kicks in
    \item $min\_profit$ = Minimum desired profit
\end{itemize}

\textbf{Objective Function:}

Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot batches_p) - \sum_{m=1}^{M} (cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_p))
\]

\textbf{Subject to:}

1. Machine time utilization constraints:

\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_p) \leq available_m \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements:

\[
batches_p \geq min\_batches_p \quad \forall p = 1, \ldots, P
\]

3. Labor cost constraints (for Machine 1):

\[
\text{Total hours used on Machine 1} = \sum_{p=1}^{P} (time_{1,p} \cdot batches_p)
\]
\[
\text{If } \sum_{p=1}^{P} (time_{1,p} \cdot batches_p) \leq overtime\_hour \Rightarrow \text{Cost} = standard\_cost \cdot \sum_{p=1}^{P} (time_{1,p} \cdot batches_p)
\]
\[
\text{If } \sum_{p=1}^{P} (time_{1,p} \cdot batches_p) > overtime\_hour \Rightarrow \text{Cost} = standard\_cost \cdot overtime\_hour + overtime\_cost \cdot \left( \sum_{p=1}^{P} (time_{1,p} \cdot batches_p) - overtime\_hour \right)
\]

4. Profit constraint:

\[
Z \geq min\_profit
\]

\textbf{Variables:}

\begin{itemize}
    \item $batches_p \geq 0$ (for $p = 1, \ldots, P$)
\end{itemize}

\textbf{Output:}

\begin{itemize}
    \item $batches = [batches_p \text{ for } p = 1, \ldots, P]$
    \item $total\_profit = Z$
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

\textbf{Problem Definition:}

Let:
\begin{itemize}
    \item $P$ = Number of different parts
    \item $M$ = Number of different machines
    \item $batches_p$ = Number of batches produced for part $p$ (for $p = 1, \ldots, P$)
    \item $time_{m,p}$ = Time required on machine $m$ for part $p$ (in hours)
    \item $cost_m$ = Hourly cost of machine $m$
    \item $available_m$ = Available hours of machine $m$ per month
    \item $price_p$ = Selling price of part $p$ (per batch)
    \item $min\_batches_p$ = Minimum batches required for part $p$
    \item $standard\_cost$ = Standard labor cost (per hour)
    \item $overtime\_cost$ = Overtime labor cost (per hour)
    \item $overtime\_hour$ = Maximum hours before overtime kicks in
    \item $min\_profit$ = Minimum desired profit
\end{itemize}

\textbf{Objective Function:}

Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot batches_p) - \sum_{m=1}^{M} (cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_p))
\]

\textbf{Subject to:}

1. Machine time utilization constraints:

\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_p) \leq available_m \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements:

\[
batches_p \geq min\_batches_p \quad \forall p = 1, \ldots, P
\]

3. Labor cost constraints (for Machine 1):

\[
\text{Total hours used on Machine 1} = \sum_{p=1}^{P} (time_{1,p} \cdot batches_p)
\]
\[
\text{If } \sum_{p=1}^{P} (time_{1,p} \cdot batches_p) \leq overtime\_hour \Rightarrow \text{Cost} = standard\_cost \cdot \sum_{p=1}^{P} (time_{1,p} \cdot batches_p)
\]
\[
\text{If } \sum_{p=1}^{P} (time_{1,p} \cdot batches_p) > overtime\_hour \Rightarrow \text{Cost} = standard\_cost \cdot overtime\_hour + overtime\_cost \cdot \left( \sum_{p=1}^{P} (time_{1,p} \cdot batches_p) - overtime\_hour \right)
\]

4. Profit constraint:

\[
Z \geq min\_profit
\]

\textbf{Variables:}

\begin{itemize}
    \item $batches_p \geq 0$ (for $p = 1, \ldots, P$)
\end{itemize}

\textbf{Output:}

\begin{itemize}
    \item $batches = [batches_p \text{ for } p = 1, \ldots, P]$
    \item $total\_profit = Z$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


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
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

#### Problem setup
P = len(data['min_batches'])  #### Number of different parts
M = len(data['availability'])  #### Number of different machines

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * 
                     pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) 
                     for m in range(M))

problem += profit

#### Constraints
#### Machine time utilization constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m])

#### Minimum production requirements
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p])

#### Labor cost constraints for Machine 1
total_hours_m1 = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
problem += (total_hours_m1 <= data['overtime_hour'], "Overtime_Hour_Constraint")

#### Profit constraint
problem += (profit >= data['min_profit'], "Minimum_Profit_Constraint")

#### Solve the problem
problem.solve()

#### Output results
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f' (Batches Produced): {batches_result}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

