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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \), where \( p = 1, \ldots, P \).

\subsection*{Objective Function}
The objective is to maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \text{hours\_used}_m) - \text{labor\_cost}
\]

where \( \text{hours\_used}_m = \sum_{p=1}^{P} (time_{m,p} \cdot b_p / 100) \) for \( m = 1, \ldots, M \).

The labor cost for machine 1 (outsourced) is calculated as:

\[
\text{labor\_cost} = 
\begin{cases} 
standard\_cost \cdot \text{hours\_used}_1 & \text{if } \text{hours\_used}_1 \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (\text{hours\_used}_1 - overtime\_hour) & \text{if } \text{hours\_used}_1 > overtime\_hour 
\end{cases}
\]

\subsection*{Constraints}
1. **Batch Production Requirements**:
   \[
   b_p \geq min\_batches_p \quad \forall p \in \{1, \ldots, P\}
   \]

2. **Machine Availability**:
   \[
   \sum_{p=1}^{P} \left( \frac{time_{m,p}}{100} b_p \right) \leq available_m \quad \forall m \in \{1, \ldots, M\}
   \]

3. **Minimum Profit Requirement**:
   \[
   Z \geq min\_profit
   \]

4. **Non-negativity**:
   \[
   b_p \geq 0 \quad \forall p \in \{1, \ldots, P\}
   \]

\subsection*{Output}
The output will consist of:
- The number of batches of each part produced \( b_p \) for \( p = 1, \ldots, P \).
- The total profit \( Z \).

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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \), where \( p = 1, \ldots, P \).

\subsection*{Objective Function}
The objective is to maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} (cost_m \cdot \text{hours\_used}_m) - \text{labor\_cost}
\]

where \( \text{hours\_used}_m = \sum_{p=1}^{P} (time_{m,p} \cdot b_p / 100) \) for \( m = 1, \ldots, M \).

The labor cost for machine 1 (outsourced) is calculated as:

\[
\text{labor\_cost} = 
\begin{cases} 
standard\_cost \cdot \text{hours\_used}_1 & \text{if } \text{hours\_used}_1 \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (\text{hours\_used}_1 - overtime\_hour) & \text{if } \text{hours\_used}_1 > overtime\_hour 
\end{cases}
\]

\subsection*{Constraints}
1. **Batch Production Requirements**:
   \[
   b_p \geq min\_batches_p \quad \forall p \in \{1, \ldots, P\}
   \]

2. **Machine Availability**:
   \[
   \sum_{p=1}^{P} \left( \frac{time_{m,p}}{100} b_p \right) \leq available_m \quad \forall m \in \{1, \ldots, M\}
   \]

3. **Minimum Profit Requirement**:
   \[
   Z \geq min\_profit
   \]

4. **Non-negativity**:
   \[
   b_p \geq 0 \quad \forall p \in \{1, \ldots, P\}
   \]

\subsection*{Output}
The output will consist of:
- The number of batches of each part produced \( b_p \) for \( p = 1, \ldots, P \).
- The total profit \( Z \).

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from the provided JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

#### Extracting data for easier use
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Continuous')

#### Define the objective function
hours_used = [pulp.lpSum((time_required[m][p] / 100) * b[p] for p in range(P)) for m in range(M)]
labor_cost = pulp.lpSum([standard_cost * hours_used[0] if hours_used[0] <= overtime_hour else 
                          standard_cost * overtime_hour + overtime_cost * (hours_used[0] - overtime_hour)])
                        
profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * hours_used[m] for m in range(M)) - labor_cost
problem += profit, "Total_Profit"

#### Constraints
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Batches_Constraint_{p+1}"

for m in range(M):
    problem += pulp.lpSum((time_required[m][p] / 100) * b[p] for p in range(P)) <= availability[m], f"Machine_Availability_Constraint_{m+1}"

problem += profit >= min_profit, "Min_Profit_Constraint"

#### Solve the problem
problem.solve()

#### Print results
for p in range(P):
    print(f'Batches produced for part {p+1}: {b[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

