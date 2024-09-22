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

\section*{Mathematical Model for the Production Problem}

\subsection*{Sets and Parameters}
\begin{align*}
& N: \text{Number of product types} \\
& \text{assemblyHour}_i: \text{Hours of assembly labor required for product } i \quad \forall i \in \{1, 2, \ldots, N\} \\
& \text{testingHour}_i: \text{Hours of testing required for product } i \quad \forall i \in \{1, 2, \ldots, N\} \\
& \text{materialCost}_i: \text{Cost of raw materials for product } i \quad \forall i \in \{1, 2, \ldots, N\} \\
& \text{maxAssembly}: \text{Maximum assembly hours available} \\
& \text{maxTesting}: \text{Maximum testing hours available} \\
& \text{price}_i: \text{Selling price of product } i \quad \forall i \in \{1, 2, \ldots, N\} \\
& \text{maxOvertimeAssembly}: \text{Maximum hours of overtime assembly available} \\
& \text{overtimeAssemblyCost}: \text{Cost per hour of overtime assembly} \\
& \text{materialDiscount}: \text{Discount on materials (in percent)} \\
& \text{discountThreshold}: \text{Threshold for material discount} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& x_i: \text{Units of product } i \text{ produced} \quad \forall i \in \{1, 2, \ldots, N\} \\
& y: \text{Hours of overtime assembly scheduled} \\
\end{align*}

\subsection*{Objective Function}
Maximize the daily profit:
\begin{align*}
\text{dailyProfit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \left( \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) + \text{overtimeAssemblyCost} \cdot y - \text{discount} \right)
\end{align*}
where
\begin{align*}
\text{discount} =
\begin{cases}
\frac{\text{materialDiscount}}{100} \cdot \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) & \text{if } \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) > \text{discountThreshold} \\
0 & \text{otherwise}
\end{cases}
\end{align*}

\subsection*{Constraints}
\begin{align*}
\sum_{i=1}^{N} (\text{assemblyHour}_i \cdot x_i) + y & \leq \text{maxAssembly} + \text{maxOvertimeAssembly} \\
\sum_{i=1}^{N} (\text{testingHour}_i \cdot x_i) & \leq \text{maxTesting} \\
x_i & \geq 0 \quad \forall i \in \{1, 2, \ldots, N\} \\
y & \geq 0 \\
y & \leq \text{maxOvertimeAssembly} \\
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

\section*{Mathematical Model for the Production Problem}

\subsection*{Sets and Parameters}
\begin{align*}
& N: \text{Number of product types} \\
& \text{assemblyHour}_i: \text{Hours of assembly labor required for product } i \quad \forall i \in \{1, 2, \ldots, N\} \\
& \text{testingHour}_i: \text{Hours of testing required for product } i \quad \forall i \in \{1, 2, \ldots, N\} \\
& \text{materialCost}_i: \text{Cost of raw materials for product } i \quad \forall i \in \{1, 2, \ldots, N\} \\
& \text{maxAssembly}: \text{Maximum assembly hours available} \\
& \text{maxTesting}: \text{Maximum testing hours available} \\
& \text{price}_i: \text{Selling price of product } i \quad \forall i \in \{1, 2, \ldots, N\} \\
& \text{maxOvertimeAssembly}: \text{Maximum hours of overtime assembly available} \\
& \text{overtimeAssemblyCost}: \text{Cost per hour of overtime assembly} \\
& \text{materialDiscount}: \text{Discount on materials (in percent)} \\
& \text{discountThreshold}: \text{Threshold for material discount} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& x_i: \text{Units of product } i \text{ produced} \quad \forall i \in \{1, 2, \ldots, N\} \\
& y: \text{Hours of overtime assembly scheduled} \\
\end{align*}

\subsection*{Objective Function}
Maximize the daily profit:
\begin{align*}
\text{dailyProfit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \left( \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) + \text{overtimeAssemblyCost} \cdot y - \text{discount} \right)
\end{align*}
where
\begin{align*}
\text{discount} =
\begin{cases}
\frac{\text{materialDiscount}}{100} \cdot \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) & \text{if } \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) > \text{discountThreshold} \\
0 & \text{otherwise}
\end{cases}
\end{align*}

\subsection*{Constraints}
\begin{align*}
\sum_{i=1}^{N} (\text{assemblyHour}_i \cdot x_i) + y & \leq \text{maxAssembly} + \text{maxOvertimeAssembly} \\
\sum_{i=1}^{N} (\text{testingHour}_i \cdot x_i) & \leq \text{maxTesting} \\
x_i & \geq 0 \quad \forall i \in \{1, 2, \ldots, N\} \\
y & \geq 0 \\
y & \leq \text{maxOvertimeAssembly} \\
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input in JSON format
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

#### Parameters
N = data['N']
assemblyHour = data['AssemblyHour']
testingHour = data['TestingHour']
materialCost = data['MaterialCost']
maxAssembly = data['MaxAssembly']
maxTesting = data['MaxTesting']
price = data['Price']
maxOvertimeAssembly = data['MaxOvertimeAssembly']
overtimeAssemblyCost = data['OvertimeAssemblyCost']
materialDiscount = data['MaterialDiscount']
discountThreshold = data['DiscountThreshold']

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Continuous')  #### Units of product
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')  #### Overtime hours

#### Problem
problem = pulp.LpProblem("Production_Problem", pulp.LpMaximize)

#### Objective Function
discount_expr = pulp.lpSum(materialCost[i] * x[i] for i in range(N)) > discountThreshold

#### Set the objective
problem += (pulp.lpSum(price[i] * x[i] for i in range(N)) - 
             (pulp.lpSum(materialCost[i] * x[i] for i in range(N)) + 
              overtimeAssemblyCost * y - 
              pulp.lpSum((materialDiscount / 100.0) * materialCost[i] * x[i] for i in range(N) if discount_expr)))

#### Constraints
problem += (pulp.lpSum(assemblyHour[i] * x[i] for i in range(N)) + y <= maxAssembly + maxOvertimeAssembly, "Assembly_Hours_Constraint")
problem += (pulp.lpSum(testingHour[i] * x[i] for i in range(N)) <= maxTesting, "Testing_Hours_Constraint")
problem += (y <= maxOvertimeAssembly, "Max_Overtime_Assembly")

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

