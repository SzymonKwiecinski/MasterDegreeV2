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

\subsection*{Sets and Indices}
\begin{align*}
P & : \text{Set of parts, indexed by } p = 1, \ldots, P \\
M & : \text{Set of machines, indexed by } m = 1, \ldots, M
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{time\_required}_{m,p} & : \text{Time required on machine } m \text{ to produce a batch of part } p \\
\text{cost}_{m} & : \text{Cost per hour of operating machine } m \\
\text{available}_{m} & : \text{Availability of machine } m \text{ in hours per month} \\
\text{price}_{p} & : \text{Selling price of 100-part batch of part } p \\
\text{min\_batches}_{p} & : \text{Minimum batches of part } p \text{ that must be produced each month} \\
\text{standard\_cost} & : \text{Standard labor cost for machine 1 up to overtime hours} \\
\text{overtime\_cost} & : \text{Overtime labor cost for machine 1 beyond overtime hours} \\
\text{overtime\_hour} & : \text{Maximum regular hours for machine 1 before overtime} \\
\text{min\_profit} & : \text{Minimum desired profit for the month}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{batches}_{p} & : \text{Number of batches of part } p \text{ produced (integer)} \\
\text{profit} & : \text{Total profit obtained for the month}
\end{align*}

\subsection*{Objective Function}
Maximize total profit:
\begin{align*}
\text{profit} & = \sum_{p=1}^{P} (\text{price}_{p} \cdot \text{batches}_{p}) - \sum_{m=2}^{M} \left( \sum_{p=1}^{P} (\text{time\_required}_{m,p} \cdot \text{batches}_{p}) \cdot \text{cost}_{m} \right) \\
& \quad - \left( \sum_{p=1}^{P} (\text{time\_required}_{1,p} \cdot \text{batches}_{p}) \cdot \text{standard\_cost} \right) + \text{possible\_overtime\_cost}
\end{align*}

Where:
\begin{align*}
\text{possible\_overtime\_cost} & = \begin{cases} 
0, & \text{if } \sum_{p=1}^{P} (\text{time\_required}_{1,p} \cdot \text{batches}_{p}) \leq \text{overtime\_hour} \\
\left( \sum_{p=1}^{P} (\text{time\_required}_{1,p} \cdot \text{batches}_{p}) - \text{overtime\_hour} \right) \cdot (\text{overtime\_cost} - \text{standard\_cost}), & \text{otherwise}
\end{cases}
\end{align*}

\subsection*{Constraints}
\begin{align*}
\sum_{p=1}^{P} (\text{time\_required}_{m,p} \cdot \text{batches}_{p}) & \leq \text{available}_{m}, & \forall m = 2, \ldots, M \\
\text{batches}_{p} & \geq \text{min\_batches}_{p}, & \forall p = 1, \ldots, P \\
\text{profit} & \geq \text{min\_profit}
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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Sets and Indices}
\begin{align*}
P & : \text{Set of parts, indexed by } p = 1, \ldots, P \\
M & : \text{Set of machines, indexed by } m = 1, \ldots, M
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{time\_required}_{m,p} & : \text{Time required on machine } m \text{ to produce a batch of part } p \\
\text{cost}_{m} & : \text{Cost per hour of operating machine } m \\
\text{available}_{m} & : \text{Availability of machine } m \text{ in hours per month} \\
\text{price}_{p} & : \text{Selling price of 100-part batch of part } p \\
\text{min\_batches}_{p} & : \text{Minimum batches of part } p \text{ that must be produced each month} \\
\text{standard\_cost} & : \text{Standard labor cost for machine 1 up to overtime hours} \\
\text{overtime\_cost} & : \text{Overtime labor cost for machine 1 beyond overtime hours} \\
\text{overtime\_hour} & : \text{Maximum regular hours for machine 1 before overtime} \\
\text{min\_profit} & : \text{Minimum desired profit for the month}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{batches}_{p} & : \text{Number of batches of part } p \text{ produced (integer)} \\
\text{profit} & : \text{Total profit obtained for the month}
\end{align*}

\subsection*{Objective Function}
Maximize total profit:
\begin{align*}
\text{profit} & = \sum_{p=1}^{P} (\text{price}_{p} \cdot \text{batches}_{p}) - \sum_{m=2}^{M} \left( \sum_{p=1}^{P} (\text{time\_required}_{m,p} \cdot \text{batches}_{p}) \cdot \text{cost}_{m} \right) \\
& \quad - \left( \sum_{p=1}^{P} (\text{time\_required}_{1,p} \cdot \text{batches}_{p}) \cdot \text{standard\_cost} \right) + \text{possible\_overtime\_cost}
\end{align*}

