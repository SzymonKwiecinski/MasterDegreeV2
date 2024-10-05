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

\section*{Mathematical Model for the Company's Problem}

Define the decision variables:
\begin{align*}
    x_i & \text{ : number of units of product type } i \text{ produced, for } i = 1, 2, \ldots, N \\
    z   & \text{ : number of hours of overtime assembly labor scheduled}
\end{align*}

The objective is to maximize the daily profit, given by:
\[
\text{Maximize } \sum_{i=1}^{N} \left( \text{price}_i \cdot x_i - \text{materialCost}_i \cdot x_i \right) - \text{overtimeAssemblyCost} \cdot z
\]

Subject to the constraints:
\begin{align*}
    &\text{Assembly Labor Constraint:} \\
    & \sum_{i=1}^{N} \text{assemblyHour}_i \cdot x_i \leq \text{maxAssembly} + z \\
    &z \leq \text{maxOvertimeAssembly} \\
    &\text{Testing Constraint:} \\
    & \sum_{i=1}^{N} \text{testingHour}_i \cdot x_i \leq \text{maxTesting} \\
    &\text{Raw Material Discount Constraint (Only for Total Cost Calculation):} \\
    &\text{If } \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i > \text{discountThreshold}, \\
    &\quad \text{apply discount}: \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i \cdot \left(1 - \frac{\text{materialDiscount}}{100}\right) \\
    &\text{Non-negativity Constraints:} \\
    & x_i \geq 0 \quad \text{and integer, for all } i = 1, 2, \ldots, N \\
    & z \geq 0 \quad \text{and integer}
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

\section*{Mathematical Model for the Company's Problem}

Define the decision variables:
\begin{align*}
    x_i & \text{ : number of units of product type } i \text{ produced, for } i = 1, 2, \ldots, N \\
    z   & \text{ : number of hours of overtime assembly labor scheduled}
\end{align*}

The objective is to maximize the daily profit, given by:
\[
\text{Maximize } \sum_{i=1}^{N} \left( \text{price}_i \cdot x_i - \text{materialCost}_i \cdot x_i \right) - \text{overtimeAssemblyCost} \cdot z
\]

Subject to the constraints:
\begin{align*}
    &\text{Assembly Labor Constraint:} \\
    & \sum_{i=1}^{N} \text{assemblyHour}_i \cdot x_i \leq \text{maxAssembly} + z \\
    &z \leq \text{maxOvertimeAssembly} \\
    &\text{Testing Constraint:} \\
    & \sum_{i=1}^{N} \text{testingHour}_i \cdot x_i \leq \text{maxTesting} \\
    &\text{Raw Material Discount Constraint (Only for Total Cost Calculation):} \\
    &\text{If } \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i > \text{discountThreshold}, \\
    &\quad \text{apply discount}: \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i \cdot \left(1 - \frac{\text{materialDiscount}}{100}\right) \\
    &\text{Non-negativity Constraints:} \\
    & x_i \geq 0 \quad \text{and integer, for all } i = 1, 2, \ldots, N \\
    & z \geq 0 \quad \text{and integer}
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

#### Number of product types
N = data['N']

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i+1}', lowBound=0, cat='Integer') for i in range(N)]
z = pulp.LpVariable('z', lowBound=0, cat='Integer')

#### Objective function
material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(N))
profit = pulp.lpSum((data['Price'][i] - data['MaterialCost'][i]) * x[i] for i in range(N)) - data['OvertimeAssemblyCost'] * z
problem += profit

#### Constraints

#### Assembly Labor Constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(N)) <= data['MaxAssembly'] + z

#### Overtime constraint
problem += z <= data['MaxOvertimeAssembly']

#### Testing Constraint
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(N)) <= data['MaxTesting']

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


