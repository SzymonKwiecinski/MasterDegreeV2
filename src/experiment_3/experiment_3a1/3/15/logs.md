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

\section*{Mixed Integer Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item Let $x_i$ be the number of units of product $i$ produced, for $i = 1, \ldots, N$.
    \item Let $o$ be the number of hours of overtime assembly labor scheduled.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $assemblyHour_i$: hours of assembly labor required for product $i$.
    \item $testingHour_i$: hours of testing required for product $i$.
    \item $materialCost_i$: cost of raw materials for product $i$.
    \item $maxAssembly$: maximum available assembly hours per day.
    \item $maxTesting$: maximum available testing hours per day.
    \item $price_i$: selling price of product $i$.
    \item $maxOvertimeAssembly$: maximum available overtime assembly hours.
    \item $overtimeAssemblyCost$: cost per hour of overtime assembly labor.
    \item $materialDiscount$: percentage discount on raw materials.
    \item $discountThreshold$: minimum amount for discount eligibility.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize } Z &= \sum_{i=1}^{N} (price_i \cdot x_i) - \left( \sum_{i=1}^{N} (materialCost_i \cdot x_i) \cdot (1 - \frac{materialDiscount}{100}) + overtimeAssemblyCost \cdot o \right)
\end{align*}

\textbf{Constraints:}
\begin{align*}
\sum_{i=1}^{N} (assemblyHour_i \cdot x_i) + o &\leq maxAssembly + maxOvertimeAssembly \\
\sum_{i=1}^{N} (testingHour_i \cdot x_i) &\leq maxTesting \\
\sum_{i=1}^{N} (materialCost_i \cdot x_i) &\geq discountThreshold \\
x_i &\geq 0 \quad \text{(integer for all } i\text{)} \\
o &\geq 0 \quad \text{(non-negative)}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $dailyProfit$: the maximum daily profit of the company.
    \item $unitsProduced$: the array of number of units produced for each product $i$.
    \item $overtimeAssembly$: the total hours of overtime assembly labor scheduled.
    \item $materialBought$: the total amount of raw materials bought.
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

\section*{Mixed Integer Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item Let $x_i$ be the number of units of product $i$ produced, for $i = 1, \ldots, N$.
    \item Let $o$ be the number of hours of overtime assembly labor scheduled.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $assemblyHour_i$: hours of assembly labor required for product $i$.
    \item $testingHour_i$: hours of testing required for product $i$.
    \item $materialCost_i$: cost of raw materials for product $i$.
    \item $maxAssembly$: maximum available assembly hours per day.
    \item $maxTesting$: maximum available testing hours per day.
    \item $price_i$: selling price of product $i$.
    \item $maxOvertimeAssembly$: maximum available overtime assembly hours.
    \item $overtimeAssemblyCost$: cost per hour of overtime assembly labor.
    \item $materialDiscount$: percentage discount on raw materials.
    \item $discountThreshold$: minimum amount for discount eligibility.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize } Z &= \sum_{i=1}^{N} (price_i \cdot x_i) - \left( \sum_{i=1}^{N} (materialCost_i \cdot x_i) \cdot (1 - \frac{materialDiscount}{100}) + overtimeAssemblyCost \cdot o \right)
\end{align*}

\textbf{Constraints:}
\begin{align*}
\sum_{i=1}^{N} (assemblyHour_i \cdot x_i) + o &\leq maxAssembly + maxOvertimeAssembly \\
\sum_{i=1}^{N} (testingHour_i \cdot x_i) &\leq maxTesting \\
\sum_{i=1}^{N} (materialCost_i \cdot x_i) &\geq discountThreshold \\
x_i &\geq 0 \quad \text{(integer for all } i\text{)} \\
o &\geq 0 \quad \text{(non-negative)}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $dailyProfit$: the maximum daily profit of the company.
    \item $unitsProduced$: the array of number of units produced for each product $i$.
    \item $overtimeAssembly$: the total hours of overtime assembly labor scheduled.
    \item $materialBought$: the total amount of raw materials bought.
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

#### Number of products
N = data['N']

#### Create the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')  #### units of product i
o = pulp.LpVariable("o", lowBound=0)  #### overtime hours

#### Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(N)) - (
    pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(N)) * (1 - data['MaterialDiscount'] / 100) +
    data['OvertimeAssemblyCost'] * o
)
problem += profit

#### Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(N)) + o <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Hours_Constraint"
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(N)) <= data['MaxTesting'], "Testing_Hours_Constraint"
problem += pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(N)) >= data['DiscountThreshold'], "Material_Cost_Constraint"

#### Solve the problem
problem.solve()

#### Output results
dailyProfit = pulp.value(problem.objective)
unitsProduced = [pulp.value(x[i]) for i in range(N)]
overtimeAssembly = pulp.value(o)
materialBought = sum(data['MaterialCost'][i] * unitsProduced[i] for i in range(N))

print(f' (Objective Value): <OBJ>{dailyProfit}</OBJ>')
print(f'Units Produced: {unitsProduced}')
print(f'Total Overtime Assembly Hours: {overtimeAssembly}')
print(f'Total Material Bought: {materialBought}')
```