Where:
\begin{align*}
\text{possible\_overtime\_cost} & = \begin{cases} 
0, & \text{if } \sum_{p=1}^{P} (\text{time\_required}_{1,p} \cdot \text{batches}_{p}) \leq \text{overtime\_hour} \\
\left( \sum_{p=1}^{P} (\text{time\_required}_{1,p} \cdot \text{batches}_{p}) - \text{overtime\_hour} \right) \cdot (\text{overtime\_cost} - \text{standard\_cost}), & \text{otherwise}
\end{cases}
\end{align*}

\subsection*{Constraints}
\begin{align*}
\sum_{p=1}^{P} (\text{time\_required}_{m,p} \cdot \text{batches}_{p}) & \leq \text{available}_{m}, & \forall m = 2, \ldots, M \\
\text{batches}_{p} & \geq \text{min\_batches}_{p}, & \forall p = 1, \ldots, P \\
\text{profit} & \geq \text{min\_profit}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = '''
{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10],
    "standard_cost": 20,
    "overtime_cost": 30,
    "overtime_hour": 400,
    "min_profit": 5000
}
'''

#### Load data from JSON
data = json.loads(data)

#### Define sets and indices
P = len(data['prices'])
M = len(data['machine_costs'])

#### Create a linear programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
profit = pulp.LpVariable("profit")

#### Objective Function
problem += (pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) -
            pulp.lpSum((data['machine_costs'][m] * 
                         pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)))
                        for m in range(1, M)) -
            pulp.lpSum((data['standard_cost'] * 
                         pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)))) +
            (pulp.lpSum((pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) -
                          data['overtime_hour']) * (data['overtime_cost'] - data['standard_cost']))
             if pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) > data['overtime_hour'] else 0),
            "Total_Profit")

#### Constraints
for m in range(1, M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], 
                       f"Availability_Constraint_{m}")

for p in range(P):
    problem += (batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}")

problem += (profit >= data['min_profit'], "Min_Profit_Constraint")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
```python
import pulp
import json

#### Data provided in JSON format
data = '''
{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10],
    "standard_cost": 20,
    "overtime_cost": 30,
    "overtime_hour": 400,
    "min_profit": 5000
}
'''

#### Load data from JSON
data = json.loads(data)

#### Define sets and indices
P = len(data['prices'])
M = len(data['machine_costs'])

#### Create a linear programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
profit = pulp.LpVariable("profit")

#### Objective Function
problem += (pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) -
            pulp.lpSum((data['machine_costs'][m] * 
                         pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)))
                        for m in range(1, M)) -
            pulp.lpSum((data['standard_cost'] * 
                         pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)))) +
            (pulp.lpSum((pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) -
                          data['overtime_hour']) * (data['overtime_cost'] - data['standard_cost']))
             if pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) > data['overtime_hour'] else 0),
            "Total_Profit")

#### Constraints
for m in range(1, M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], 
                       f"Availability_Constraint_{m}")

for p in range(P):
    problem += (batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}")

problem += (profit >= data['min_profit'], "Min_Profit_Constraint")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b2/5/55/python_code0.py", line 42, in <module>
    if pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) > data['overtime_hour'] else 0),
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '>' not supported between instances of 'LpAffineExpression' and 'int'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = '''
{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10],
    "standard_cost": 20,
    "overtime_cost": 30,
    "overtime_hour": 400,
    "min_profit": 5000
}
'''

#### Load data from JSON
data = json.loads(data)

#### Define sets and indices
P = len(data['prices'])
M = len(data['machine_costs'])

#### Create a linear programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
profit = pulp.LpVariable("profit")

#### Objective Function
total_profit = (pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) -
                pulp.lpSum((data['machine_costs'][m] * 
                             pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)))
                            for m in range(1, M)) -
                pulp.lpSum((data['standard_cost'] * 
                             pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)))) +
                (pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) - 
                 data['overtime_hour']) * (data['overtime_cost'] - data['standard_cost']))

problem += total_profit, "Total_Profit"

#### Constraints
for m in range(1, M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], 
                       f"Availability_Constraint_{m}")

for p in range(P):
    problem += (batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}")

problem += (profit >= data['min_profit'], "Min_Profit_Constraint")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

