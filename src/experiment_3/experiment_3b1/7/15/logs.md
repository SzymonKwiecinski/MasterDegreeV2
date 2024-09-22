# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO: 
- A company produces \var{N} kinds of products. 
- A product of the \var{i}-th type requires \var{assemblyHour_i} hours of assembly labor, \var{testingHour_i} hours of testing, and \var{materialCost_i} worth of raw materials (in $).
- Given the current personnel of the company, there can be at most \var{maxAssembly} hours of assembly labor and \var{maxTesting} hours of testing, each day.
- Product of the \var{i}-th type has a price of \var{price_i} dollars.
- The company can schedule up tp \var{maxOvertimeAssembly} hours of overtime assembly labor can be sched­uled, at a cost of \var{overtimeAssemblyCost} per hour.
- Suppose that the raw material supplier provides a \var{materialDiscount}% discount if the daily bill is above \var{discountThreshold} dollars (\var{materialDiscount} is a number between 0 and 100).

INPUT FORMAT: 

{
    "assemblyHour": [assemblyHour_i for i in 1, ..., N]
    "testingHour": [testingHour_i for i in 1, ..., N],
    "materialCost": [materialCost_i for i in 1, ..., N],
    "maxAssembly": maxAssembly
    "maxTesting": maxTesting,
    "price": [price_i for i in 1, ..., N],
    "maxOvertimeAssembly": maxOvertimeAssembly,
    "overtimeAssemblyCost": overtimeAssemblyCost,
    "materialDiscount": materialDiscount,
    "discountThreshold": discountThreshold
}

OBJECTIVE: We want to maximize the daily profit of the company, which is the total revenue minus the total cost.

OUTPUT INFO: 

- \var{dailyProfit} shows the daily profit of the company 
- \var{unitsProduced_i} shows the number of units of the \var{i}-th product produced
- \var{overtimeAssembly} shows the number of hours of overtime assembly labor scheduled
- \var{materialBought} shows the amount of raw materials bought

OUTPUT FORMAT:

{
    "dailyProfit": dailyProfit,
    "unitsProduced": [unitsProduced_i for i in 1, ..., N],
    "overtimeAssembly": overtimeAssembly,
    "materialBought": materialBought
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mixed Integer Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of product types
    \item $assemblyHour_i$: Hours of assembly labor required for product type $i$
    \item $testingHour_i$: Hours of testing required for product type $i$
    \item $materialCost_i$: Cost of raw materials for product type $i$ (in dollars)
    \item $maxAssembly$: Maximum assembly hours available per day
    \item $maxTesting$: Maximum testing hours available per day
    \item $price_i$: Selling price for product type $i$ (in dollars)
    \item $maxOvertimeAssembly$: Maximum overtime assembly hours that can be scheduled
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly
    \item $materialDiscount$: Percentage discount on materials if daily bill exceeds the threshold
    \item $discountThreshold$: Threshold for material discount (in dollars)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $unitsProduced_i$: Number of units produced of product type $i$
    \item $overtimeAssembly$: Number of hours of overtime assembly labor scheduled
    \item $materialBought$: Total cost of raw materials bought
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{maximize} \quad dailyProfit = \sum_{i=1}^{N} (price_i \cdot unitsProduced_i) - \left( \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \cdot (1 - \frac{materialDiscount}{100}) \cdot \mathbbm{1}\left(\sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i > discountThreshold\right) + \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \cdot \mathbbm{1}\left(\sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \leq discountThreshold\right) + overtimeAssembly \cdot overtimeAssemblyCost \right)
\]

\subsection*{Constraints}
\begin{align*}
    \sum_{i=1}^{N} assemblyHour_i \cdot unitsProduced_i & \leq maxAssembly + overtimeAssembly \\
    \sum_{i=1}^{N} testingHour_i \cdot unitsProduced_i & \leq maxTesting \\
    0 \leq overtimeAssembly & \leq maxOvertimeAssembly \\
    unitsProduced_i & \geq 0 \quad \forall i \in \{1, \ldots, N\} \\
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

\section*{Mixed Integer Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of product types
    \item $assemblyHour_i$: Hours of assembly labor required for product type $i$
    \item $testingHour_i$: Hours of testing required for product type $i$
    \item $materialCost_i$: Cost of raw materials for product type $i$ (in dollars)
    \item $maxAssembly$: Maximum assembly hours available per day
    \item $maxTesting$: Maximum testing hours available per day
    \item $price_i$: Selling price for product type $i$ (in dollars)
    \item $maxOvertimeAssembly$: Maximum overtime assembly hours that can be scheduled
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly
    \item $materialDiscount$: Percentage discount on materials if daily bill exceeds the threshold
    \item $discountThreshold$: Threshold for material discount (in dollars)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $unitsProduced_i$: Number of units produced of product type $i$
    \item $overtimeAssembly$: Number of hours of overtime assembly labor scheduled
    \item $materialBought$: Total cost of raw materials bought
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{maximize} \quad dailyProfit = \sum_{i=1}^{N} (price_i \cdot unitsProduced_i) - \left( \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \cdot (1 - \frac{materialDiscount}{100}) \cdot \mathbbm{1}\left(\sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i > discountThreshold\right) + \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \cdot \mathbbm{1}\left(\sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \leq discountThreshold\right) + overtimeAssembly \cdot overtimeAssemblyCost \right)
\]

