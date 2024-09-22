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

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_i \) be the production quantity of the \( i \)-th product, where \( i = 1, 2, \ldots, P \).
    \item Let \( u \) be a binary variable that indicates whether the company upgrades its machine capacity (\( u = 1 \)) or not (\( u = 0 \)).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{cash} \): Total available cash.
    \item \( \text{hour}_i \): Machine hours required per unit of the \( i \)-th product.
    \item \( \text{cost}_i \): Production cost per unit of the \( i \)-th product.
    \item \( \text{price}_i \): Selling price per unit of the \( i \)-th product.
    \item \( \text{investPercentage}_i \): Percentage of sales revenue from the \( i \)-th product made available for operations.
    \item \( \text{upgradeHours} \): Additional machine hours gained by upgrading.
    \item \( \text{upgradeCost} \): Cost of upgrading.
    \item \( \text{availableHours} \): Total available machine hours in the current production period.
\end{itemize}

\textbf{Objective Function:}
We aim to maximize the total net income:
\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( \text{price}_i x_i - \text{cost}_i x_i - \text{investPercentage}_i \cdot \text{price}_i x_i \right) - \text{upgradeCost} \cdot u
\]

\textbf{Constraints:}

1. Cash availability constraint:
\[
\sum_{i=1}^{P} \text{cost}_i x_i \leq \text{cash}
\]

2. Machine capacity constraint:
\[
\sum_{i=1}^{P} \text{hour}_i x_i \leq \text{availableHours} + \text{upgradeHours} \cdot u
\]

3. Non-negativity and integer constraints:
\[
x_i \geq 0, \quad \forall i \in \{1, 2, \ldots, P\}
\]
\[
u \in \{0, 1\}
\]

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{net\_income} = Z \)
    \item \( \text{production} = [x_1, x_2, \ldots, x_P] \)
    \item \( \text{upgrade} = u \)
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

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_i \) be the production quantity of the \( i \)-th product, where \( i = 1, 2, \ldots, P \).
    \item Let \( u \) be a binary variable that indicates whether the company upgrades its machine capacity (\( u = 1 \)) or not (\( u = 0 \)).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{cash} \): Total available cash.
    \item \( \text{hour}_i \): Machine hours required per unit of the \( i \)-th product.
    \item \( \text{cost}_i \): Production cost per unit of the \( i \)-th product.
    \item \( \text{price}_i \): Selling price per unit of the \( i \)-th product.
    \item \( \text{investPercentage}_i \): Percentage of sales revenue from the \( i \)-th product made available for operations.
    \item \( \text{upgradeHours} \): Additional machine hours gained by upgrading.
    \item \( \text{upgradeCost} \): Cost of upgrading.
    \item \( \text{availableHours} \): Total available machine hours in the current production period.
\end{itemize}

\textbf{Objective Function:}
We aim to maximize the total net income:
\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( \text{price}_i x_i - \text{cost}_i x_i - \text{investPercentage}_i \cdot \text{price}_i x_i \right) - \text{upgradeCost} \cdot u
\]

\textbf{Constraints:}

1. Cash availability constraint:
\[
\sum_{i=1}^{P} \text{cost}_i x_i \leq \text{cash}
\]

2. Machine capacity constraint:
\[
\sum_{i=1}^{P} \text{hour}_i x_i \leq \text{availableHours} + \text{upgradeHours} \cdot u
\]

3. Non-negativity and integer constraints:
\[
x_i \geq 0, \quad \forall i \in \{1, 2, \ldots, P\}
\]
\[
u \in \{0, 1\}
\]

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{net\_income} = Z \)
    \item \( \text{production} = [x_1, x_2, \ldots, x_P] \)
    \item \( \text{upgrade} = u \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

#### Parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

#### Problem definition
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(P)]
u = pulp.LpVariable('u', cat='Binary')

#### Objective function
problem += pulp.lpSum([(price[i] * x[i]) - (cost[i] * x[i]) - (invest_percentage[i] * price[i] * x[i]) for i in range(P)]) - (upgrade_cost * u), "Total_Net_Income"

#### Constraints
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash, "Cash_Availability"
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= available_hours + (upgrade_hours * u), "Machine_Capacity"

#### Solve the problem
problem.solve()

#### Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

