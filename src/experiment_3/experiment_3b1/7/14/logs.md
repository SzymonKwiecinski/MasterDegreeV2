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

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different products
    \item $cash$: Total available cash
    \item $hour_i$: Machine hours required for producing one unit of product $i$ (for $i = 1, \ldots, P$)
    \item $cost_i$: Production cost per unit of product $i$ (for $i = 1, \ldots, P$)
    \item $price_i$: Selling price per unit of product $i$ (for $i = 1, \ldots, P$)
    \item $investPercentage_i$: Investment percentage of the sales revenues from product $i$ (for $i = 1, \ldots, P$)
    \item $upgradeHours$: Additional machine hours available from upgrades
    \item $upgradeCost$: Cost for upgrading the machine
    \item $availableHours$: Total available machine hours before upgrades
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $production_i$: Production quantity of product $i$ (for $i = 1, \ldots, P$)
    \item $upgrade$: A binary variable indicating whether the company should upgrade its machine capacity
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} (price_i \cdot production_i - cost_i \cdot production_i - investPercentage_i \cdot (price_i \cdot production_i)) - upgradeCost \cdot upgrade
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \sum_{i=1}^{P} (hour_i \cdot production_i) \leq availableHours + upgradeHours \cdot upgrade \\
2. & \quad \sum_{i=1}^{P} (cost_i \cdot production_i) + \sum_{i=1}^{P} (investPercentage_i \cdot (price_i \cdot production_i)) \leq cash \\
3. & \quad production_i \geq 0 \quad \text{for } i=1,\ldots,P \\
4. & \quad upgrade \in \{0, 1\}
\end{align*}

\subsection*{Output}
The output consists of:
\begin{itemize}
    \item $net\_income$: The net income of the company
    \item $production$: An array containing $production_i$ for $i = 1, \ldots, P$
    \item $upgrade$: A boolean variable indicating whether to upgrade or not
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

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different products
    \item $cash$: Total available cash
    \item $hour_i$: Machine hours required for producing one unit of product $i$ (for $i = 1, \ldots, P$)
    \item $cost_i$: Production cost per unit of product $i$ (for $i = 1, \ldots, P$)
    \item $price_i$: Selling price per unit of product $i$ (for $i = 1, \ldots, P$)
    \item $investPercentage_i$: Investment percentage of the sales revenues from product $i$ (for $i = 1, \ldots, P$)
    \item $upgradeHours$: Additional machine hours available from upgrades
    \item $upgradeCost$: Cost for upgrading the machine
    \item $availableHours$: Total available machine hours before upgrades
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $production_i$: Production quantity of product $i$ (for $i = 1, \ldots, P$)
    \item $upgrade$: A binary variable indicating whether the company should upgrade its machine capacity
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} (price_i \cdot production_i - cost_i \cdot production_i - investPercentage_i \cdot (price_i \cdot production_i)) - upgradeCost \cdot upgrade
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \sum_{i=1}^{P} (hour_i \cdot production_i) \leq availableHours + upgradeHours \cdot upgrade \\
2. & \quad \sum_{i=1}^{P} (cost_i \cdot production_i) + \sum_{i=1}^{P} (investPercentage_i \cdot (price_i \cdot production_i)) \leq cash \\
3. & \quad production_i \geq 0 \quad \text{for } i=1,\ldots,P \\
4. & \quad upgrade \in \{0, 1\}
\end{align*}

\subsection*{Output}
The output consists of:
\begin{itemize}
    \item $net\_income$: The net income of the company
    \item $production$: An array containing $production_i$ for $i = 1, \ldots, P$
    \item $upgrade$: A boolean variable indicating whether to upgrade or not
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

#### Parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

#### Create the problem instance
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0) for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

#### Objective Function
net_income = pulp.lpSum(price[i] * production[i] - cost[i] * production[i] - investPercentage[i] * (price[i] * production[i]) for i in range(P)) - upgradeCost * upgrade
problem += net_income

#### Constraints
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= availableHours + upgradeHours * upgrade
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) + pulp.lpSum(investPercentage[i] * (price[i] * production[i]) for i in range(P)) <= cash

#### Solve the problem
problem.solve()

#### Output the results
production_values = [production[i].varValue for i in range(P)]
upgrade_value = upgrade.varValue
net_income_value = pulp.value(problem.objective)

print(f'Production quantities: {production_values}')
print(f'Upgrade machine: {bool(upgrade_value)}')
print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')
```

