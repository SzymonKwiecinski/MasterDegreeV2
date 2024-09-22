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

\textbf{Sets:}
\begin{itemize}
    \item $N$: Number of product types
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $assemblyHour_i$: Assembly hours required for product type $i$ 
    \item $testingHour_i$: Testing hours required for product type $i$ 
    \item $materialCost_i$: Material cost for product type $i$ in dollars
    \item $maxAssembly$: Maximum available assembly hours per day
    \item $maxTesting$: Maximum available testing hours per day
    \item $price_i$: Selling price of product type $i$ in dollars
    \item $maxOvertimeAssembly$: Maximum allowable overtime assembly hours
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly
    \item $materialDiscount$: Discount percentage on materials if applicable
    \item $discountThreshold$: Threshold for discount eligibility
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $unitsProduced_i$: Number of units produced of product type $i$
    \item $overtimeAssembly$: Number of overtime assembly hours scheduled
    \item $materialBought$: Total cost of materials bought
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize: } & \text{dailyProfit} = \sum_{i=1}^{N} (price_i \cdot unitsProduced_i) - materialBought - (overtimeAssembly \cdot overtimeAssemblyCost)
\end{align*}

\textbf{Constraints:}
\begin{align*}
1. & \quad \sum_{i=1}^{N} (assemblyHour_i \cdot unitsProduced_i) + overtimeAssembly \leq maxAssembly + maxOvertimeAssembly \\
2. & \quad \sum_{i=1}^{N} (testingHour_i \cdot unitsProduced_i) \leq maxTesting \\
3. & \quad materialBought = \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \cdot \left(1 - \frac{materialDiscount}{100}\right) \text{ if } materialBought > discountThreshold \\
4. & \quad materialBought = \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \text{ otherwise}
\end{align*}

\textbf{Output:}
\begin{align*}
\text{dailyProfit} & \\
unitsProduced & = [unitsProduced_1, unitsProduced_2, \ldots, unitsProduced_N] \\
overtimeAssembly & \\
materialBought & 
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

\section*{Mathematical Model for Production Optimization}

\textbf{Sets:}
\begin{itemize}
    \item $N$: Number of product types
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $assemblyHour_i$: Assembly hours required for product type $i$ 
    \item $testingHour_i$: Testing hours required for product type $i$ 
    \item $materialCost_i$: Material cost for product type $i$ in dollars
    \item $maxAssembly$: Maximum available assembly hours per day
    \item $maxTesting$: Maximum available testing hours per day
    \item $price_i$: Selling price of product type $i$ in dollars
    \item $maxOvertimeAssembly$: Maximum allowable overtime assembly hours
    \item $overtimeAssemblyCost$: Cost per hour of overtime assembly
    \item $materialDiscount$: Discount percentage on materials if applicable
    \item $discountThreshold$: Threshold for discount eligibility
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $unitsProduced_i$: Number of units produced of product type $i$
    \item $overtimeAssembly$: Number of overtime assembly hours scheduled
    \item $materialBought$: Total cost of materials bought
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize: } & \text{dailyProfit} = \sum_{i=1}^{N} (price_i \cdot unitsProduced_i) - materialBought - (overtimeAssembly \cdot overtimeAssemblyCost)
\end{align*}

\textbf{Constraints:}
\begin{align*}
1. & \quad \sum_{i=1}^{N} (assemblyHour_i \cdot unitsProduced_i) + overtimeAssembly \leq maxAssembly + maxOvertimeAssembly \\
2. & \quad \sum_{i=1}^{N} (testingHour_i \cdot unitsProduced_i) \leq maxTesting \\
3. & \quad materialBought = \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \cdot \left(1 - \frac{materialDiscount}{100}\right) \text{ if } materialBought > discountThreshold \\
4. & \quad materialBought = \sum_{i=1}^{N} materialCost_i \cdot unitsProduced_i \text{ otherwise}
\end{align*}

\textbf{Output:}
\begin{align*}
\text{dailyProfit} & \\
unitsProduced & = [unitsProduced_1, unitsProduced_2, \ldots, unitsProduced_N] \\
overtimeAssembly & \\
materialBought & 
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extracting data
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

#### Defining the problem
problem = pulp.LpProblem("ProductionOptimization", pulp.LpMaximize)

#### Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')
materialBought = pulp.LpVariable('materialBought', lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N'])) - materialBought - (overtimeAssembly * data['OvertimeAssemblyCost'])
problem += profit

#### Constraints

#### Assembly hours constraint including overtime
problem += (pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) + overtimeAssembly 
            <= data['MaxAssembly'] + data['MaxOvertimeAssembly'])

#### Testing hours constraint
problem += (pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxTesting'])

#### Material cost with discount application
material_cost_no_discount = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
discounted_material_cost = material_cost_no_discount * (1 - data['MaterialDiscount'] / 100)

#### Conditional constraint for material bought
problem += (materialBought >= discounted_material_cost, "MaterialDiscountConditional") 
problem += (materialBought >= material_cost_no_discount, "MaterialCostNoDiscount")

#### Solve the problem
problem.solve()

#### Output Results
print(f'unitsProduced: {[pulp.value(unitsProduced[i]) for i in range(data["N"])]}')
print(f'overtimeAssembly: {pulp.value(overtimeAssembly)}')
print(f'materialBought: {pulp.value(materialBought)}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

