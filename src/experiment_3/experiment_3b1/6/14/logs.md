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

\textbf{Parameters:}
\begin{itemize}
    \item $P$: Number of different products
    \item $cash$: Available cash
    \item $hour_i$: Machine hours required for product $i$ ($i = 1, \ldots, P$)
    \item $cost_i$: Production cost per unit of product $i$ ($i = 1, \ldots, P$)
    \item $price_i$: Selling price per unit of product $i$ ($i = 1, \ldots, P$)
    \item $investPercentage_i$: Investment percentage of the sales revenues from product $i$ ($i = 1, \ldots, P$)
    \item $upgradeHours$: Additional machine hours after upgrade
    \item $upgradeCost$: Cost of upgrading the machine
    \item $availableHours$: Current available machine hours
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: Production quantity of product $i$ ($i = 1, \ldots, P$)
    \item $upgrade$: A binary variable indicating if machine upgrade should occur ($upgrade \in \{0, 1\}$)
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize } Z = \sum_{i=1}^{P} (price_i \cdot x_i - cost_i \cdot x_i - investPercentage_i \cdot (price_i \cdot x_i)) 
\]

\textbf{Subject to:}
\begin{align*}
\sum_{i=1}^{P} hour_i \cdot x_i & \leq availableHours + upgrade \cdot upgradeHours \quad \text{(Machine hour constraint)} \\
\sum_{i=1}^{P} (cost_i \cdot x_i + investPercentage_i \cdot (price_i \cdot x_i)) & \leq cash + (upgrade \cdot upgradeCost) \quad \text{(Cash constraint)} \\
x_i & \geq 0 \quad \text{(Non-negativity constraint)} \\
upgrade & \in \{0, 1\} \quad \text{(Binary variable)}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $net\_income$: Total net income of the company
    \item $production$: Production quantities $[production_1, production_2, \ldots, production_P]$
    \item $upgrade$: Whether the company should upgrade its machine capacity (true/false)
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

\textbf{Parameters:}
\begin{itemize}
    \item $P$: Number of different products
    \item $cash$: Available cash
    \item $hour_i$: Machine hours required for product $i$ ($i = 1, \ldots, P$)
    \item $cost_i$: Production cost per unit of product $i$ ($i = 1, \ldots, P$)
    \item $price_i$: Selling price per unit of product $i$ ($i = 1, \ldots, P$)
    \item $investPercentage_i$: Investment percentage of the sales revenues from product $i$ ($i = 1, \ldots, P$)
    \item $upgradeHours$: Additional machine hours after upgrade
    \item $upgradeCost$: Cost of upgrading the machine
    \item $availableHours$: Current available machine hours
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: Production quantity of product $i$ ($i = 1, \ldots, P$)
    \item $upgrade$: A binary variable indicating if machine upgrade should occur ($upgrade \in \{0, 1\}$)
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize } Z = \sum_{i=1}^{P} (price_i \cdot x_i - cost_i \cdot x_i - investPercentage_i \cdot (price_i \cdot x_i)) 
\]

\textbf{Subject to:}
\begin{align*}
\sum_{i=1}^{P} hour_i \cdot x_i & \leq availableHours + upgrade \cdot upgradeHours \quad \text{(Machine hour constraint)} \\
\sum_{i=1}^{P} (cost_i \cdot x_i + investPercentage_i \cdot (price_i \cdot x_i)) & \leq cash + (upgrade \cdot upgradeCost) \quad \text{(Cash constraint)} \\
x_i & \geq 0 \quad \text{(Non-negativity constraint)} \\
upgrade & \in \{0, 1\} \quad \text{(Binary variable)}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $net\_income$: Total net income of the company
    \item $production$: Production quantities $[production_1, production_2, \ldots, production_P]$
    \item $upgrade$: Whether the company should upgrade its machine capacity (true/false)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'P': 2,
    'Cash': 3000,
    'Hour': [2, 6],
    'Cost': [3, 2],
    'Price': [6, 5],
    'InvestPercentage': [0.4, 0.3],
    'UpgradeHours': 2000,
    'UpgradeCost': 400,
    'AvailableHours': 2000
}

#### Initializing the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("production", range(data['P']), lowBound=0)  #### Production quantities
upgrade = pulp.LpVariable("upgrade", cat='Binary')  #### Upgrade machine variable

#### Objective function
problem += pulp.lpSum((data['Price'][i] * x[i] - data['Cost'][i] * x[i] - data['InvestPercentage'][i] * (data['Price'][i] * x[i])) for i in range(data['P']))

#### Constraints
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + upgrade * data['UpgradeHours'], "Machine_Hour_Constraint"
problem += pulp.lpSum((data['Cost'][i] + data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])) <= data['Cash'] + upgrade * data['UpgradeCost'], "Cash_Constraint"

#### Solve the problem
problem.solve()

#### Print the results
production_quantities = [x[i].varValue for i in range(data['P'])]
net_income = pulp.value(problem.objective)
upgrade_decision = upgrade.varValue == 1

print(f'Net Income: {net_income}, Production Quantities: {production_quantities}, Upgrade Required: {upgrade_decision}')
print(f' (Objective Value): <OBJ>{net_income}</OBJ>')
```

