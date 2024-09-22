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
    \item \( P \): Number of different products
    \item \( hour_i \): Machine hours required for product \( i \) (for \( i = 1, \ldots, P \))
    \item \( cost_i \): Production cost per unit of product \( i \) (for \( i = 1, \ldots, P \))
    \item \( price_i \): Selling price per unit of product \( i \) (for \( i = 1, \ldots, P \))
    \item \( investPercentage_i \): Investment percentage from sales revenues of product \( i \) (for \( i = 1, \ldots, P \))
    \item \( availableHours \): Available machine hours
    \item \( cash \): Available cash
    \item \( upgradeHours \): Possible machine hours to upgrade
    \item \( upgradeCost \): Cost to upgrade machine hours
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( production_i \): Quantity to produce of product \( i \) (for \( i = 1, \ldots, P \))
    \item \( upgrade \): Boolean variable indicating whether to upgrade machine capacity (1 if yes, 0 if no)
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize } net\_income = \sum_{i=1}^{P} \left( (price_i - cost_i) \cdot production_i - investPercentage_i \cdot (price_i \cdot production_i) \right) - upgradeCost \cdot upgrade
\end{align*}

\textbf{Subject to:}

\textbf{1. Machine Capacity Constraint:}
\begin{align*}
    \sum_{i=1}^{P} hour_i \cdot production_i \leq availableHours + upgradeHours \cdot upgrade
\end{align*}

\textbf{2. Cash Constraint:}
\begin{align*}
    \sum_{i=1}^{P} cost_i \cdot production_i \leq cash
\end{align*}

\textbf{3. Non-negativity Restrictions:}
\begin{align*}
    production_i \geq 0 \quad \forall i \in \{1, \ldots, P\} \\
    upgrade \in \{0, 1\}
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

\textbf{Parameters:}
\begin{itemize}
    \item \( P \): Number of different products
    \item \( hour_i \): Machine hours required for product \( i \) (for \( i = 1, \ldots, P \))
    \item \( cost_i \): Production cost per unit of product \( i \) (for \( i = 1, \ldots, P \))
    \item \( price_i \): Selling price per unit of product \( i \) (for \( i = 1, \ldots, P \))
    \item \( investPercentage_i \): Investment percentage from sales revenues of product \( i \) (for \( i = 1, \ldots, P \))
    \item \( availableHours \): Available machine hours
    \item \( cash \): Available cash
    \item \( upgradeHours \): Possible machine hours to upgrade
    \item \( upgradeCost \): Cost to upgrade machine hours
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( production_i \): Quantity to produce of product \( i \) (for \( i = 1, \ldots, P \))
    \item \( upgrade \): Boolean variable indicating whether to upgrade machine capacity (1 if yes, 0 if no)
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize } net\_income = \sum_{i=1}^{P} \left( (price_i - cost_i) \cdot production_i - investPercentage_i \cdot (price_i \cdot production_i) \right) - upgradeCost \cdot upgrade
\end{align*}

\textbf{Subject to:}

\textbf{1. Machine Capacity Constraint:}
\begin{align*}
    \sum_{i=1}^{P} hour_i \cdot production_i \leq availableHours + upgradeHours \cdot upgrade
\end{align*}

\textbf{2. Cash Constraint:}
\begin{align*}
    \sum_{i=1}^{P} cost_i \cdot production_i \leq cash
\end{align*}

\textbf{3. Non-negativity Restrictions:}
\begin{align*}
    production_i \geq 0 \quad \forall i \in \{1, \ldots, P\} \\
    upgrade \in \{0, 1\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads("{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}")

#### Parameters
P = data['P']
availableHours = data['AvailableHours']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']

#### Define the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision variables
production = [pulp.LpVariable(f'production_{i+1}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

#### Objective function
net_income = pulp.lpSum([(price[i] - cost[i]) * production[i] - investPercentage[i] * (price[i] * production[i]) for i in range(P)]) - upgradeCost * upgrade
problem += net_income

#### Constraints
problem += pulp.lpSum([hour[i] * production[i] for i in range(P)]) <= availableHours + upgradeHours * upgrade
problem += pulp.lpSum([cost[i] * production[i] for i in range(P)]) <= cash

#### Solve the problem
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

