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

\section*{Linear Programming Model for Product Production}

Let:
\begin{itemize}
    \item $P$: The number of products
    \item $cash$: The available cash
    \item $hour_i$: The machine hours required for producing the $i$-th product
    \item $cost_i$: The production cost per unit of the $i$-th product
    \item $price_i$: The selling price per unit of the $i$-th product
    \item $investPercentage_i$: The percentage of revenues from the $i$-th product available for reinvestment
    \item $upgradeHours$: Additional machine hours that can be obtained through upgrades
    \item $upgradeCost$: The cost of upgrading the machine capacity
    \item $availableHours$: The current available machine hours
    \item $production_i$: The quantity produced of the $i$-th product
    \item $upgrade$: A binary variable indicating whether to upgrade the machine
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:

\[
Z = \sum_{i=1}^{P} \left( (price_i - cost_i) \cdot production_i - investPercentage_i \cdot (price_i \cdot production_i) \right) - upgradeCost \cdot upgrade
\]

\subsection*{Constraints}

1. **Machine Capacity Constraint**:
\[
\sum_{i=1}^{P} hour_i \cdot production_i \leq availableHours + upgradeHours \cdot upgrade
\]

2. **Cash Availability Constraint**:
\[
\sum_{i=1}^{P} cost_i \cdot production_i \leq cash
\]

3. **Non-negativity Constraints**:
\[
production_i \geq 0 \quad \forall i = 1, \ldots, P
\]
\[
upgrade \in \{0, 1\}
\]

\subsection*{Output Variables}
The outputs of the model will be:
\begin{itemize}
    \item $\text{net\_income}$: Total net income from production
    \item $\text{production}$: The production quantities $[production_1, production_2, \ldots, production_P]$
    \item $\text{upgrade}$: Indicates if the upgrade was performed (true or false)
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

\section*{Linear Programming Model for Product Production}

Let:
\begin{itemize}
    \item $P$: The number of products
    \item $cash$: The available cash
    \item $hour_i$: The machine hours required for producing the $i$-th product
    \item $cost_i$: The production cost per unit of the $i$-th product
    \item $price_i$: The selling price per unit of the $i$-th product
    \item $investPercentage_i$: The percentage of revenues from the $i$-th product available for reinvestment
    \item $upgradeHours$: Additional machine hours that can be obtained through upgrades
    \item $upgradeCost$: The cost of upgrading the machine capacity
    \item $availableHours$: The current available machine hours
    \item $production_i$: The quantity produced of the $i$-th product
    \item $upgrade$: A binary variable indicating whether to upgrade the machine
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:

\[
Z = \sum_{i=1}^{P} \left( (price_i - cost_i) \cdot production_i - investPercentage_i \cdot (price_i \cdot production_i) \right) - upgradeCost \cdot upgrade
\]

\subsection*{Constraints}

1. **Machine Capacity Constraint**:
\[
\sum_{i=1}^{P} hour_i \cdot production_i \leq availableHours + upgradeHours \cdot upgrade
\]

2. **Cash Availability Constraint**:
\[
\sum_{i=1}^{P} cost_i \cdot production_i \leq cash
\]

3. **Non-negativity Constraints**:
\[
production_i \geq 0 \quad \forall i = 1, \ldots, P
\]
\[
upgrade \in \{0, 1\}
\]

\subsection*{Output Variables}
The outputs of the model will be:
\begin{itemize}
    \item $\text{net\_income}$: Total net income from production
    \item $\text{production}$: The production quantities $[production_1, production_2, \ldots, production_P]$
    \item $\text{upgrade}$: Indicates if the upgrade was performed (true or false)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
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

#### Create the LP problem
problem = pulp.LpProblem("Product_Production", pulp.LpMaximize)

#### Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0) for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

#### Objective Function
net_income = pulp.lpSum((data['Price'][i] - data['Cost'][i]) * production[i] - 
                         data['InvestPercentage'][i] * (data['Price'][i] * production[i]) 
                         for i in range(data['P']))
objective = net_income - data['UpgradeCost'] * upgrade
problem += objective, "Total_Net_Income"

#### Constraints
#### Machine Capacity Constraint
problem += (pulp.lpSum(data['Hour'][i] * production[i] for i in range(data['P'])) <= 
             data['AvailableHours'] + data['UpgradeHours'] * upgrade), "Machine_Capacity"

#### Cash Availability Constraint
problem += (pulp.lpSum(data['Cost'][i] * production[i] for i in range(data['P'])) <= 
             data['Cash']), "Cash_Availability"

#### Solve the problem
problem.solve()

#### Output the results
production_values = [production[i].varValue for i in range(data['P'])]
upgrade_value = upgrade.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Production quantities: {production_values}')
print(f'Upgrade performed: {bool(upgrade_value)}')
```

