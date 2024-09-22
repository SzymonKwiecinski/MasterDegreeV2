# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A company produces and sells \var{P} different products. 
- The demand for each product is unlimited, but the company is constrained by cash availability and machine capacity.
- Each unit of the \var{i}-th product requires \var{hour_i} machine hours.
- There are \var{availableHours} machine hours available in the current production period.
- The production costs are \var{cost_i} per unit of the \var{i}-th product.
- The selling prices of the \var{i}-th product is \var{price_i} per unit.
- The available cash is \var{cash}.
- Furthermore, \var{investRate_i} of the sales revenues from the \var{i}-th product will be made available to finance operations during the current period.
- \var{investPercentage_i} is a number between 0 and 1
- The company could increase its available machine hours by \var{upgradeHours}, after spending \var{upgradeCost} for certain repairs. 
- The net income from each product is the revenue we get from selling it minus the production cost and the investment cost.

INPUT FORMAT:

{
    "cash": cash,
    "hour": [hour_i for i in 1, ..., P],
    "cost": [cost_i for i in 1, ..., P],
    "price": [price_i for i in 1, ..., P],
    "investPercentage": [investPercentage_i for i in 1, ..., P],
    "upgradeHours": upgradeHours,   
    "upgradeCost": upgradeCost,
    "availableHours": availableHours,
}

OBJECTIVE: We are aiming at maximizing total net income subject to the cash availability and machine capacity limitations

OUTPUT INFO:

- \var{net_income} shows the net income of the company
- \var{production_i} shows the production quantity of the \var{i}-th product
- \var{upgrade} is a boolean variable that shows whether the company should upgrade its machine capacity or not

OUTPUT FORMAT:

{
    "net_income": net_income,
    "production": [production_i for i in 1, ..., P],
    "upgrade": true/false,
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Indices:} \\
Let \( i \) denote the index of products, where \( i = 1, 2, \ldots, P \).

\textbf{Parameters:} \\
\begin{align*}
\text{availableHours} & : \text{Total machine hours available} \\
\text{cash} & : \text{Total available cash} \\
\text{hour}_i & : \text{Machine hours required for product } i \\
\text{cost}_i & : \text{Production cost per unit of product } i \\
\text{price}_i & : \text{Selling price per unit of product } i \\
\text{investPercentage}_i & : \text{Percentage of sales revenue invested from product } i \\
\text{upgradeHours} & : \text{Additional machine hours gained from upgrade} \\
\text{upgradeCost} & : \text{Cost of upgrading machine hours}
\end{align*}

\textbf{Decision Variables:} \\
Let \( x_i \) be the number of units produced of product \( i \) (for \( i = 1, \ldots, P \)). \\
Let \( u \) be a binary variable indicating whether the machine capacity should be upgraded (1 if upgraded, 0 otherwise).

\textbf{Objective Function:} \\
Maximize the total net income:
\[
\text{Maximize } Z = \sum_{i=1}^{P} (price_i \cdot x_i - cost_i \cdot x_i - investPercentage_i \cdot (price_i \cdot x_i)) - upgradeCost \cdot u
\]

\textbf{Subject to the Constraints:}

1. Machine Capacity Constraint:
\[
\sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot u
\]

2. Cash Availability Constraint:
\[
\sum_{i=1}^{P} cost_i \cdot x_i \leq cash
\]

3. Non-negativity:
\[
x_i \geq 0 \quad \forall i \\
u \in \{0, 1\}
\end{align*}

\textbf{Output:} \\
The solution to the above model will yield:
\begin{align*}
\text{net\_income} & : Z \\
\text{production} & : [x_1, x_2, \ldots, x_P] \\
\text{upgrade} & : u
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

\section*{Linear Programming Model}

\textbf{Indices:} \\
Let \( i \) denote the index of products, where \( i = 1, 2, \ldots, P \).

\textbf{Parameters:} \\
\begin{align*}
\text{availableHours} & : \text{Total machine hours available} \\
\text{cash} & : \text{Total available cash} \\
\text{hour}_i & : \text{Machine hours required for product } i \\
\text{cost}_i & : \text{Production cost per unit of product } i \\
\text{price}_i & : \text{Selling price per unit of product } i \\
\text{investPercentage}_i & : \text{Percentage of sales revenue invested from product } i \\
\text{upgradeHours} & : \text{Additional machine hours gained from upgrade} \\
\text{upgradeCost} & : \text{Cost of upgrading machine hours}
\end{align*}

\textbf{Decision Variables:} \\
Let \( x_i \) be the number of units produced of product \( i \) (for \( i = 1, \ldots, P \)). \\
Let \( u \) be a binary variable indicating whether the machine capacity should be upgraded (1 if upgraded, 0 otherwise).

\textbf{Objective Function:} \\
Maximize the total net income:
\[
\text{Maximize } Z = \sum_{i=1}^{P} (price_i \cdot x_i - cost_i \cdot x_i - investPercentage_i \cdot (price_i \cdot x_i)) - upgradeCost \cdot u
\]

\textbf{Subject to the Constraints:}

1. Machine Capacity Constraint:
\[
\sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot u
\]

2. Cash Availability Constraint:
\[
\sum_{i=1}^{P} cost_i \cdot x_i \leq cash
\]

3. Non-negativity:
\[
x_i \geq 0 \quad \forall i \\
u \in \{0, 1\}
\end{align*}

\textbf{Output:} \\
The solution to the above model will yield:
\begin{align*}
\text{net\_income} & : Z \\
\text{production} & : [x_1, x_2, \ldots, x_P] \\
\text{upgrade} & : u
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the JSON format
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 
        'AvailableHours': 2000}

#### Extracting parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

#### Define the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(1, P + 1), lowBound=0, cat='Continuous')  #### Production quantities
u = pulp.LpVariable("u", cat='Binary')  #### Upgrade decision

#### Objective Function
problem += pulp.lpSum([(price[i-1] * x[i] - cost[i-1] * x[i] - invest_percentage[i-1] * (price[i-1] * x[i])) for i in range(1, P + 1)]) - upgrade_cost * u, "Total_Net_Income"

#### Constraints
problem += pulp.lpSum([hour[i-1] * x[i] for i in range(1, P + 1)]) <= available_hours + upgrade_hours * u, "Machine_Capacity_Constraint"
problem += pulp.lpSum([cost[i-1] * x[i] for i in range(1, P + 1)]) <= cash, "Cash_Availability_Constraint"

#### Solve the problem
problem.solve()

#### Output results
net_income = pulp.value(problem.objective)
production = [pulp.value(x[i]) for i in range(1, P + 1)]
upgrade = pulp.value(u)

print(f' (Objective Value): <OBJ>{net_income}</OBJ>')
print(f'Production quantities: {production}')
print(f'Upgrade: {upgrade}')
```

