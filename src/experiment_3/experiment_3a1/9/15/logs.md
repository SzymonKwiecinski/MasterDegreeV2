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

\section*{Mathematical Model for MILP Problem}

\subsection*{Parameters}

\begin{itemize}
    \item $N$: Number of kinds of products
    \item $assemblyHour_i$: Hours of assembly labor required for product $i$
    \item $testingHour_i$: Hours of testing required for product $i$
    \item $materialCost_i$: Cost of raw materials for product $i$ (in \$)
    \item $maxAssembly$: Maximum hours of assembly labor available per day
    \item $maxTesting$: Maximum hours of testing available per day
    \item $price_i$: Price of product $i$ (in \$)
    \item $maxOvertimeAssembly$: Maximum hours of overtime assembly labor allowed
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly labor
    \item $materialDiscount$: Percentage discount on raw materials if the daily bill exceeds the threshold
    \item $discountThreshold$: Threshold for raw material bill to apply discount (in \$)
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $unitsProduced_i$: Number of units of product $i$ produced
    \item $overtimeAssembly$: Number of hours of overtime assembly labor scheduled
    \item $materialBought$: Total amount of raw materials bought (in \$)
\end{itemize}

\subsection*{Objective Function}

Maximize daily profit:

\[
dailyProfit = \sum_{i=1}^{N} price_i \cdot unitsProduced_i - \left( \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \cdot (1 - \frac{materialDiscount}{100}) + overtimeAssembly \cdot overtimeAssemblyCost \right)
\]

\subsection*{Constraints}

\begin{align}
    \sum_{i=1}^{N} assemblyHour_i \cdot unitsProduced_i + overtimeAssembly & \leq maxAssembly + maxOvertimeAssembly \\
    \sum_{i=1}^{N} testingHour_i \cdot unitsProduced_i & \leq maxTesting \\
    materialBought & = \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \\
    & \text{if } materialBought > discountThreshold \text{ then apply discount on material cost} \\
    unitsProduced_i & \geq 0 \quad \forall i \in \{1, \ldots, N\} \\
    overtimeAssembly & \geq 0
\end{align}

\subsection*{Output}

\begin{itemize}
    \item $dailyProfit$: Daily profit of the company
    \item $unitsProduced$: List of $unitsProduced_i$ for $i = 1, \ldots, N$
    \item $overtimeAssembly$: Hours of overtime assembly labor scheduled
    \item $materialBought$: Amount of raw materials bought
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

\section*{Mathematical Model for MILP Problem}

\subsection*{Parameters}

\begin{itemize}
    \item $N$: Number of kinds of products
    \item $assemblyHour_i$: Hours of assembly labor required for product $i$
    \item $testingHour_i$: Hours of testing required for product $i$
    \item $materialCost_i$: Cost of raw materials for product $i$ (in \$)
    \item $maxAssembly$: Maximum hours of assembly labor available per day
    \item $maxTesting$: Maximum hours of testing available per day
    \item $price_i$: Price of product $i$ (in \$)
    \item $maxOvertimeAssembly$: Maximum hours of overtime assembly labor allowed
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly labor
    \item $materialDiscount$: Percentage discount on raw materials if the daily bill exceeds the threshold
    \item $discountThreshold$: Threshold for raw material bill to apply discount (in \$)
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $unitsProduced_i$: Number of units of product $i$ produced
    \item $overtimeAssembly$: Number of hours of overtime assembly labor scheduled
    \item $materialBought$: Total amount of raw materials bought (in \$)
\end{itemize}

\subsection*{Objective Function}

Maximize daily profit:

\[
dailyProfit = \sum_{i=1}^{N} price_i \cdot unitsProduced_i - \left( \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \cdot (1 - \frac{materialDiscount}{100}) + overtimeAssembly \cdot overtimeAssemblyCost \right)
\]

\subsection*{Constraints}

\begin{align}
    \sum_{i=1}^{N} assemblyHour_i \cdot unitsProduced_i + overtimeAssembly & \leq maxAssembly + maxOvertimeAssembly \\
    \sum_{i=1}^{N} testingHour_i \cdot unitsProduced_i & \leq maxTesting \\
    materialBought & = \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \\
    & \text{if } materialBought > discountThreshold \text{ then apply discount on material cost} \\
    unitsProduced_i & \geq 0 \quad \forall i \in \{1, \ldots, N\} \\
    overtimeAssembly & \geq 0
\end{align}

\subsection*{Output}

\begin{itemize}
    \item $dailyProfit$: Daily profit of the company
    \item $unitsProduced$: List of $unitsProduced_i$ for $i = 1, \ldots, N$
    \item $overtimeAssembly$: Hours of overtime assembly labor scheduled
    \item $materialBought$: Amount of raw materials bought
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

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Continuous')
materialBought = pulp.LpVariable('materialBought', cat='Continuous')

#### Objective Function
profit_terms = [data['Price'][i] * unitsProduced[i] for i in range(data['N'])]
cost_terms = [data['MaterialCost'][i] * unitsProduced[i] * (1 - data['MaterialDiscount'] / 100) for i in range(data['N'])]
objective = pulp.lpSum(profit_terms) - (pulp.lpSum(cost_terms) + overtimeAssembly * data['OvertimeAssemblyCost'])
problem += objective

#### Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) + overtimeAssembly 
            <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint")

problem += (pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) 
            <= data['MaxTesting'], "Testing_Labor_Constraint")

problem += (materialBought == pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N'])), 
            "Material_Bought_Constraint")

#### Solve the problem
problem.solve()

#### Output results
unitsProduced_result = [unitsProduced[i].varValue for i in range(data['N'])]
overtimeAssembly_result = overtimeAssembly.varValue
materialBought_result = materialBought.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Units Produced: {unitsProduced_result}')
print(f'Overtime Assembly Hours: {overtimeAssembly_result}')
print(f'Material Bought: {materialBought_result}')
```

