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

\section*{Linear Programming Model for Production and Investment Optimization}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let $x_i$ be the production quantity of the $i$-th product, where $i = 1, 2, \ldots, P$.
    \item Let $y$ be a binary variable where $y = 1$ if the company upgrades its machine capacity and $y = 0$ otherwise.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $hour_i$: machine hours required for the $i$-th product.
    \item $cost_i$: production cost for the $i$-th product.
    \item $price_i$: selling price of the $i$-th product.
    \item $investPercentage_i$: percentage of the sales revenue made available for financing operations for the $i$-th product.
    \item $upgradeHours$: additional machine hours available after upgrade.
    \item $upgradeCost$: cost of upgrading the machine.
    \item $availableHours$: total machine hours available in the current production period.
    \item $cash$: total available cash for production.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total net income:
\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( (price_i - cost_i) x_i - investPercentage_i \cdot price_i \cdot x_i \right) - upgradeCost \cdot y
\]

\subsection*{Constraints}
1. **Machine Hours Constraint**:
\[
\sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot y
\]
2. **Cash Constraint**:
\[
\sum_{i=1}^{P} cost_i \cdot x_i \leq cash
\]
3. **Non-negativity Constraint**:
\[
x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, P
\]
4. **Binary Variable**:
\[
y \in \{0, 1\}
\]

\subsection*{Output Variables}
- The net income:
\[
\text{net\_income} = Z
\]
- The production quantities:
\[
\text{production} = [x_1, x_2, \ldots, x_P]
\]
- The upgrade decision:
\[
\text{upgrade} = y
\]

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

\section*{Linear Programming Model for Production and Investment Optimization}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let $x_i$ be the production quantity of the $i$-th product, where $i = 1, 2, \ldots, P$.
    \item Let $y$ be a binary variable where $y = 1$ if the company upgrades its machine capacity and $y = 0$ otherwise.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $hour_i$: machine hours required for the $i$-th product.
    \item $cost_i$: production cost for the $i$-th product.
    \item $price_i$: selling price of the $i$-th product.
    \item $investPercentage_i$: percentage of the sales revenue made available for financing operations for the $i$-th product.
    \item $upgradeHours$: additional machine hours available after upgrade.
    \item $upgradeCost$: cost of upgrading the machine.
    \item $availableHours$: total machine hours available in the current production period.
    \item $cash$: total available cash for production.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total net income:
\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( (price_i - cost_i) x_i - investPercentage_i \cdot price_i \cdot x_i \right) - upgradeCost \cdot y
\]

\subsection*{Constraints}
1. **Machine Hours Constraint**:
\[
\sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot y
\]
2. **Cash Constraint**:
\[
\sum_{i=1}^{P} cost_i \cdot x_i \leq cash
\]
3. **Non-negativity Constraint**:
\[
x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, P
\]
4. **Binary Variable**:
\[
y \in \{0, 1\}
\]

\subsection*{Output Variables}
- The net income:
\[
\text{net\_income} = Z
\]
- The production quantities:
\[
\text{production} = [x_1, x_2, \ldots, x_P]
\]
- The upgrade decision:
\[
\text{upgrade} = y
\]

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided in JSON format
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

#### Create the problem variable to contain the problem data
problem = pulp.LpProblem("Production_and_Investment_Optimization", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable('y', cat='Binary')

#### Objective function
profit_terms = [
    (data['Price'][i] - data['Cost'][i]) * x[i] - data['InvestPercentage'][i] * data['Price'][i] * x[i]
    for i in range(data['P'])
]
problem += pulp.lpSum(profit_terms) - data['UpgradeCost'] * y

#### Constraints

#### Machine Hours Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * y

#### Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

