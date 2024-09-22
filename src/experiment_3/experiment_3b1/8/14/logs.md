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

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: Number of units produced of product $i$, for $i = 1, \ldots, P$.
    \item $u$: Boolean variable indicating whether the company should upgrade its machine capacity (1 if upgrade, 0 otherwise).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $hour_i$: Machine hours required for each unit of product $i$.
    \item $availableHours$: Total available machine hours in the current production period.
    \item $cost_i$: Production cost per unit of product $i$.
    \item $price_i$: Selling price per unit of product $i$.
    \item $investPercentage_i$: Percentage of sales revenue from product $i$ that is reinvested.
    \item $cash$: Total available cash.
    \item $upgradeHours$: Additional machine hours obtained by upgrading.
    \item $upgradeCost$: Cost of upgrading the machine capacity.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{i=1}^P \left( x_i \cdot (price_i - cost_i - investPercentage_i \cdot price_i) \right) - upgradeCost \cdot u
\]

\textbf{Subject to:}
\[
\sum_{i=1}^P hour_i \cdot x_i \leq availableHours + upgradeHours \cdot u
\]

\[
\sum_{i=1}^P cost_i \cdot x_i \leq cash
\]

\[
x_i \geq 0 \quad \text{and integer for } i = 1, \ldots, P
\]

\[
u \in \{0, 1\}
\]

\textbf{Output:}
\begin{itemize}
    \item $\text{net\_income} = Z$
    \item $\text{production} = [x_1, x_2, \ldots, x_P]$
    \item $\text{upgrade} = u$
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

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: Number of units produced of product $i$, for $i = 1, \ldots, P$.
    \item $u$: Boolean variable indicating whether the company should upgrade its machine capacity (1 if upgrade, 0 otherwise).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $hour_i$: Machine hours required for each unit of product $i$.
    \item $availableHours$: Total available machine hours in the current production period.
    \item $cost_i$: Production cost per unit of product $i$.
    \item $price_i$: Selling price per unit of product $i$.
    \item $investPercentage_i$: Percentage of sales revenue from product $i$ that is reinvested.
    \item $cash$: Total available cash.
    \item $upgradeHours$: Additional machine hours obtained by upgrading.
    \item $upgradeCost$: Cost of upgrading the machine capacity.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{i=1}^P \left( x_i \cdot (price_i - cost_i - investPercentage_i \cdot price_i) \right) - upgradeCost \cdot u
\]

\textbf{Subject to:}
\[
\sum_{i=1}^P hour_i \cdot x_i \leq availableHours + upgradeHours \cdot u
\]

\[
\sum_{i=1}^P cost_i \cdot x_i \leq cash
\]

\[
x_i \geq 0 \quad \text{and integer for } i = 1, \ldots, P
\]

\[
u \in \{0, 1\}
\]

\textbf{Output:}
\begin{itemize}
    \item $\text{net\_income} = Z$
    \item $\text{production} = [x_1, x_2, \ldots, x_P]$
    \item $\text{upgrade} = u$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

#### Extracting data from the dictionary
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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(1, P + 1), lowBound=0, cat='Integer')
u = pulp.LpVariable("u", cat='Binary')

#### Objective function
problem += pulp.lpSum([(x[i] * (price[i-1] - cost[i-1] - investPercentage[i-1] * price[i-1])) for i in range(1, P + 1)]) - (upgradeCost * u), "Objective"

#### Constraints
problem += pulp.lpSum([hour[i-1] * x[i] for i in range(1, P + 1)]) <= availableHours + upgradeHours * u, "Machine_Hours_Constraint"
problem += pulp.lpSum([cost[i-1] * x[i] for i in range(1, P + 1)]) <= cash, "Cash_Constraint"

#### Solve the problem
problem.solve()

#### Output results
net_income = pulp.value(problem.objective)
production = [x[i].varValue for i in range(1, P + 1)]
upgrade = u.varValue

print(f' (Objective Value): <OBJ>{net_income}</OBJ>')
print(f'Production: {production}')
print(f'Upgrade: {upgrade}')
```

