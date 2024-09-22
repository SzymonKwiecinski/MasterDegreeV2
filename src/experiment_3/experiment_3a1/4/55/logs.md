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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Variables}
Let \( b_p \) represent the number of batches produced for part \( p \) where \( p = 1, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): Time required on machine \( m \) to produce one batch of part \( p \) (in hours).
    \item \( cost_m \): Cost per hour for using machine \( m \).
    \item \( available_m \): Availability of machine \( m \) (in hours).
    \item \( price_p \): Selling price per batch of part \( p \).
    \item \( min\_batches_p \): Minimum batches of part \( p \) required to fulfill contract.
    \item \( standard\_cost \): Standard labor cost per hour.
    \item \( overtime\_cost \): Overtime labor cost per hour.
    \item \( overtime\_hour \): Hours for which standard cost applies before overtime kicks in.
    \item \( min\_profit \): Minimum desired profit.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p))
\]

Where labor costs for machine 1 are given by:

\[
\text{Labor Cost} = 
\begin{cases} 
standard\_cost \cdot \min(\text{Hours Used}, overtime\_hour) + overtime\_cost \cdot \max(0, \text{Hours Used} - overtime\_hour) & \text{if } m = 1 \\
0 & \text{else}
\end{cases}
\]

\subsection*{Constraints}
1. Time availability for each machine:
   \[
   \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_m, \quad \forall m = 1, \ldots, M
   \]

2. Minimum batch requirements:
   \[
   b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
   \]

3. Profit constraint:
   \[
   Z \geq min\_profit
   \]

4. Non-negativity:
   \[
   b_p \geq 0, \quad \forall p = 1, \ldots, P
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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Variables}
Let \( b_p \) represent the number of batches produced for part \( p \) where \( p = 1, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): Time required on machine \( m \) to produce one batch of part \( p \) (in hours).
    \item \( cost_m \): Cost per hour for using machine \( m \).
    \item \( available_m \): Availability of machine \( m \) (in hours).
    \item \( price_p \): Selling price per batch of part \( p \).
    \item \( min\_batches_p \): Minimum batches of part \( p \) required to fulfill contract.
    \item \( standard\_cost \): Standard labor cost per hour.
    \item \( overtime\_cost \): Overtime labor cost per hour.
    \item \( overtime\_hour \): Hours for which standard cost applies before overtime kicks in.
    \item \( min\_profit \): Minimum desired profit.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p))
\]

Where labor costs for machine 1 are given by:

\[
\text{Labor Cost} = 
\begin{cases} 
standard\_cost \cdot \min(\text{Hours Used}, overtime\_hour) + overtime\_cost \cdot \max(0, \text{Hours Used} - overtime\_hour) & \text{if } m = 1 \\
0 & \text{else}
\end{cases}
\]

\subsection*{Constraints}
1. Time availability for each machine:
   \[
   \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_m, \quad \forall m = 1, \ldots, M
   \]

2. Minimum batch requirements:
   \[
   b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
   \]

3. Profit constraint:
   \[
   Z \geq min\_profit
   \]

4. Non-negativity:
   \[
   b_p \geq 0, \quad \forall p = 1, \ldots, P
   \]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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
problem = pulp.LpProblem("Auto_Parts_Manufacturer_Problem", pulp.LpMaximize)

#### Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

#### Decision variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  #### batches produced for each part

#### Objective function
profit = pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(M))

#### Adding labor costs for machine 1
labor_cost_machine_1 = pulp.lpSum(data['standard_cost'] * pulp.lpMin(pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P)), data['overtime_hour']) + 
                                 data['overtime_cost'] * pulp.lpMax(0, pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P)) - data['overtime_hour']))

#### Final objective function including labor costs for machine 1
problem += profit - labor_cost_machine_1

#### Constraints
#### Time availability for each machine
for m in range(M):
    problem += pulp.lpSum(data['time_required[m][p]'] * b[p] for p in range(P)) <= data['availability'][m], f"Time_Availability_Machine_{m}"

#### Minimum batch requirements
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_Batches_Part_{p}"

#### Profit constraint
problem += profit >= data['min_profit'], "Min_Profit"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

