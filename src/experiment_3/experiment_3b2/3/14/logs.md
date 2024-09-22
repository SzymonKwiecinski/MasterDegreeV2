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
To model the given linear programming problem using LaTeX, we will define the decision variables, objective function, and constraints accordingly. Here's a LaTeX document representing the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\subsection*{Decision Variables}

Let:
\begin{align*}
x_i & : \text{production quantity of the } i\text{-th product} \\
u & : \text{binary variable, 1 if the company upgrades machine capacity, 0 otherwise}
\end{align*}

\subsection*{Parameters}

Given:
\begin{align*}
\text{cash} & : \text{available cash} \\
\text{hour}_i & : \text{machine hours required per unit of the } i\text{-th product} \\
\text{cost}_i & : \text{production cost per unit of the } i\text{-th product} \\
\text{price}_i & : \text{selling price per unit of the } i\text{-th product} \\
\text{investPercentage}_i & : \text{investment rate of sales revenue from the } i\text{-th product} \\
\text{upgradeHours} & : \text{additional machine hours available if upgraded} \\
\text{upgradeCost} & : \text{cost of upgrading machine capacity} \\
\text{availableHours} & : \text{current available machine hours} \\
P & : \text{number of products}
\end{align*}

\subsection*{Objective Function}

Maximize total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} \left( (\text{price}_i - \text{cost}_i - \text{price}_i \cdot \text{investPercentage}_i) \cdot x_i \right) - u \cdot \text{upgradeCost}
\]

\subsection*{Constraints}

1. Machine capacity constraint:
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + u \cdot \text{upgradeHours}
\]

2. Cash availability constraint:
\[
\sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} + \sum_{i=1}^{P} \text{price}_i \cdot \text{investPercentage}_i \cdot x_i - u \cdot \text{upgradeCost}
\]

3. Non-negativity and binary constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, P
\]
\[
u \in \{0, 1\}
\]

\end{document}
```

This document lays out the decision variables, parameters, objective function, and constraints for the linear programming model that represents the company's problem. The goal is to maximize the total net income while considering machine capacity and cash limitations. The decision to upgrade machine capacity is represented by a binary variable \( u \).

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

\subsection*{Decision Variables}

Let:
\begin{align*}
x_i & : \text{production quantity of the } i\text{-th product} \\
u & : \text{binary variable, 1 if the company upgrades machine capacity, 0 otherwise}
\end{align*}

\subsection*{Parameters}

Given:
\begin{align*}
\text{cash} & : \text{available cash} \\
\text{hour}_i & : \text{machine hours required per unit of the } i\text{-th product} \\
\text{cost}_i & : \text{production cost per unit of the } i\text{-th product} \\
\text{price}_i & : \text{selling price per unit of the } i\text{-th product} \\
\text{investPercentage}_i & : \text{investment rate of sales revenue from the } i\text{-th product} \\
\text{upgradeHours} & : \text{additional machine hours available if upgraded} \\
\text{upgradeCost} & : \text{cost of upgrading machine capacity} \\
\text{availableHours} & : \text{current available machine hours} \\
P & : \text{number of products}
\end{align*}

\subsection*{Objective Function}

Maximize total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} \left( (\text{price}_i - \text{cost}_i - \text{price}_i \cdot \text{investPercentage}_i) \cdot x_i \right) - u \cdot \text{upgradeCost}
\]

\subsection*{Constraints}

1. Machine capacity constraint:
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + u \cdot \text{upgradeHours}
\]

2. Cash availability constraint:
\[
\sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} + \sum_{i=1}^{P} \text{price}_i \cdot \text{investPercentage}_i \cdot x_i - u \cdot \text{upgradeCost}
\]

3. Non-negativity and binary constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, P
\]
\[
u \in \{0, 1\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
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

#### Problem definition
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(P)]
u = pulp.LpVariable('u', cat='Binary')

#### Objective Function
net_income = pulp.lpSum([(price[i] - cost[i] - price[i] * investPercentage[i]) * x[i] for i in range(P)]) - u * upgradeCost
problem += net_income, "Total_Net_Income"

#### Constraints
#### Machine capacity constraint
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= availableHours + u * upgradeHours, "Machine_Capacity_Constraint"

#### Cash availability constraint
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash + pulp.lpSum([price[i] * investPercentage[i] * x[i] for i in range(P)]) - u * upgradeCost, "Cash_Availability_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

