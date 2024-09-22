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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
The objective is to maximize the total profit, which can be defined as:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \text{Total\_time}_m) - \text{Labor\_cost}
\]

where the total time for each machine \( m \) is given by:

\[
\text{Total\_time}_m = \sum_{p=1}^{P} (time_{m,p} \cdot b_p)
\]

The labor cost is defined as:

\[
\text{Labor\_cost} = 
\begin{cases} 
standard\_cost \cdot \text{time\_used} & \text{if } \text{time\_used} \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (\text{time\_used} - overtime\_hour) & \text{if } \text{time\_used} > overtime\_hour 
\end{cases}
\]

where \( \text{time\_used} = \sum_{p=1}^{P} (time_{1,p} \cdot b_p) \).

\subsection*{Constraints}

1. **Machine Time Availability:**
   Each machine \( m \) must not exceed its available hours:

   \[
   \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_m, \quad \forall m = 1, \ldots, M
   \]

2. **Minimum Batches Required:**
   Each part \( p \) must meet the minimum batch requirement:

   \[
   b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
   \]

3. **Minimum Profit Requirement:**
   The total profit must exceed the minimum profit:

   \[
   Z \geq min\_profit
   \]

4. **Non-negativity Constraints:**
   The batches produced must be non-negative:

   \[
   b_p \geq 0, \quad \forall p = 1, \ldots, P
   \]

\subsection*{Output Variables}
The solution should provide:

\begin{itemize}
    \item An array representing the number of batches produced for each part: \( \{b_p\} \)
    \item The total profit: \( total\_profit = Z \)
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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).

\subsection*{Objective Function}
The objective is to maximize the total profit, which can be defined as:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \text{Total\_time}_m) - \text{Labor\_cost}
\]

where the total time for each machine \( m \) is given by:

\[
\text{Total\_time}_m = \sum_{p=1}^{P} (time_{m,p} \cdot b_p)
\]

The labor cost is defined as:

\[
\text{Labor\_cost} = 
\begin{cases} 
standard\_cost \cdot \text{time\_used} & \text{if } \text{time\_used} \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (\text{time\_used} - overtime\_hour) & \text{if } \text{time\_used} > overtime\_hour 
\end{cases}
\]

where \( \text{time\_used} = \sum_{p=1}^{P} (time_{1,p} \cdot b_p) \).

\subsection*{Constraints}

1. **Machine Time Availability:**
   Each machine \( m \) must not exceed its available hours:

   \[
   \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_m, \quad \forall m = 1, \ldots, M
   \]

2. **Minimum Batches Required:**
   Each part \( p \) must meet the minimum batch requirement:

   \[
   b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
   \]

3. **Minimum Profit Requirement:**
   The total profit must exceed the minimum profit:

   \[
   Z \geq min\_profit
   \]

4. **Non-negativity Constraints:**
   The batches produced must be non-negative:

   \[
   b_p \geq 0, \quad \forall p = 1, \ldots, P
   \]

\subsection*{Output Variables}
The solution should provide:

\begin{itemize}
    \item An array representing the number of batches produced for each part: \( \{b_p\} \)
    \item The total profit: \( total\_profit = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data input
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

#### Indices
P = len(data['prices'])
M = len(data['machine_costs'])

#### Define the Linear Programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Variables: number of batches for each part
b = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(P)]

#### Time used on the labor machine (Machine 1)
time_used = pulp.lpSum([data['time_required'][0][p] * b[p] for p in range(P)])

#### Total machine cost for each machine
total_time = [pulp.lpSum([data['time_required'][m][p] * b[p] for p in range(P)]) for m in range(M)]

#### Labor cost calculation
labor_cost = pulp.LpVariable("Labor_Cost", lowBound=0, cat='Continuous')
problem += labor_cost >= data['standard_cost'] * time_used
problem += labor_cost >= (data['standard_cost'] * data['overtime_hour'] + 
                          data['overtime_cost'] * (time_used - data['overtime_hour']))

#### Objective function
total_income = pulp.lpSum([data['prices'][p] * b[p] for p in range(P)])
total_machine_costs = pulp.lpSum([data['machine_costs'][m] * total_time[m] for m in range(M)])
problem += total_income - total_machine_costs - labor_cost, "Total_Profit"

#### Constraints

#### Machine time availability constraints
for m in range(M):
    problem += total_time[m] <= data['availability'][m], f"Machine_{m}_Availability"

#### Minimum batches required for each part
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_Batches_{p}"

#### Minimum profit requirement
problem += (total_income - total_machine_costs - labor_cost) >= data['min_profit'], "Min_Profit"

#### Solve the problem
problem.solve()

#### Output results
batches_produced = [pulp.value(b[p]) for p in range(P)]
print("Batches Produced:", batches_produced)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

