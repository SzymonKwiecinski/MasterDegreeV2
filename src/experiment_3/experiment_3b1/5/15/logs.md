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

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item \( N \): Number of product types
    \item \( \text{assemblyHour}_i \): Hours of assembly labor required for product \( i \)
    \item \( \text{testingHour}_i \): Hours of testing required for product \( i \)
    \item \( \text{materialCost}_i \): Cost of raw materials for product \( i \) (in dollars)
    \item \( \text{maxAssembly} \): Maximum hours of assembly labor available per day
    \item \( \text{maxTesting} \): Maximum hours of testing available per day
    \item \( \text{price}_i \): Selling price of product \( i \) (in dollars)
    \item \( \text{maxOvertimeAssembly} \): Maximum hours of overtime assembly labor available
    \item \( \text{overtimeAssemblyCost} \): Cost per hour of overtime assembly labor
    \item \( \text{materialDiscount} \): Discount percentage on materials if daily bill exceeds threshold
    \item \( \text{discountThreshold} \): Threshold for material discount (in dollars)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_i \): Number of units of product \( i \) produced
    \item \( y \): Number of hours of overtime assembly labor scheduled
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{dailyProfit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \left( \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) - \text{materialDiscount} \cdot \mathbb{1}\{ \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) > \text{discountThreshold} \} \cdot \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) \right) - ( \text{overtimeAssemblyCost} \cdot y )
\]

\subsection*{Constraints}
\begin{align}
    \text{Assembly Labor Constraint:} \quad & \sum_{i=1}^{N} (\text{assemblyHour}_i \cdot x_i) + y \leq \text{maxAssembly} + \text{maxOvertimeAssembly} \\
    \text{Testing Labor Constraint:} \quad & \sum_{i=1}^{N} (\text{testingHour}_i \cdot x_i) \leq \text{maxTesting} \\
    \text{Non-negativity Constraint:} \quad & x_i \geq 0, \quad \forall i = 1, \ldots, N \\
    \text{Overtime Non-negativity Constraint:} \quad & y \geq 0
\end{align}

\subsection*{Output Variables}
\begin{itemize}
    \item \text{dailyProfit}: Daily profit of the company
    \item \( x_i \): Units produced of product \( i \)
    \item \( y \): Overtime assembly hours scheduled
    \item \text{materialBought}: Total amount of raw materials bought given by \( \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) \)
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

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item \( N \): Number of product types
    \item \( \text{assemblyHour}_i \): Hours of assembly labor required for product \( i \)
    \item \( \text{testingHour}_i \): Hours of testing required for product \( i \)
    \item \( \text{materialCost}_i \): Cost of raw materials for product \( i \) (in dollars)
    \item \( \text{maxAssembly} \): Maximum hours of assembly labor available per day
    \item \( \text{maxTesting} \): Maximum hours of testing available per day
    \item \( \text{price}_i \): Selling price of product \( i \) (in dollars)
    \item \( \text{maxOvertimeAssembly} \): Maximum hours of overtime assembly labor available
    \item \( \text{overtimeAssemblyCost} \): Cost per hour of overtime assembly labor
    \item \( \text{materialDiscount} \): Discount percentage on materials if daily bill exceeds threshold
    \item \( \text{discountThreshold} \): Threshold for material discount (in dollars)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_i \): Number of units of product \( i \) produced
    \item \( y \): Number of hours of overtime assembly labor scheduled
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{dailyProfit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \left( \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) - \text{materialDiscount} \cdot \mathbb{1}\{ \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) > \text{discountThreshold} \} \cdot \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) \right) - ( \text{overtimeAssemblyCost} \cdot y )
\]

\subsection*{Constraints}
\begin{align}
    \text{Assembly Labor Constraint:} \quad & \sum_{i=1}^{N} (\text{assemblyHour}_i \cdot x_i) + y \leq \text{maxAssembly} + \text{maxOvertimeAssembly} \\
    \text{Testing Labor Constraint:} \quad & \sum_{i=1}^{N} (\text{testingHour}_i \cdot x_i) \leq \text{maxTesting} \\
    \text{Non-negativity Constraint:} \quad & x_i \geq 0, \quad \forall i = 1, \ldots, N \\
    \text{Overtime Non-negativity Constraint:} \quad & y \geq 0
\end{align}

\subsection*{Output Variables}
\begin{itemize}
    \item \text{dailyProfit}: Daily profit of the company
    \item \( x_i \): Units produced of product \( i \)
    \item \( y \): Overtime assembly hours scheduled
    \item \text{materialBought}: Total amount of raw materials bought given by \( \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {'N': 2, 
        'AssemblyHour': [0.25, 0.3333], 
        'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 
        'MaxTesting': 70, 
        'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 
        'DiscountThreshold': 300}

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0)

#### Objective function
daily_profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - \
    (pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) - 
     (data['MaterialDiscount'] / 100) * pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) 
     * pulp.lpIndicator(pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) > data['DiscountThreshold'])) - \
    (data['OvertimeAssemblyCost'] * y)

problem += daily_profit

#### Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <= data['MaxAssembly'] + data['MaxOvertimeAssembly']
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

#### Solve the problem
problem.solve()

#### Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(data['N']):
    print(f'Units produced for product {i+1}: {pulp.value(x[i])}')
print(f'Overtime hours scheduled: {pulp.value(y)}')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
```python
import pulp

#### Data from the JSON format
data = {'N': 2, 
        'AssemblyHour': [0.25, 0.3333], 
        'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 
        'MaxTesting': 70, 
        'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 
        'DiscountThreshold': 300}

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0)

#### Objective function
daily_profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - \
    (pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) - 
     (data['MaterialDiscount'] / 100) * pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) 
     * pulp.lpIndicator(pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) > data['DiscountThreshold'])) - \
    (data['OvertimeAssemblyCost'] * y)

problem += daily_profit

#### Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <= data['MaxAssembly'] + data['MaxOvertimeAssembly']
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

#### Solve the problem
problem.solve()

#### Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(data['N']):
    print(f'Units produced for product {i+1}: {pulp.value(x[i])}')
print(f'Overtime hours scheduled: {pulp.value(y)}')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/5/15/python_code0.py", line 27, in <module>
    * pulp.lpIndicator(pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) > data['DiscountThreshold'])) - \
      ^^^^^^^^^^^^^^^^
AttributeError: module 'pulp' has no attribute 'lpIndicator'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {'N': 2, 
        'AssemblyHour': [0.25, 0.3333], 
        'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 
        'MaxTesting': 70, 
        'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 
        'DiscountThreshold': 300}

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0)

#### Objective function
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
daily_profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - \
    (total_material_cost - 
     (data['MaterialDiscount'] / 100) * total_material_cost 
     * pulp.lpSum(1 if total_material_cost > data['DiscountThreshold'] else 0) ) - \
    (data['OvertimeAssemblyCost'] * y)

problem += daily_profit

#### Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <= data['MaxAssembly'] + data['MaxOvertimeAssembly']
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

#### Solve the problem
problem.solve()

#### Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(data['N']):
    print(f'Units produced for product {i+1}: {pulp.value(x[i])}')
print(f'Overtime hours scheduled: {pulp.value(y)}')
```

