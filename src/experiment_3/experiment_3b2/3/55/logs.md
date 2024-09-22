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
To formulate the problem as a linear programming model, we can start by defining the decision variables, objective function, and constraints based on the problem description.

Let's define:

- Decision Variables:
  - \( x_p \): the number of batches to produce for each part \( p \), where \( p = 1, \ldots, P \).

- Objective Function:
  - The objective is to maximize the profit, given by the revenue from selling parts minus the cost of machine usage and labor costs.

The linear programming model can be formulated as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize \( \text{Profit} = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \sum_{p=1}^{P} \text{cost}_m \cdot \text{time}_{m,p} \cdot x_p - \text{LaborCost} \)

Where:
\[
\text{LaborCost} = 
\begin{cases} 
\text{standard\_cost} \cdot \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p, & \text{if } \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p \leq \text{overtime\_hour}\\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left( \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p - \text{overtime\_hour} \right), & \text{otherwise}
\end{cases}
\]

\textbf{Subject to:}

1. Minimum production requirement for each part:
   \[
   x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]

2. Machine availability constraints (excluding machine 1):
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m, \quad \forall m = 2, \ldots, M
   \]

3. Profit constraint:
   \[
   \text{Profit} \geq \text{min\_profit}
   \]

4. Non-negativity constraints:
   \[
   x_p \geq 0, \quad \forall p = 1, \ldots, P
   \]

\end{document}
```

In this model:
- The objective function is constructed to calculate the profit as the difference between total sales revenue and the total costs incurred from machine usage and labor for machine 1.
- The labor cost for machine 1 is calculated based on whether the usage exceeds the standard hours available before incurring overtime costs.
- Constraints ensure minimum batches are met, availability is not exceeded for machines except for machine 1, and the profit requirement is satisfied.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize \( \text{Profit} = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \sum_{p=1}^{P} \text{cost}_m \cdot \text{time}_{m,p} \cdot x_p - \text{LaborCost} \)

Where:
\[
\text{LaborCost} = 
\begin{cases} 
\text{standard\_cost} \cdot \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p, & \text{if } \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p \leq \text{overtime\_hour}\\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left( \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p - \text{overtime\_hour} \right), & \text{otherwise}
\end{cases}
\]

\textbf{Subject to:}

1. Minimum production requirement for each part:
   \[
   x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]

2. Machine availability constraints (excluding machine 1):
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m, \quad \forall m = 2, \ldots, M
   \]

3. Profit constraint:
   \[
   \text{Profit} \geq \text{min\_profit}
   \]

4. Non-negativity constraints:
   \[
   x_p \geq 0, \quad \forall p = 1, \ldots, P
   \]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

#### Parameters
P = len(data['prices'])  #### Number of parts
M = len(data['availability'])  #### Number of machines
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

#### Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

#### Objective function
labor_cost = pulp.LpVariable("LaborCost")
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(1, M)) - labor_cost

problem += profit

#### Labor cost constraints
total_time = pulp.lpSum(time_required[0][p] * x[p] for p in range(P))
problem += labor_cost == (standard_cost * total_time if total_time <= overtime_hour else 
                           standard_cost * overtime_hour + 
                           overtime_cost * (total_time - overtime_hour))

#### Constraints
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_batches_constraint_part_{p}"

for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Availability_constraint_machine_{m}"

problem += profit >= min_profit, "Profit_constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

