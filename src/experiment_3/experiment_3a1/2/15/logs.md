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
    \item \( \text{maxAssembly} \): Maximum available hours of assembly labor per day
    \item \( \text{maxTesting} \): Maximum available hours of testing per day
    \item \( \text{price}_i \): Selling price of product \( i \) (in dollars)
    \item \( \text{maxOvertimeAssembly} \): Maximum allowable hours of overtime assembly labor
    \item \( \text{overtimeAssemblyCost} \): Cost per hour of overtime assembly
    \item \( \text{materialDiscount} \): Discount percentage on materials if the daily bill exceeds a threshold
    \item \( \text{discountThreshold} \): Daily bill threshold for receiving the material discount
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_i \): Number of units produced of product \( i \) 
    \item \( y \): Number of overtime assembly hours scheduled
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{dailyProfit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i - \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i - \text{overtimeAssemblyCost} \cdot y - \text{materialDiscount} \cdot \left( \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i \geq \text{discountThreshold} \right)
\]

\subsection*{Constraints}
1. Assembly labor constraint:
\[
\sum_{i=1}^{N} \text{assemblyHour}_i \cdot x_i + y \leq \text{maxAssembly} + \text{maxOvertimeAssembly}
\]
2. Testing labor constraint:
\[
\sum_{i=1}^{N} \text{testingHour}_i \cdot x_i \leq \text{maxTesting}
\]
3. Non-negativity constraints:
\[
x_i \geq 0, \quad \forall i \in \{1, \ldots, N\}
\]
\[
y \geq 0
\]

\subsection*{Output Variables}
\begin{itemize}
    \item \text{dailyProfit}: Total daily profit of the company
    \item \text{unitsProduced}: Array of \( [x_1, x_2, \ldots, x_N] \) indicating the units produced of each product
    \item \text{overtimeAssembly}: Total hours of overtime assembly labor scheduled (variable \( y \))
    \item \text{materialBought}: Total raw materials bought, calculated as \( \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i \)
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
    \item \( \text{maxAssembly} \): Maximum available hours of assembly labor per day
    \item \( \text{maxTesting} \): Maximum available hours of testing per day
    \item \( \text{price}_i \): Selling price of product \( i \) (in dollars)
    \item \( \text{maxOvertimeAssembly} \): Maximum allowable hours of overtime assembly labor
    \item \( \text{overtimeAssemblyCost} \): Cost per hour of overtime assembly
    \item \( \text{materialDiscount} \): Discount percentage on materials if the daily bill exceeds a threshold
    \item \( \text{discountThreshold} \): Daily bill threshold for receiving the material discount
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_i \): Number of units produced of product \( i \) 
    \item \( y \): Number of overtime assembly hours scheduled
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{dailyProfit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i - \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i - \text{overtimeAssemblyCost} \cdot y - \text{materialDiscount} \cdot \left( \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i \geq \text{discountThreshold} \right)
\]

\subsection*{Constraints}
1. Assembly labor constraint:
\[
\sum_{i=1}^{N} \text{assemblyHour}_i \cdot x_i + y \leq \text{maxAssembly} + \text{maxOvertimeAssembly}
\]
2. Testing labor constraint:
\[
\sum_{i=1}^{N} \text{testingHour}_i \cdot x_i \leq \text{maxTesting}
\]
3. Non-negativity constraints:
\[
x_i \geq 0, \quad \forall i \in \{1, \ldots, N\}
\]
\[
y \geq 0
\]

\subsection*{Output Variables}
\begin{itemize}
    \item \text{dailyProfit}: Total daily profit of the company
    \item \text{unitsProduced}: Array of \( [x_1, x_2, \ldots, x_N] \) indicating the units produced of each product
    \item \text{overtimeAssembly}: Total hours of overtime assembly labor scheduled (variable \( y \))
    \item \text{materialBought}: Total raw materials bought, calculated as \( \sum_{i=1}^{N} \text{materialCost}_i \cdot x_i \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Extract data from JSON
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

#### Parameters
N = data['N']
assembly_hours = data['AssemblyHour']
testing_hours = data['TestingHour']
material_costs = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
prices = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

#### Create the problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Continuous')  #### number of units produced
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')  #### overtime hours

#### Objective Function
profit_expr = pulp.lpSum(prices[i] * x[i] for i in range(N)) \
              - pulp.lpSum(material_costs[i] * x[i] for i in range(N)) \
              - overtime_assembly_cost * y \
              - material_discount * pulp.lpSum(material_costs[i] * x[i] for i in range(N)) >= discount_threshold

problem += pulp.lpSum(prices[i] * x[i] for i in range(N)) \
           - pulp.lpSum(material_costs[i] * x[i] for i in range(N)) \
           - overtime_assembly_cost * y, "Total_Profit"

#### Constraints
problem += pulp.lpSum(assembly_hours[i] * x[i] for i in range(N)) + y <= max_assembly + max_overtime_assembly, "Assembly_Labor_Constraint"
problem += pulp.lpSum(testing_hours[i] * x[i] for i in range(N)) <= max_testing, "Testing_Labor_Constraint"

#### Solve the problem
problem.solve()

#### Output results
units_produced = [x[i].varValue for i in range(N)]
overtime_hours = y.varValue
material_bought = sum(material_costs[i] * x[i].varValue for i in range(N))

print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly Hours: {overtime_hours}')
print(f'Material Bought: {material_bought}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

