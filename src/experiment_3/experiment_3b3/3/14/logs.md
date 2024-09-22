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

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_i \) be the quantity produced of product \( i \) for \( i = 1, 2, \ldots, P \).
    \item Let \( u \) be a binary variable where \( u = 1 \) indicates that the machine capacity is upgraded, and \( u = 0 \) otherwise.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{cash} \): Available cash
    \item \( \text{hour}_i \): Machine hours required per unit of product \( i \)
    \item \( \text{cost}_i \): Production cost per unit of product \( i \)
    \item \( \text{price}_i \): Selling price per unit of product \( i \)
    \item \( \text{investPercentage}_i \): Investment percentage of sales revenue for product \( i \)
    \item \( \text{upgradeHours} \): Additional machine hours available if upgraded
    \item \( \text{upgradeCost} \): Cost of upgrading the machine
    \item \( \text{availableHours} \): Current available machine hours
\end{itemize}

\textbf{Objective Function:}

Maximize total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot (\text{price}_i \cdot x_i) \right) - u \cdot \text{upgradeCost}
\]

\textbf{Constraints:}

1. Cash Availability Constraint:
\[
\sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash}
\]

2. Machine Capacity Constraint:
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + u \cdot \text{upgradeHours}
\]

3. Non-negativity and Binary Constraints:
\[
x_i \geq 0 \quad \forall i
\]
\[
u \in \{0, 1\}
\]

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{net\_income} \): Total net income of the company
    \item \( \text{production}_i \): Production quantity of the \( i \)-th product
    \item \( \text{upgrade} \): Upgrade status of the machine (true/false)
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

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_i \) be the quantity produced of product \( i \) for \( i = 1, 2, \ldots, P \).
    \item Let \( u \) be a binary variable where \( u = 1 \) indicates that the machine capacity is upgraded, and \( u = 0 \) otherwise.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{cash} \): Available cash
    \item \( \text{hour}_i \): Machine hours required per unit of product \( i \)
    \item \( \text{cost}_i \): Production cost per unit of product \( i \)
    \item \( \text{price}_i \): Selling price per unit of product \( i \)
    \item \( \text{investPercentage}_i \): Investment percentage of sales revenue for product \( i \)
    \item \( \text{upgradeHours} \): Additional machine hours available if upgraded
    \item \( \text{upgradeCost} \): Cost of upgrading the machine
    \item \( \text{availableHours} \): Current available machine hours
\end{itemize}

\textbf{Objective Function:}

Maximize total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot (\text{price}_i \cdot x_i) \right) - u \cdot \text{upgradeCost}
\]

\textbf{Constraints:}

1. Cash Availability Constraint:
\[
\sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash}
\]

2. Machine Capacity Constraint:
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + u \cdot \text{upgradeHours}
\]

3. Non-negativity and Binary Constraints:
\[
x_i \geq 0 \quad \forall i
\]
\[
u \in \{0, 1\}
\]

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{net\_income} \): Total net income of the company
    \item \( \text{production}_i \): Production quantity of the \( i \)-th product
    \item \( \text{upgrade} \): Upgrade status of the machine (true/false)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Problem
problem = pulp.LpProblem("Product_Production", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

#### Objective Function
profit_terms = [(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]
problem += pulp.lpSum(profit_terms) - u * data['UpgradeCost'], "Net Income"

#### Constraints
#### Cash Availability Constraint
problem += pulp.lpSum([data['Cost'][i] * x[i] for i in range(data['P'])]) <= data['Cash'], "Cash Constraint"

#### Machine Capacity Constraint
problem += pulp.lpSum([data['Hour'][i] * x[i] for i in range(data['P'])]) <= data['AvailableHours'] + u * data['UpgradeHours'], "Machine Capacity"

#### Solve
problem.solve()

#### Output
production = [pulp.value(x[i]) for i in range(data['P'])]
upgrade = bool(pulp.value(u))
net_income = pulp.value(problem.objective)

for i, qty in enumerate(production):
    print(f'Production quantity for product {i+1}: {qty}')
print(f'Upgrade status of the machine: {upgrade}')
print(f'Net Income: {net_income}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

