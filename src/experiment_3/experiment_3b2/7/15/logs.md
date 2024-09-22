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
To solve this problem, we need to formulate it as a Mixed-Integer Linear Programming (MILP) model. We'll define decision variables, objective function, and constraints accordingly.

######### Decision Variables

- \( x_i \): Number of units of product \( i \) produced (integer, \( i = 1, \ldots, N \)).
- \( o \): Overtime assembly hours used (continuous, \( 0 \leq o \leq \text{maxOvertimeAssembly} \)).

######### Objective Function

Maximize the daily profit, which is total revenue minus total costs. The revenue is the sum of the product quantities multiplied by their respective prices. The costs include material costs (subject to discount), and overtime assembly labor costs.

######### Constraints

1. **Assembly Time Constraint**: The total hours required for assembly (including overtime) should not exceed the available regular and overtime hours.
2. **Testing Time Constraint**: The total hours required for testing should not exceed the maximum available testing hours.
3. **Material Cost for Discount**: Calculate material cost with and without discount based on total material cost surpassing the discount threshold.

Let's denote:
- \( A_i \) = \text{assemblyHour}_i
- \( T_i \) = \text{testingHour}_i
- \( M_i \) = \text{materialCost}_i
- \( P_i \) = \text{price}_i
- \( \text{discountFactor} = 1 - \frac{\text{materialDiscount}}{100} \)

######### Mathematical Model

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Maximize} \quad Z = \left( \sum_{i=1}^{N} P_i \times x_i \right) - \left( C_m + \text{overtimeAssemblyCost} \times o \right)
\]
Where:
\[
C_m = \begin{cases} 
\sum_{i=1}^{N} M_i \times x_i \cdot \text{discountFactor}, & \text{if } \sum_{i=1}^{N} M_i \times x_i \geq \text{discountThreshold} \\
\sum_{i=1}^{N} M_i \times x_i, & \text{otherwise}
\end{cases}
\]

\textbf{Subject to:}
\[
\sum_{i=1}^{N} A_i \times x_i \leq \text{maxAssembly} + o
\]
\[
\sum_{i=1}^{N} T_i \times x_i \leq \text{maxTesting}
\]
\[
0 \leq o \leq \text{maxOvertimeAssembly}
\]
\[
x_i \in \mathbb{Z}^+, \quad \text{for } i = 1, \ldots, N
\]

\textbf{Variables:}
\begin{align*}
x_i &: \text{units produced of product } i \\
o &: \text{overtime assembly hours used}
\end{align*}

\end{document}
```

This formulation captures all the given constraints and objective to maximize the profit. This problem can be solved using MILP solvers that handle integer and continuous variables efficiently.

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
\[
\text{Maximize} \quad Z = \left( \sum_{i=1}^{N} P_i \times x_i \right) - \left( C_m + \text{overtimeAssemblyCost} \times o \right)
\]
Where:
\[
C_m = \begin{cases} 
\sum_{i=1}^{N} M_i \times x_i \cdot \text{discountFactor}, & \text{if } \sum_{i=1}^{N} M_i \times x_i \geq \text{discountThreshold} \\
\sum_{i=1}^{N} M_i \times x_i, & \text{otherwise}
\end{cases}
\]

\textbf{Subject to:}
\[
\sum_{i=1}^{N} A_i \times x_i \leq \text{maxAssembly} + o
\]
\[
\sum_{i=1}^{N} T_i \times x_i \leq \text{maxTesting}
\]
\[
0 \leq o \leq \text{maxOvertimeAssembly}
\]
\[
x_i \in \mathbb{Z}^+, \quad \text{for } i = 1, \ldots, N
\]

\textbf{Variables:}
\begin{align*}
x_i &: \text{units produced of product } i \\
o &: \text{overtime assembly hours used}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

#### Parameters
N = data['N']
A = data['AssemblyHour']
T = data['TestingHour']
M = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
P = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
o = pulp.LpVariable("o", lowBound=0, upBound=max_overtime_assembly)

#### Objective function
C_m = pulp.lpSum(M[i] * x[i] for i in range(N))
discounted_C_m = pulp.lpSum(M[i] * x[i] * (1 - material_discount / 100) for i in range(N))

C_m_expr = pulp.If(C_m >= discount_threshold, discounted_C_m, C_m)

Z = pulp.lpSum(P[i] * x[i] for i in range(N)) - (C_m_expr + overtime_assembly_cost * o)
problem += Z, "Objective"

#### Constraints
problem += pulp.lpSum(A[i] * x[i] for i in range(N)) <= max_assembly + o, "Assembly_Constraint"
problem += pulp.lpSum(T[i] * x[i] for i in range(N)) <= max_testing, "Testing_Constraint"

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

#### Data input
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

#### Parameters
N = data['N']
A = data['AssemblyHour']
T = data['TestingHour']
M = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
P = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
o = pulp.LpVariable("o", lowBound=0, upBound=max_overtime_assembly)

#### Objective function
C_m = pulp.lpSum(M[i] * x[i] for i in range(N))
discounted_C_m = pulp.lpSum(M[i] * x[i] * (1 - material_discount / 100) for i in range(N))

C_m_expr = pulp.If(C_m >= discount_threshold, discounted_C_m, C_m)

Z = pulp.lpSum(P[i] * x[i] for i in range(N)) - (C_m_expr + overtime_assembly_cost * o)
problem += Z, "Objective"

#### Constraints
problem += pulp.lpSum(A[i] * x[i] for i in range(N)) <= max_assembly + o, "Assembly_Constraint"
problem += pulp.lpSum(T[i] * x[i] for i in range(N)) <= max_testing, "Testing_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b2/7/15/python_code0.py", line 31, in <module>
    C_m_expr = pulp.If(C_m >= discount_threshold, discounted_C_m, C_m)
               ^^^^^^^
AttributeError: module 'pulp' has no attribute 'If'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

#### Parameters
N = data['N']
A = data['AssemblyHour']
T = data['TestingHour']
M = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
P = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
o = pulp.LpVariable("o", lowBound=0, upBound=max_overtime_assembly)

#### Objective function
C_m = pulp.lpSum(M[i] * x[i] for i in range(N))
discounted_C_m = pulp.lpSum(M[i] * x[i] * (1 - material_discount / 100) for i in range(N))

#### Use a conditional check for the objective function
C_m_expr = C_m - (discounted_C_m - C_m) * pulp.lpSum((C_m < discount_threshold))

Z = pulp.lpSum(P[i] * x[i] for i in range(N)) - (C_m_expr + overtime_assembly_cost * o)
problem += Z, "Objective"

#### Constraints
problem += pulp.lpSum(A[i] * x[i] for i in range(N)) <= max_assembly + o, "Assembly_Constraint"
problem += pulp.lpSum(T[i] * x[i] for i in range(N)) <= max_testing, "Testing_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

