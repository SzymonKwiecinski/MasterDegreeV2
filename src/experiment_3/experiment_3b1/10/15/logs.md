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

\section*{Mathematical Model for Daily Profit Maximization}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item $x_i$: number of units of product type $i$ produced, for $i = 1, \ldots, N$
    \item $o$: hours of overtime assembly labor scheduled
\end{itemize}

\subsection*{Parameters}
Given:
\begin{itemize}
    \item $assemblyHour_i$: hours of assembly labor required for product type $i$
    \item $testingHour_i$: hours of testing required for product type $i$
    \item $materialCost_i$: cost of raw materials for product type $i$ in dollars
    \item $maxAssembly$: maximum hours of assembly labor available per day
    \item $maxTesting$: maximum hours of testing available per day
    \item $price_i$: price of product type $i$ in dollars
    \item $maxOvertimeAssembly$: maximum hours of overtime assembly labor that can be scheduled
    \item $overtimeAssemblyCost$: cost of overtime assembly labor per hour
    \item $materialDiscount$: percentage discount on materials if the daily bill exceeds the threshold
    \item $discountThreshold$: threshold for material discount in dollars
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{maximize } Z = \sum_{i=1}^{N} \left( price_i \cdot x_i \right) - \sum_{i=1}^{N} \left( materialCost_i \cdot x_i \right) \cdot \left(1 - \frac{materialDiscount}{100} \cdot \mathbb{1}\left(\sum_{i=1}^{N} materialCost_i \cdot x_i > discountThreshold\right)\right) - o \cdot overtimeAssemblyCost
\]

\subsection*{Constraints}
1. Assembly labor constraint:
\[
\sum_{i=1}^{N} (assemblyHour_i \cdot x_i) + o \leq maxAssembly + maxOvertimeAssembly
\]

2. Testing labor constraint:
\[
\sum_{i=1}^{N} (testingHour_i \cdot x_i) \leq maxTesting
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \forall i = 1, \ldots, N
\]
\[
o \geq 0
\]

\subsection*{Output Variables}
The outputs are:
\begin{itemize}
    \item $dailyProfit = Z$
    \item $unitsProduced = [x_1, x_2, \ldots, x_N]$
    \item $overtimeAssembly = o$
    \item $materialBought = \sum_{i=1}^{N} materialCost_i \cdot x_i$
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

\section*{Mathematical Model for Daily Profit Maximization}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item $x_i$: number of units of product type $i$ produced, for $i = 1, \ldots, N$
    \item $o$: hours of overtime assembly labor scheduled
\end{itemize}

\subsection*{Parameters}
Given:
\begin{itemize}
    \item $assemblyHour_i$: hours of assembly labor required for product type $i$
    \item $testingHour_i$: hours of testing required for product type $i$
    \item $materialCost_i$: cost of raw materials for product type $i$ in dollars
    \item $maxAssembly$: maximum hours of assembly labor available per day
    \item $maxTesting$: maximum hours of testing available per day
    \item $price_i$: price of product type $i$ in dollars
    \item $maxOvertimeAssembly$: maximum hours of overtime assembly labor that can be scheduled
    \item $overtimeAssemblyCost$: cost of overtime assembly labor per hour
    \item $materialDiscount$: percentage discount on materials if the daily bill exceeds the threshold
    \item $discountThreshold$: threshold for material discount in dollars
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{maximize } Z = \sum_{i=1}^{N} \left( price_i \cdot x_i \right) - \sum_{i=1}^{N} \left( materialCost_i \cdot x_i \right) \cdot \left(1 - \frac{materialDiscount}{100} \cdot \mathbb{1}\left(\sum_{i=1}^{N} materialCost_i \cdot x_i > discountThreshold\right)\right) - o \cdot overtimeAssemblyCost
\]

\subsection*{Constraints}
1. Assembly labor constraint:
\[
\sum_{i=1}^{N} (assemblyHour_i \cdot x_i) + o \leq maxAssembly + maxOvertimeAssembly
\]

2. Testing labor constraint:
\[
\sum_{i=1}^{N} (testingHour_i \cdot x_i) \leq maxTesting
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \forall i = 1, \ldots, N
\]
\[
o \geq 0
\]

\subsection*{Output Variables}
The outputs are:
\begin{itemize}
    \item $dailyProfit = Z$
    \item $unitsProduced = [x_1, x_2, \ldots, x_N]$
    \item $overtimeAssembly = o$
    \item $materialBought = \sum_{i=1}^{N} materialCost_i \cdot x_i$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from JSON format
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

#### Create the linear programming problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  #### Units produced for each product
o = pulp.LpVariable("o", lowBound=0)  #### Overtime hours

#### Objective function
profit_terms = [
    (data['Price'][i] * x[i] for i in range(data['N'])),
]
material_cost_terms = [
    (data['MaterialCost'][i] * x[i] for i in range(data['N'])),
]
total_material_cost = pulp.lpSum(material_cost_terms)
material_discount = (data['MaterialDiscount'] / 100) * (total_material_cost > data['DiscountThreshold'])
objective = pulp.lpSum(profit_terms) - (total_material_cost * (1 - material_discount)) - (o * data['OvertimeAssemblyCost'])

problem += objective, "Total_Profit"

#### Constraints
#### 1. Assembly labor constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + o <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint"

#### 2. Testing labor constraint
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Labor_Constraint"

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

#### Data extracted from JSON format
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

#### Create the linear programming problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  #### Units produced for each product
o = pulp.LpVariable("o", lowBound=0)  #### Overtime hours

#### Objective function
profit_terms = [
    (data['Price'][i] * x[i] for i in range(data['N'])),
]
material_cost_terms = [
    (data['MaterialCost'][i] * x[i] for i in range(data['N'])),
]
total_material_cost = pulp.lpSum(material_cost_terms)
material_discount = (data['MaterialDiscount'] / 100) * (total_material_cost > data['DiscountThreshold'])
objective = pulp.lpSum(profit_terms) - (total_material_cost * (1 - material_discount)) - (o * data['OvertimeAssemblyCost'])

problem += objective, "Total_Profit"

#### Constraints
#### 1. Assembly labor constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + o <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint"

#### 2. Testing labor constraint
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Labor_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/10/15/python_code0.py", line 33, in <module>
    material_discount = (data['MaterialDiscount'] / 100) * (total_material_cost > data['DiscountThreshold'])
                                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '>' not supported between instances of 'LpAffineExpression' and 'int'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from JSON format
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

#### Create the linear programming problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  #### Units produced for each product
o = pulp.LpVariable("o", lowBound=0)  #### Overtime hours

#### Objective function
profit_terms = [
    (data['Price'][i] * x[i] for i in range(data['N'])),
]
material_cost_terms = [
    (data['MaterialCost'][i] * x[i] for i in range(data['N'])),
]
total_material_cost = pulp.lpSum(material_cost_terms)

#### Apply discount
material_discount = pulp.lpSum([1 if total_material_cost > data['DiscountThreshold'] else 0]) * (data['MaterialDiscount'] / 100)
objective = pulp.lpSum(profit_terms) - (total_material_cost * (1 - material_discount)) - (o * data['OvertimeAssemblyCost'])

problem += objective, "Total_Profit"

#### Constraints
#### 1. Assembly labor constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + o <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint"

#### 2. Testing labor constraint
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Labor_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

