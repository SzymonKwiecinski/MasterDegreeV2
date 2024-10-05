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
To formulate this problem as a linear program, we need to define decision variables, an objective function, and a set of constraints based on the given problem description.

######### Decision Variables
- Let \( x_p \) be the number of batches of part \( p \) produced each month, for \( p = 1, \ldots, P \).

######### Objective Function
We aim to maximize the total profit. The profit for selling part \( p \) is given by:
\[
\text{Profit for part } p = \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_m
\]

Considering machine 1 with labor costs and potential overtime:
- For machine 1, if \( \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p \leq \text{overtime\_hour} \), then the cost is \(\text{standard\_cost} \cdot \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p\).
- Otherwise, it's \(\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot \left(\sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p - \text{overtime\_hour}\right)\).

######### Constraints
1. **Machine Availability:**
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m \quad \text{for } m = 2, \ldots, M
   \]

2. **Minimum Batches Requirement:**
   \[
   x_p \geq \text{min\_batches}_p \quad \text{for } p = 1, \ldots, P
   \]

3. **Minimum Profit Requirement:**
   \[
   \sum_{p=1}^{P} \left(\text{price}_p \cdot x_p - \sum_{m=2}^{M} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_m\right) - \left( \text{standard\_cost} \cdot y + \text{overtime\_cost} \cdot z \right) \geq \text{min\_profit}
   \]
   where \( y \) is the hours worked at standard cost and \( z \) is the hours worked at overtime cost for machine 1 subject to:
   \[
   y + z = \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p
   \]
   \[
   0 \leq y \leq \text{overtime\_hour}
   \]

######### Linear Programming Model in LaTeX
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\begin{align*}
\text{Maximize } & \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p - \sum_{m=2}^{M} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_m \right) \\
& - \left( \text{standard\_cost} \cdot y + \text{overtime\_cost} \cdot z \right) \\
\text{subject to:} \\
& \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m, \quad m = 2, \ldots, M, \\
& x_p \geq \text{min\_batches}_p, \quad p = 1, \ldots, P, \\
& y + z = \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p, \\
& 0 \leq y \leq \text{overtime\_hour}, \\
& \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p - \sum_{m=2}^{M} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_m \right) \\
& - \left( \text{standard\_cost} \cdot y + \text{overtime\_cost} \cdot z \right) \geq \text{min\_profit}.
\end{align*}

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

\begin{align*}
\text{Maximize } & \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p - \sum_{m=2}^{M} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_m \right) \\
& - \left( \text{standard\_cost} \cdot y + \text{overtime\_cost} \cdot z \right) \\
\text{subject to:} \\
& \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m, \quad m = 2, \ldots, M, \\
& x_p \geq \text{min\_batches}_p, \quad p = 1, \ldots, P, \\
& y + z = \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p, \\
& 0 \leq y \leq \text{overtime\_hour}, \\
& \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p - \sum_{m=2}^{M} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_m \right) \\
& - \left( \text{standard\_cost} \cdot y + \text{overtime\_cost} \cdot z \right) \geq \text{min\_profit}.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


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
    'min_batches': [10, 10, 10, 10], 
    'standard_cost': 20, 
    'overtime_cost': 30, 
    'overtime_hour': 400, 
    'min_profit': 5000
}

#### Create the problem
problem = pulp.LpProblem("MaximizeProfit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(len(data['prices']))]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')
z = pulp.LpVariable('z', cat='Continuous')

#### Objective function
profit = pulp.lpSum(
    data['prices'][p] * x[p] - pulp.lpSum(data['time_required'][m][p] * x[p] * data['machine_costs'][m] for m in range(1, len(data['machine_costs'])))
    for p in range(len(data['prices']))
) - (data['standard_cost'] * y + data['overtime_cost'] * z)

problem += profit

#### Constraints
for m in range(1, len(data['availability'])):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(len(data['prices']))) <= data['availability'][m]

problem += y + z == pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(len(data['prices'])))
problem += y <= data['overtime_hour']
problem += profit >= data['min_profit']

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

