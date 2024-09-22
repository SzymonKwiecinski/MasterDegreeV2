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

\subsection*{Variables}
Define the following variables:
\begin{align*}
x_i & : \text{number of units produced of product } i, \quad i = 1, \ldots, N \\
h_{\text{overtime}} & : \text{overtime assembly hours scheduled} \\
\text{materialBought} & : \text{amount of raw materials bought}
\end{align*}

\subsection*{Parameters}
Let the following parameters be given:
\begin{align*}
\text{assemblyHour}_i & : \text{hours of assembly labor required for product } i \\
\text{testingHour}_i & : \text{hours of testing required for product } i \\
\text{materialCost}_i & : \text{cost of raw materials for product } i \\
\text{maxAssembly} & : \text{maximum available assembly hours per day} \\
\text{maxTesting} & : \text{maximum available testing hours per day} \\
\text{price}_i & : \text{selling price of product } i \\
\text{maxOvertimeAssembly} & : \text{maximum overtime assembly hours allowed} \\
\text{overtimeAssemblyCost} & : \text{cost per hour of overtime assembly labor} \\
\text{materialDiscount} & : \text{percentage discount on raw materials} \\
\text{discountThreshold} & : \text{threshold for material discount in dollars}
\end{align*}

\subsection*{Objective Function}
The objective is to maximize the daily profit:
\[
\text{maximize } Z = \sum_{i=1}^{N} \text{price}_i \cdot x_i - \left( \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i - \frac{\text{materialDiscount}}{100} \cdot \max(0, \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i - \text{discountThreshold}) \right) - \text{overtimeAssemblyCost} \cdot h_{\text{overtime}}
\]

\subsection*{Constraints}
1. Assembly hours constraint:
\[
\sum_{i=1}^{N} \text{assemblyHour}_i \cdot x_i + h_{\text{overtime}} \leq \text{maxAssembly} + \text{maxOvertimeAssembly}
\]

2. Testing hours constraint:
\[
\sum_{i=1}^{N} \text{testingHour}_i \cdot x_i \leq \text{maxTesting}
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, \ldots, N
\]
\[
h_{\text{overtime}} \geq 0
\]

\subsection*{Output Variables}
The output of the model will include:
\begin{align*}
\text{dailyProfit} & : Z \\
\text{unitsProduced}_i & : x_i \quad \text{for } i = 1, \ldots, N \\
\text{overtimeAssembly} & : h_{\text{overtime}} \\
\text{materialBought} & : \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i
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

\section*{Mathematical Model for Daily Profit Maximization}

\subsection*{Variables}
Define the following variables:
\begin{align*}
x_i & : \text{number of units produced of product } i, \quad i = 1, \ldots, N \\
h_{\text{overtime}} & : \text{overtime assembly hours scheduled} \\
\text{materialBought} & : \text{amount of raw materials bought}
\end{align*}

\subsection*{Parameters}
Let the following parameters be given:
\begin{align*}
\text{assemblyHour}_i & : \text{hours of assembly labor required for product } i \\
\text{testingHour}_i & : \text{hours of testing required for product } i \\
\text{materialCost}_i & : \text{cost of raw materials for product } i \\
\text{maxAssembly} & : \text{maximum available assembly hours per day} \\
\text{maxTesting} & : \text{maximum available testing hours per day} \\
\text{price}_i & : \text{selling price of product } i \\
\text{maxOvertimeAssembly} & : \text{maximum overtime assembly hours allowed} \\
\text{overtimeAssemblyCost} & : \text{cost per hour of overtime assembly labor} \\
\text{materialDiscount} & : \text{percentage discount on raw materials} \\
\text{discountThreshold} & : \text{threshold for material discount in dollars}
\end{align*}

\subsection*{Objective Function}
The objective is to maximize the daily profit:
\[
\text{maximize } Z = \sum_{i=1}^{N} \text{price}_i \cdot x_i - \left( \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i - \frac{\text{materialDiscount}}{100} \cdot \max(0, \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i - \text{discountThreshold}) \right) - \text{overtimeAssemblyCost} \cdot h_{\text{overtime}}
\]

\subsection*{Constraints}
1. Assembly hours constraint:
\[
\sum_{i=1}^{N} \text{assemblyHour}_i \cdot x_i + h_{\text{overtime}} \leq \text{maxAssembly} + \text{maxOvertimeAssembly}
\]

2. Testing hours constraint:
\[
\sum_{i=1}^{N} \text{testingHour}_i \cdot x_i \leq \text{maxTesting}
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, \ldots, N
\]
\[
h_{\text{overtime}} \geq 0
\]

\subsection*{Output Variables}
The output of the model will include:
\begin{align*}
\text{dailyProfit} & : Z \\
\text{unitsProduced}_i & : x_i \quad \text{for } i = 1, \ldots, N \\
\text{overtimeAssembly} & : h_{\text{overtime}} \\
\text{materialBought} & : \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 'DiscountThreshold': 300}

#### Create a linear programming problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
h_overtime = pulp.LpVariable('h_overtime', lowBound=0, cat='Continuous')

#### Objective Function
total_material_cost = sum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
material_discount_value = (data['MaterialDiscount']/100) * pulp.lpSum([pulp.lpSum([data['MaterialCost'][i] * x[i] for i in range(data['N'])]) - data['DiscountThreshold']])
effective_material_cost = total_material_cost - material_discount_value
revenue = sum(data['Price'][i] * x[i] for i in range(data['N']))

problem += revenue - effective_material_cost - data['OvertimeAssemblyCost'] * h_overtime

#### Constraints
#### Assembly hours constraint
problem += sum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + h_overtime <= data['MaxAssembly'] + data['MaxOvertimeAssembly']

#### Testing hours constraint
problem += sum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

#### Solve the problem
problem.solve()

#### Output Results
print(f'Daily Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(data['N']):
    print(f'Units produced of product {i+1}: {pulp.value(x[i])}')
print(f'Overtime Assembly Hours: {pulp.value(h_overtime)}')
material_cost_used = sum(data['MaterialCost'][i] * pulp.value(x[i]) for i in range(data['N']))
print(f'Material Bought: {material_cost_used}')
```