\subsection*{Constraints}
\begin{align*}
    \sum_{i=1}^{N} assemblyHour_i \cdot unitsProduced_i & \leq maxAssembly + overtimeAssembly \\
    \sum_{i=1}^{N} testingHour_i \cdot unitsProduced_i & \leq maxTesting \\
    0 \leq overtimeAssembly & \leq maxOvertimeAssembly \\
    unitsProduced_i & \geq 0 \quad \forall i \in \{1, \ldots, N\} \\
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'N': 2,
    'AssemblyHour': [0.25, 0.3333],
    'TestingHour': [0.125, 0.3333],
    'MaterialCost': [1.2, 0.9],
    'MaxAssembly': 10,
    'MaxTesting': 70,
    'Price': [9, 8],
    'MaxOvertimeAssembly': 50,
    'OvertimeAssemblyCost': 5,
    'MaterialDiscount': 10,
    'DiscountThreshold': 300
}

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')
materialBought = pulp.LpVariable('materialBought', lowBound=0, cat='Continuous')

#### Objective Function
material_cost = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
total_material_cost_discounted = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] * (1 - data['MaterialDiscount'] / 100) for i in range(data['N'])) 
profit = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N'])) - (
    total_material_cost_discounted * pulp.lpIndicator(material_cost > data['DiscountThreshold']) +
    material_cost * pulp.lpIndicator(material_cost <= data['DiscountThreshold']) +
    overtimeAssembly * data['OvertimeAssemblyCost']
)

problem += profit

#### Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxAssembly'] + overtimeAssembly
problem += pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxTesting']

#### Solve the problem
problem.solve()

#### Output the objective value
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

#### Data from JSON
data = {
    'N': 2,
    'AssemblyHour': [0.25, 0.3333],
    'TestingHour': [0.125, 0.3333],
    'MaterialCost': [1.2, 0.9],
    'MaxAssembly': 10,
    'MaxTesting': 70,
    'Price': [9, 8],
    'MaxOvertimeAssembly': 50,
    'OvertimeAssemblyCost': 5,
    'MaterialDiscount': 10,
    'DiscountThreshold': 300
}

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')
materialBought = pulp.LpVariable('materialBought', lowBound=0, cat='Continuous')

#### Objective Function
material_cost = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
total_material_cost_discounted = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] * (1 - data['MaterialDiscount'] / 100) for i in range(data['N'])) 
profit = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N'])) - (
    total_material_cost_discounted * pulp.lpIndicator(material_cost > data['DiscountThreshold']) +
    material_cost * pulp.lpIndicator(material_cost <= data['DiscountThreshold']) +
    overtimeAssembly * data['OvertimeAssemblyCost']
)

problem += profit

#### Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxAssembly'] + overtimeAssembly
problem += pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxTesting']

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/7/15/python_code0.py", line 30, in <module>
    total_material_cost_discounted * pulp.lpIndicator(material_cost > data['DiscountThreshold']) +
                                     ^^^^^^^^^^^^^^^^
AttributeError: module 'pulp' has no attribute 'lpIndicator'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'N': 2,
    'AssemblyHour': [0.25, 0.3333],
    'TestingHour': [0.125, 0.3333],
    'MaterialCost': [1.2, 0.9],
    'MaxAssembly': 10,
    'MaxTesting': 70,
    'Price': [9, 8],
    'MaxOvertimeAssembly': 50,
    'OvertimeAssemblyCost': 5,
    'MaterialDiscount': 10,
    'DiscountThreshold': 300
}

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')
materialBought = pulp.LpVariable('materialBought', lowBound=0, cat='Continuous')

#### Objective Function
material_cost = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
total_material_cost_discounted = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] * (1 - data['MaterialDiscount'] / 100) for i in range(data['N'])) 
profit = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N'])) - (
    total_material_cost_discounted * (material_cost > data['DiscountThreshold']) +
    material_cost * (material_cost <= data['DiscountThreshold']) +
    overtimeAssembly * data['OvertimeAssemblyCost']
)

problem += profit

#### Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxAssembly'] + overtimeAssembly
problem += pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxTesting']

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

