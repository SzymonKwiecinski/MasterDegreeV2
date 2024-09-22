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

Let:
\begin{itemize}
    \item $N$: Number of types of products
    \item $assemblyHour_i$: Assembly hours required for product $i$ (for $i=1, \ldots, N$)
    \item $testingHour_i$: Testing hours required for product $i$ (for $i=1, \ldots, N$)
    \item $materialCost_i$: Material cost for product $i$ (for $i=1, \ldots, N$)
    \item $maxAssembly$: Maximum assembly hours available per day
    \item $maxTesting$: Maximum testing hours available per day
    \item $price_i$: Selling price for product $i$ (for $i=1, \ldots, N$)
    \item $maxOvertimeAssembly$: Maximum allowed overtime assembly hours
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly
    \item $materialDiscount$: Discount percentage on materials if the bill exceeds the threshold
    \item $discountThreshold$: Threshold for material bill to qualify for discount
\end{itemize}

Define variables:
\begin{itemize}
    \item $x_i$: Number of units produced of product $i$ (for $i=1, \ldots, N$)
    \item $overtimeAssembly$: Hours of overtime assembly labor scheduled
    \item $materialBought$: Total amount spent on raw materials
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{dailyProfit} = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{materialBought} - (overtimeAssembly \cdot overtimeAssemblyCost)
\]

\subsection*{Subject to the following constraints}

1. Assembly hours constraint:
\[
\sum_{i=1}^{N} (assemblyHour_i \cdot x_i) + overtimeAssembly \leq maxAssembly + maxOvertimeAssembly
\]

2. Testing hours constraint:
\[
\sum_{i=1}^{N} (testingHour_i \cdot x_i) \leq maxTesting
\]

3. Material cost calculation:
\[
\text{materialBought} = \sum_{i=1}^{N} materialCost_i \cdot x_i
\]
If $\text{materialBought} > discountThreshold$:
\[
\text{materialBought} = \text{materialBought} \cdot (1 - \frac{materialDiscount}{100})
\]

4. Non-negativity constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, \ldots, N
\]
\[
overtimeAssembly \geq 0
\]

\subsection*{Output Variables}
The output will include:
\begin{itemize}
    \item \text{dailyProfit}: The optimal value of daily profit.
    \item \text{unitsProduced}: Vector $[x_1, x_2, \ldots, x_N]$ representing the units of each product produced.
    \item \text{overtimeAssembly}: The optimal number of overtime assembly hours scheduled.
    \item \text{materialBought}: The optimal amount of raw materials bought.
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

\section*{Mathematical Model for the Production Problem}

Let:
\begin{itemize}
    \item $N$: Number of types of products
    \item $assemblyHour_i$: Assembly hours required for product $i$ (for $i=1, \ldots, N$)
    \item $testingHour_i$: Testing hours required for product $i$ (for $i=1, \ldots, N$)
    \item $materialCost_i$: Material cost for product $i$ (for $i=1, \ldots, N$)
    \item $maxAssembly$: Maximum assembly hours available per day
    \item $maxTesting$: Maximum testing hours available per day
    \item $price_i$: Selling price for product $i$ (for $i=1, \ldots, N$)
    \item $maxOvertimeAssembly$: Maximum allowed overtime assembly hours
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly
    \item $materialDiscount$: Discount percentage on materials if the bill exceeds the threshold
    \item $discountThreshold$: Threshold for material bill to qualify for discount
\end{itemize}

Define variables:
\begin{itemize}
    \item $x_i$: Number of units produced of product $i$ (for $i=1, \ldots, N$)
    \item $overtimeAssembly$: Hours of overtime assembly labor scheduled
    \item $materialBought$: Total amount spent on raw materials
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{dailyProfit} = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{materialBought} - (overtimeAssembly \cdot overtimeAssemblyCost)
\]

\subsection*{Subject to the following constraints}

1. Assembly hours constraint:
\[
\sum_{i=1}^{N} (assemblyHour_i \cdot x_i) + overtimeAssembly \leq maxAssembly + maxOvertimeAssembly
\]

2. Testing hours constraint:
\[
\sum_{i=1}^{N} (testingHour_i \cdot x_i) \leq maxTesting
\]

3. Material cost calculation:
\[
\text{materialBought} = \sum_{i=1}^{N} materialCost_i \cdot x_i
\]
If $\text{materialBought} > discountThreshold$:
\[
\text{materialBought} = \text{materialBought} \cdot (1 - \frac{materialDiscount}{100})
\]

4. Non-negativity constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, \ldots, N
\]
\[
overtimeAssembly \geq 0
\]

\subsection*{Output Variables}
The output will include:
\begin{itemize}
    \item \text{dailyProfit}: The optimal value of daily profit.
    \item \text{unitsProduced}: Vector $[x_1, x_2, \ldots, x_N]$ representing the units of each product produced.
    \item \text{overtimeAssembly}: The optimal number of overtime assembly hours scheduled.
    \item \text{materialBought}: The optimal amount of raw materials bought.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

#### Model
problem = pulp.LpProblem("Production_Problem", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0)
materialBought = pulp.LpVariable("materialBought", lowBound=0)

#### Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - materialBought - (overtimeAssembly * data['OvertimeAssemblyCost'])
problem += profit

#### Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Hours_Constraint")
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Hours_Constraint")
problem += (materialBought == pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])), "Material_Cost_Calculation")

#### Discount constraint
discounted_material = materialBought * (1 - data['MaterialDiscount'] / 100)
problem += (pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) <= data['DiscountThreshold'], "No_Discount") \
           | (materialBought == discounted_material, "With_Discount")

#### Solve the problem
problem.solve()

#### Print the objective value and results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Units Produced: {[pulp.value(x[i]) for i in range(data["N"])]}')
print(f'Overtime Assembly: {pulp.value(overtimeAssembly)}')
print(f'Material Bought: {pulp.value(materialBought)}')
```

