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

\title{Mathematical Model for Production Optimization}
\author{}
\date{}
\maketitle

\section*{Problem Description}

Let \( N \) be the number of different product types produced by the company. For each product \( i \) (where \( i = 1, \ldots, N \)), the following parameters are defined:

\begin{itemize}
    \item \( \text{assemblyHour}_i \): hours of assembly labor required for product \( i \)
    \item \( \text{testingHour}_i \): hours of testing required for product \( i \)
    \item \( \text{materialCost}_i \): cost of raw materials for product \( i \) (in dollars)
    \item \( \text{price}_i \): selling price of product \( i \) (in dollars)
\end{itemize}

Additionally, the following constraints are given:

\begin{itemize}
    \item Maximum hours of assembly labor per day: \( \text{maxAssembly} \)
    \item Maximum hours of testing per day: \( \text{maxTesting} \)
    \item Maximum overtime assembly hours: \( \text{maxOvertimeAssembly} \)
    \item Overtime assembly cost per hour: \( \text{overtimeAssemblyCost} \)
    \item Material discount percentage: \( \text{materialDiscount} \)
    \item Discount threshold: \( \text{discountThreshold} \)
\end{itemize}

\section*{Decision Variables}

Let:
\begin{itemize}
    \item \( x_i \): number of units produced of product \( i \)
    \item \( y \): hours of overtime assembly labor scheduled
\end{itemize}

The total amount of raw materials bought can be represented as:
\[
\text{materialBought} = \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i
\]

\section*{Objective Function}

The objective is to maximize the daily profit, defined as:

\[
\text{dailyProfit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i - \left( \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i \cdot \left(1 - \frac{\text{materialDiscount}}{100}\right) + y \cdot \text{overtimeAssemblyCost} \right)
\]

\section*{Constraints}

1. Total assembly hours used must not exceed the maximum available hours:
\[
\sum_{i=1}^{N} \text{assemblyHour}_i \cdot x_i + y \leq \text{maxAssembly} + \text{maxOvertimeAssembly}
\]

2. Total testing hours must not exceed the maximum available hours:
\[
\sum_{i=1}^{N} \text{testingHour}_i \cdot x_i \leq \text{maxTesting}
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \forall i = 1, \ldots, N 
\]
\[
y \geq 0
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

\title{Mathematical Model for Production Optimization}
\author{}
\date{}
\maketitle

\section*{Problem Description}

Let \( N \) be the number of different product types produced by the company. For each product \( i \) (where \( i = 1, \ldots, N \)), the following parameters are defined:

\begin{itemize}
    \item \( \text{assemblyHour}_i \): hours of assembly labor required for product \( i \)
    \item \( \text{testingHour}_i \): hours of testing required for product \( i \)
    \item \( \text{materialCost}_i \): cost of raw materials for product \( i \) (in dollars)
    \item \( \text{price}_i \): selling price of product \( i \) (in dollars)
\end{itemize}

Additionally, the following constraints are given:

\begin{itemize}
    \item Maximum hours of assembly labor per day: \( \text{maxAssembly} \)
    \item Maximum hours of testing per day: \( \text{maxTesting} \)
    \item Maximum overtime assembly hours: \( \text{maxOvertimeAssembly} \)
    \item Overtime assembly cost per hour: \( \text{overtimeAssemblyCost} \)
    \item Material discount percentage: \( \text{materialDiscount} \)
    \item Discount threshold: \( \text{discountThreshold} \)
\end{itemize}

\section*{Decision Variables}

Let:
\begin{itemize}
    \item \( x_i \): number of units produced of product \( i \)
    \item \( y \): hours of overtime assembly labor scheduled
\end{itemize}

The total amount of raw materials bought can be represented as:
\[
\text{materialBought} = \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i
\]

\section*{Objective Function}

The objective is to maximize the daily profit, defined as:

\[
\text{dailyProfit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i - \left( \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i \cdot \left(1 - \frac{\text{materialDiscount}}{100}\right) + y \cdot \text{overtimeAssemblyCost} \right)
\]

\section*{Constraints}

1. Total assembly hours used must not exceed the maximum available hours:
\[
\sum_{i=1}^{N} \text{assemblyHour}_i \cdot x_i + y \leq \text{maxAssembly} + \text{maxOvertimeAssembly}
\]

2. Total testing hours must not exceed the maximum available hours:
\[
\sum_{i=1}^{N} \text{testingHour}_i \cdot x_i \leq \text{maxTesting}
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \forall i = 1, \ldots, N 
\]
\[
y \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')

#### Objective Function
material_discount_factor = 1 - data['MaterialDiscount'] / 100
daily_profit = (
    pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) -
    pulp.lpSum(data['MaterialCost'][i] * x[i] * material_discount_factor for i in range(data['N'])) -
    y * data['OvertimeAssemblyCost']
)
problem += daily_profit

#### Constraints
#### Total assembly hours
problem += (
    pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <=
    data['MaxAssembly'] + data['MaxOvertimeAssembly']
)

#### Total testing hours
problem += (
    pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']
)

#### Solve
problem.solve()

#### Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

