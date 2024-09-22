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
To model this problem as a Mixed-Integer Linear Program (MILP) and maximize the daily profit, we will introduce decision variables and constraints that represent the resources and operations of the company. Here is how the mathematical model is constructed:

**Decision Variables:**
- \( x_i \): Number of units of product \( i \) produced. (integer)
- \( y \): Overtime assembly labor hours scheduled. (integer)

**Parameters:**
- \( \text{assemblyHour}_i \): Hours of assembly required for one unit of product \( i \).
- \( \text{testingHour}_i \): Hours of testing required for one unit of product \( i \).
- \( \text{materialCost}_i \): Cost of materials for one unit of product \( i \).
- \( \text{price}_i \): Selling price for one unit of product \( i \).
- \( \text{maxAssembly} \): Maximum regular assembly labor hours available.
- \( \text{maxTesting} \): Maximum testing labor hours available.
- \( \text{maxOvertimeAssembly} \): Maximum overtime assembly labor hours.
- \( \text{overtimeAssemblyCost} \): Cost per hour for overtime assembly labor.
- \( \text{materialDiscount} \): Discount percentage on raw materials if eligible.
- \( \text{discountThreshold} \): Threshold for material cost to get a discount.

**Objective:**
Maximize the daily profit, which is total revenue minus total costs (assembly, testing, and materials).

**Constraints:**
1. Assembly labor constraint: Sum of assembly hours (including overtime) should not exceed available hours.
2. Testing labor constraint: Sum of testing hours should not exceed available hours.
3. Overtime hours constraint.
4. Material cost calculation including potential discount.

Here's the LaTeX code for the MILP formulation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Formulation for Maximizing Daily Profit}

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Number of units of product } i \text{ produced} \\
y & : \text{Overtime assembly labor hours scheduled}
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{assemblyHour}_i & : \text{Hours of assembly required for one unit of product } i \\
\text{testingHour}_i & : \text{Hours of testing required for one unit of product } i \\
\text{materialCost}_i & : \text{Cost of materials for one unit of product } i \\
\text{price}_i & : \text{Selling price for one unit of product } i \\
\text{maxAssembly} & : \text{Maximum regular assembly labor hours available} \\
\text{maxTesting} & : \text{Maximum testing labor hours available} \\
\text{maxOvertimeAssembly} & : \text{Maximum overtime assembly labor hours} \\
\text{overtimeAssemblyCost} & : \text{Cost per hour for overtime assembly labor} \\
\text{materialDiscount} & : \text{Discount percentage on raw materials if eligible} \\
\text{discountThreshold} & : \text{Threshold for material cost to get a discount} \\
N & : \text{Number of product types}
\end{align*}

\subsection*{Objective}
Maximize the daily profit:
\begin{align*}
\text{Profit} = \sum_{i=1}^{N} \left( \text{price}_i \cdot x_i \right) - \left( \text{overtimeAssemblyCost} \cdot y \right) - \text{Material Cost}
\end{align*}

\subsection*{Constraints}
\begin{align}
\sum_{i=1}^{N} \left(\text{assemblyHour}_i \cdot x_i\right) & \leq \text{maxAssembly} + y, \label{assembly} \\
\sum_{i=1}^{N} \left(\text{testingHour}_i \cdot x_i\right) & \leq \text{maxTesting}, \label{testing} \\
0 \leq y & \leq \text{maxOvertimeAssembly}, \label{overtime} \\
\text{Material Cost} = 
\begin{cases} 
\sum_{i=1}^{N} \left(\text{materialCost}_i \cdot x_i\right), & \text{if } \sum_{i=1}^{N} \left(\text{materialCost}_i \cdot x_i\right) \leq \text{discountThreshold} \\
(1 - \frac{\text{materialDiscount}}{100}) \cdot \sum_{i=1}^{N} \left(\text{materialCost}_i \cdot x_i\right), & \text{otherwise}
\end{cases} \label{material_cost}
\end{align}

\end{document}
```

This modeling covers the constraints and objectives, and can be solved using MILP solvers to determine the optimal production plan.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Formulation for Maximizing Daily Profit}

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Number of units of product } i \text{ produced} \\
y & : \text{Overtime assembly labor hours scheduled}
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{assemblyHour}_i & : \text{Hours of assembly required for one unit of product } i \\
\text{testingHour}_i & : \text{Hours of testing required for one unit of product } i \\
\text{materialCost}_i & : \text{Cost of materials for one unit of product } i \\
\text{price}_i & : \text{Selling price for one unit of product } i \\
\text{maxAssembly} & : \text{Maximum regular assembly labor hours available} \\
\text{maxTesting} & : \text{Maximum testing labor hours available} \\
\text{maxOvertimeAssembly} & : \text{Maximum overtime assembly labor hours} \\
\text{overtimeAssemblyCost} & : \text{Cost per hour for overtime assembly labor} \\
\text{materialDiscount} & : \text{Discount percentage on raw materials if eligible} \\
\text{discountThreshold} & : \text{Threshold for material cost to get a discount} \\
N & : \text{Number of product types}
\end{align*}

\subsection*{Objective}
Maximize the daily profit:
\begin{align*}
\text{Profit} = \sum_{i=1}^{N} \left( \text{price}_i \cdot x_i \right) - \left( \text{overtimeAssemblyCost} \cdot y \right) - \text{Material Cost}
\end{align*}

\subsection*{Constraints}
\begin{align}
\sum_{i=1}^{N} \left(\text{assemblyHour}_i \cdot x_i\right) & \leq \text{maxAssembly} + y, \label{assembly} \\
\sum_{i=1}^{N} \left(\text{testingHour}_i \cdot x_i\right) & \leq \text{maxTesting}, \label{testing} \\
0 \leq y & \leq \text{maxOvertimeAssembly}, \label{overtime} \\
\text{Material Cost} = 
\begin{cases} 
\sum_{i=1}^{N} \left(\text{materialCost}_i \cdot x_i\right), & \text{if } \sum_{i=1}^{N} \left(\text{materialCost}_i \cdot x_i\right) \leq \text{discountThreshold} \\
(1 - \frac{\text{materialDiscount}}{100}) \cdot \sum_{i=1}^{N} \left(\text{materialCost}_i \cdot x_i\right), & \text{otherwise}
\end{cases} \label{material_cost}
\end{align}

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
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

#### Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + y
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

#### Material Cost Calculations
material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))

#### Apply discounts if applicable
material_cost_discounted = pulp.LpVariable('MaterialCostDiscounted', cat='Continuous')
problem += material_cost_discounted >= material_cost - data['DiscountThreshold'] * (1 - data['MaterialDiscount']/100)
problem += material_cost_discounted <= material_cost * (1 - data['MaterialDiscount']/100)
problem += material_cost_discounted >= material_cost

#### Objective Function
profit = (
    pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) -
    data['OvertimeAssemblyCost'] * y -
    material_cost_discounted
)

problem += profit

#### Solve problem
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

