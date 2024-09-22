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

\section*{Mathematical Model for Production Optimization}

\subsection*{Indices}
\begin{itemize}
    \item $i \in \{1, \ldots, N\}$: index for the types of products
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $assemblyHour_i$: hours of assembly labor required for product $i$
    \item $testingHour_i$: hours of testing required for product $i$
    \item $materialCost_i$: cost of raw materials for product $i$ (in \$)
    \item $maxAssembly$: maximum hours of assembly labor available per day
    \item $maxTesting$: maximum hours of testing available per day
    \item $price_i$: selling price of product $i$ (in \$)
    \item $maxOvertimeAssembly$: maximum hours of overtime assembly labor that can be scheduled
    \item $overtimeAssemblyCost$: cost per hour of overtime assembly labor (in \$)
    \item $materialDiscount$: percentage discount on material cost if daily bill exceeds threshold
    \item $discountThreshold$: threshold for material discount (in \$)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $unitsProduced_i$: number of units of product $i$ produced
    \item $overtimeAssembly$: number of hours of overtime assembly labor scheduled
    \item $materialBought$: total amount of raw materials bought (in \$)
\end{itemize}

\subsection*{Objective Function}
We want to maximize the daily profit of the company:
\[
\text{Maximize } Z = \sum_{i=1}^{N} (price_i \cdot unitsProduced_i) - \text{Total Cost}
\]
where
\[
\text{Total Cost} = \sum_{i=1}^{N} (materialCost_i \cdot unitsProduced_i) + 
\begin{cases} 
0 & \text{if } \sum_{i=1}^{N} (materialCost_i \cdot unitsProduced_i) \leq discountThreshold \\
(1 - \frac{materialDiscount}{100}) \cdot \sum_{i=1}^{N} (materialCost_i \cdot unitsProduced_i) & \text{otherwise} 
\end{cases}
+ overtimeAssemblyCost \cdot overtimeAssembly
\]

\subsection*{Constraints}
1. Assembly labor constraint:
\[
\sum_{i=1}^{N} (assemblyHour_i \cdot unitsProduced_i) + overtimeAssembly \leq maxAssembly + maxOvertimeAssembly
\]

2. Testing labor constraint:
\[
\sum_{i=1}^{N} (testingHour_i \cdot unitsProduced_i) \leq maxTesting
\]

3. Non-negativity constraints:
\[
unitsProduced_i \geq 0 \quad \forall i, \quad overtimeAssembly \geq 0, \quad materialBought \geq 0
\]

\subsection*{Output Representation}
The results of the optimization will be represented as follows:
\[
\text{Output} = 
\begin{cases}
\text{dailyProfit} = Z \\
\text{unitsProduced} = [unitsProduced_1, ..., unitsProduced_N] \\
\text{overtimeAssembly} = overtimeAssembly \\
\text{materialBought} = materialBought
\end{cases}
\]

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

\section*{Mathematical Model for Production Optimization}

\subsection*{Indices}
\begin{itemize}
    \item $i \in \{1, \ldots, N\}$: index for the types of products
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $assemblyHour_i$: hours of assembly labor required for product $i$
    \item $testingHour_i$: hours of testing required for product $i$
    \item $materialCost_i$: cost of raw materials for product $i$ (in \$)
    \item $maxAssembly$: maximum hours of assembly labor available per day
    \item $maxTesting$: maximum hours of testing available per day
    \item $price_i$: selling price of product $i$ (in \$)
    \item $maxOvertimeAssembly$: maximum hours of overtime assembly labor that can be scheduled
    \item $overtimeAssemblyCost$: cost per hour of overtime assembly labor (in \$)
    \item $materialDiscount$: percentage discount on material cost if daily bill exceeds threshold
    \item $discountThreshold$: threshold for material discount (in \$)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $unitsProduced_i$: number of units of product $i$ produced
    \item $overtimeAssembly$: number of hours of overtime assembly labor scheduled
    \item $materialBought$: total amount of raw materials bought (in \$)
\end{itemize}

\subsection*{Objective Function}
We want to maximize the daily profit of the company:
\[
\text{Maximize } Z = \sum_{i=1}^{N} (price_i \cdot unitsProduced_i) - \text{Total Cost}
\]
where
\[
\text{Total Cost} = \sum_{i=1}^{N} (materialCost_i \cdot unitsProduced_i) + 
\begin{cases} 
0 & \text{if } \sum_{i=1}^{N} (materialCost_i \cdot unitsProduced_i) \leq discountThreshold \\
(1 - \frac{materialDiscount}{100}) \cdot \sum_{i=1}^{N} (materialCost_i \cdot unitsProduced_i) & \text{otherwise} 
\end{cases}
+ overtimeAssemblyCost \cdot overtimeAssembly
\]

\subsection*{Constraints}
1. Assembly labor constraint:
\[
\sum_{i=1}^{N} (assemblyHour_i \cdot unitsProduced_i) + overtimeAssembly \leq maxAssembly + maxOvertimeAssembly
\]

2. Testing labor constraint:
\[
\sum_{i=1}^{N} (testingHour_i \cdot unitsProduced_i) \leq maxTesting
\]

3. Non-negativity constraints:
\[
unitsProduced_i \geq 0 \quad \forall i, \quad overtimeAssembly \geq 0, \quad materialBought \geq 0
\]

\subsection*{Output Representation}
The results of the optimization will be represented as follows:
\[
\text{Output} = 
\begin{cases}
\text{dailyProfit} = Z \\
\text{unitsProduced} = [unitsProduced_1, ..., unitsProduced_N] \\
\text{overtimeAssembly} = overtimeAssembly \\
\text{materialBought} = materialBought
\end{cases}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided
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

#### Create a Linear Programming problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i+1}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Continuous')
materialBought = pulp.LpVariable('materialBought', lowBound=0, cat='Continuous')

#### Objective Function
total_revenue = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N']))
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
material_cost_after_discount = (total_material_cost * (1 - data['MaterialDiscount'] / 100) 
                                 if total_material_cost > data['DiscountThreshold'] 
                                 else total_material_cost)

total_cost = material_cost_after_discount + (data['OvertimeAssemblyCost'] * overtimeAssembly)

problem += total_revenue - total_cost, "Total_Profit"

#### Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) 
             + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], 
             "Assembly_Labor_Constraint")

problem += (pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) 
             <= data['MaxTesting'], 
             "Testing_Labor_Constraint")

#### Solve the problem
problem.solve()

#### Output results
daily_profit = pulp.value(problem.objective)
units_produced_values = [pulp.value(unitsProduced[i]) for i in range(data['N'])]
print(f' (Objective Value): <OBJ>{daily_profit}</OBJ>')
print(f'Units Produced: {units_produced_values}')
print(f'Overtime Assembly: {pulp.value(overtimeAssembly)}')
print(f'Material Bought: {pulp.value(materialBought)}')
```

