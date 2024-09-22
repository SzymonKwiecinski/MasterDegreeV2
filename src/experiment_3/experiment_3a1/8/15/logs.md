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

Let:
\begin{itemize}
    \item \( N \): number of product types
    \item \( \text{assemblyHour}_i \): hours of assembly labor required for product \( i \)
    \item \( \text{testingHour}_i \): hours of testing required for product \( i \)
    \item \( \text{materialCost}_i \): cost of raw materials for product \( i \) (in dollars)
    \item \( \text{maxAssembly} \): maximum hours of assembly labor available (per day)
    \item \( \text{maxTesting} \): maximum hours of testing available (per day)
    \item \( \text{price}_i \): selling price of product \( i \) (in dollars)
    \item \( \text{maxOvertimeAssembly} \): maximum hours of overtime assembly labor available
    \item \( \text{overtimeAssemblyCost} \): cost per hour of overtime assembly labor
    \item \( \text{materialDiscount} \): percentage discount on materials if the daily bill exceeds the discount threshold
    \item \( \text{discountThreshold} \): threshold amount for receiving a material discount (in dollars)
\end{itemize}

Let:
\[
x_i \quad \text{= number of units of product } i \text{ produced}
\]
\[
o \quad \text{= number of hours of overtime assembly labor scheduled}
\]

\subsection*{Objective Function}
We want to maximize the daily profit, defined as:
\[
\text{dailyProfit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \left( \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) + \text{overtimeAssemblyCost} \cdot o \right)
\]

\subsection*{Constraints}
1. Assembly labor constraint:
\[
\sum_{i=1}^{N} (\text{assemblyHour}_i \cdot x_i) + o \leq \text{maxAssembly} + \text{maxOvertimeAssembly}
\]

2. Testing labor constraint:
\[
\sum_{i=1}^{N} (\text{testingHour}_i \cdot x_i) \leq \text{maxTesting}
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \forall i \in \{1, 2, \ldots, N\}
\]
\[
o \geq 0
\]

4. Material cost constraint for discount:
Let \( C \) be the total material cost:
\[
C = \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i)
\]
If \( C > \text{discountThreshold} \), the effective cost is reduced by \( \frac{\text{materialDiscount}}{100} \cdot C \).

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

Let:
\begin{itemize}
    \item \( N \): number of product types
    \item \( \text{assemblyHour}_i \): hours of assembly labor required for product \( i \)
    \item \( \text{testingHour}_i \): hours of testing required for product \( i \)
    \item \( \text{materialCost}_i \): cost of raw materials for product \( i \) (in dollars)
    \item \( \text{maxAssembly} \): maximum hours of assembly labor available (per day)
    \item \( \text{maxTesting} \): maximum hours of testing available (per day)
    \item \( \text{price}_i \): selling price of product \( i \) (in dollars)
    \item \( \text{maxOvertimeAssembly} \): maximum hours of overtime assembly labor available
    \item \( \text{overtimeAssemblyCost} \): cost per hour of overtime assembly labor
    \item \( \text{materialDiscount} \): percentage discount on materials if the daily bill exceeds the discount threshold
    \item \( \text{discountThreshold} \): threshold amount for receiving a material discount (in dollars)
\end{itemize}

Let:
\[
x_i \quad \text{= number of units of product } i \text{ produced}
\]
\[
o \quad \text{= number of hours of overtime assembly labor scheduled}
\]

\subsection*{Objective Function}
We want to maximize the daily profit, defined as:
\[
\text{dailyProfit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \left( \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i) + \text{overtimeAssemblyCost} \cdot o \right)
\]

\subsection*{Constraints}
1. Assembly labor constraint:
\[
\sum_{i=1}^{N} (\text{assemblyHour}_i \cdot x_i) + o \leq \text{maxAssembly} + \text{maxOvertimeAssembly}
\]

2. Testing labor constraint:
\[
\sum_{i=1}^{N} (\text{testingHour}_i \cdot x_i) \leq \text{maxTesting}
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \forall i \in \{1, 2, \ldots, N\}
\]
\[
o \geq 0
\]

4. Material cost constraint for discount:
Let \( C \) be the total material cost:
\[
C = \sum_{i=1}^{N} (\text{materialCost}_i \cdot x_i)
\]
If \( C > \text{discountThreshold} \), the effective cost is reduced by \( \frac{\text{materialDiscount}}{100} \cdot C \).

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
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
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

#### Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')
o = pulp.LpVariable("o", lowBound=0, cat='Continuous')

#### Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) \
         - (pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) + data['OvertimeAssemblyCost'] * o)

problem += profit

#### Constraints
#### 1. Assembly labor constraint
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + o 
            <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint")

#### 2. Testing labor constraint
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) 
            <= data['MaxTesting'], "Testing_Labor_Constraint")

#### 4. Material cost constraint for discount
C = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
discounted_C = C * (1 - data['MaterialDiscount'] / 100)

#### Add the material cost constraint if the discount threshold is crossed
problem += (C <= data['DiscountThreshold'] + 1e-5) | (discounted_C <= C)

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

