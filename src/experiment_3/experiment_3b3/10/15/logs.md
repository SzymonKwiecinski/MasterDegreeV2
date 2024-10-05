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

\section*{Mathematical Model for Production Maximization}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of product types
    \item $assemblyHour_i$: Hours of assembly labor required for product $i$
    \item $testingHour_i$: Hours of testing required for product $i$
    \item $materialCost_i$: Cost of raw materials for product $i$
    \item $maxAssembly$: Maximum hours of assembly labor available per day
    \item $maxTesting$: Maximum hours of testing available per day
    \item $price_i$: Selling price of product $i$
    \item $maxOvertimeAssembly$: Maximum hours of overtime assembly labor allowed
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly labor
    \item $materialDiscount$: Discount percentage on materials if the total exceeds a threshold
    \item $discountThreshold$: Threshold for material bill to qualify for a discount
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of units of product $i$ produced
    \item $overtimeAssembly$: Hours of overtime assembly labor scheduled
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{dailyProfit} = \sum_{i=1}^{N} (price_i \cdot x_i) - \left( \sum_{i=1}^{N} (materialCost_i \cdot x_i) - \text{discount} \right) - (overtimeAssembly \cdot overtimeAssemblyCost)
\]
Where,
\[
\text{discount} = 
\begin{cases} 
\frac{materialDiscount}{100} \cdot \sum_{i=1}^{N} (materialCost_i \cdot x_i) & \text{if } \sum_{i=1}^{N} (materialCost_i \cdot x_i) > discountThreshold \\
0 & \text{otherwise} 
\end{cases}
\]

\subsection*{Constraints}
1. Assembly labor constraint:
   \[
   \sum_{i=1}^{N} (assemblyHour_i \cdot x_i) + overtimeAssembly \leq maxAssembly + maxOvertimeAssembly
   \]
   
2. Testing hours constraint:
   \[
   \sum_{i=1}^{N} (testingHour_i \cdot x_i) \leq maxTesting
   \]

3. Non-negativity constraints:
   \[
   x_i \geq 0 \quad \forall i \in \{1, \ldots, N\}
   \]
   \[
   overtimeAssembly \geq 0
   \]

\subsection*{Outputs}
\begin{itemize}
    \item \text{dailyProfit}: The calculated daily profit
    \item \text{unitsProduced}: $[x_1, x_2, \ldots, x_N]$: Number of units produced for each product
    \item \text{overtimeAssembly}: Hours of overtime assembly scheduled
    \item \text{materialBought}: Total amount of raw materials purchased
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

\section*{Mathematical Model for Production Maximization}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of product types
    \item $assemblyHour_i$: Hours of assembly labor required for product $i$
    \item $testingHour_i$: Hours of testing required for product $i$
    \item $materialCost_i$: Cost of raw materials for product $i$
    \item $maxAssembly$: Maximum hours of assembly labor available per day
    \item $maxTesting$: Maximum hours of testing available per day
    \item $price_i$: Selling price of product $i$
    \item $maxOvertimeAssembly$: Maximum hours of overtime assembly labor allowed
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly labor
    \item $materialDiscount$: Discount percentage on materials if the total exceeds a threshold
    \item $discountThreshold$: Threshold for material bill to qualify for a discount
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of units of product $i$ produced
    \item $overtimeAssembly$: Hours of overtime assembly labor scheduled
\end{itemize}

\subsection*{Objective Function}
Maximize the daily profit:
\[
\text{dailyProfit} = \sum_{i=1}^{N} (price_i \cdot x_i) - \left( \sum_{i=1}^{N} (materialCost_i \cdot x_i) - \text{discount} \right) - (overtimeAssembly \cdot overtimeAssemblyCost)
\]
Where,
\[
\text{discount} = 
\begin{cases} 
\frac{materialDiscount}{100} \cdot \sum_{i=1}^{N} (materialCost_i \cdot x_i) & \text{if } \sum_{i=1}^{N} (materialCost_i \cdot x_i) > discountThreshold \\
0 & \text{otherwise} 
\end{cases}
\]

\subsection*{Constraints}
1. Assembly labor constraint:
   \[
   \sum_{i=1}^{N} (assemblyHour_i \cdot x_i) + overtimeAssembly \leq maxAssembly + maxOvertimeAssembly
   \]
   
2. Testing hours constraint:
   \[
   \sum_{i=1}^{N} (testingHour_i \cdot x_i) \leq maxTesting
   \]

3. Non-negativity constraints:
   \[
   x_i \geq 0 \quad \forall i \in \{1, \ldots, N\}
   \]
   \[
   overtimeAssembly \geq 0
   \]

\subsection*{Outputs}
\begin{itemize}
    \item \text{dailyProfit}: The calculated daily profit
    \item \text{unitsProduced}: $[x_1, x_2, \ldots, x_N]$: Number of units produced for each product
    \item \text{overtimeAssembly}: Hours of overtime assembly scheduled
    \item \text{materialBought}: Total amount of raw materials purchased
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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
problem = pulp.LpProblem("Production_Maximization", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Continuous')

#### Discount calculation
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
discount = pulp.LpVariable('discount', lowBound=0, cat='Continuous')

#### Objective Function
profit = (
    pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) 
    - total_material_cost 
    + discount
    - overtimeAssembly * data['OvertimeAssemblyCost']
)
problem += profit

#### Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly']), 'Assembly_Labor_Constraint'
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']), 'Testing_Hours_Constraint'

#### Material cost constraint for discount
problem += (
    discount <= data['MaterialDiscount'] / 100 * total_material_cost
), 'Discount_Constraint'
problem += (
    discount <= (total_material_cost - data['DiscountThreshold']) * 1000
), 'Discount_Threshold_Constraint'

#### Solve
problem.solve()

#### Outputs
unitsProduced = [pulp.value(x[i]) for i in range(data['N'])]
overtimeHours = pulp.value(overtimeAssembly)
totalMaterialBought = pulp.value(total_material_cost)

#### Display Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Other Outputs
print(f'Units Produced: {unitsProduced}')
print(f'Overtime Assembly Hours: {overtimeHours}')
print(f'Total Material Cost: {totalMaterialBought}')
```


