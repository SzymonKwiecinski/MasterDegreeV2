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

\section*{Linear Programming Model for Maximizing Net Income}

\textbf{Parameters:}
\begin{itemize}
    \item Let \( P \) be the number of different products.
    \item Let \( \text{cash} \) be the available cash.
    \item Let \( \text{hour}_i \) be the machine hours required for product \( i \) where \( i \in \{1, 2, \ldots, P\} \).
    \item Let \( \text{cost}_i \) be the production cost per unit of product \( i \).
    \item Let \( \text{price}_i \) be the selling price per unit of product \( i \).
    \item Let \( \text{investPercentage}_i \) be the percentage of sales revenue from product \( i \) allocated for operations.
    \item Let \( \text{upgradeHours} \) be the additional machine hours available through upgrading.
    \item Let \( \text{upgradeCost} \) be the cost of upgrading the machine.
    \item Let \( \text{availableHours} \) be the current available machine hours.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_i \) be the quantity produced of product \( i \).
    \item Let \( \text{upgrade} \in \{0, 1\} \) be a binary variable indicating whether the company chooses to upgrade its machine capacity (1 for yes, 0 for no).
\end{itemize}

\textbf{Objective Function:}
We aim to maximize the total net income given by:
\[
\max \quad \text{net\_income} = \sum_{i=1}^{P} \left( ( \text{price}_i - \text{cost}_i - \text{investPercentage}_i \cdot \text{price}_i ) \cdot x_i \right) - \text{upgradeCost} \cdot \text{upgrade}
\]

\textbf{Constraints:}
1. **Cash Constraint:**
\[
\sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} - \text{investPercentage}_i \cdot \text{price}_i \cdot \sum_{i=1}^{P} x_i \cdot \text{upgrade}
\]

2. **Machine Hours Constraint:**
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + \text{upgradeHours} \cdot \text{upgrade}
\]

3. **Non-negativity Constraints:**
\[
x_i \geq 0 \quad \forall i \in \{1, 2, \ldots, P\}
\]
\[
\text{upgrade} \in \{0, 1\}
\]

\textbf{Output Variables:}
\begin{itemize}
    \item The net income is given by \( \text{net\_income} \).
    \item The production quantities are given by \( x_i \) for \( i \in \{1, 2, \ldots, P\} \).
    \item The variable \( \text{upgrade} \) indicates whether an upgrade is performed or not.
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

\section*{Linear Programming Model for Maximizing Net Income}

\textbf{Parameters:}
\begin{itemize}
    \item Let \( P \) be the number of different products.
    \item Let \( \text{cash} \) be the available cash.
    \item Let \( \text{hour}_i \) be the machine hours required for product \( i \) where \( i \in \{1, 2, \ldots, P\} \).
    \item Let \( \text{cost}_i \) be the production cost per unit of product \( i \).
    \item Let \( \text{price}_i \) be the selling price per unit of product \( i \).
    \item Let \( \text{investPercentage}_i \) be the percentage of sales revenue from product \( i \) allocated for operations.
    \item Let \( \text{upgradeHours} \) be the additional machine hours available through upgrading.
    \item Let \( \text{upgradeCost} \) be the cost of upgrading the machine.
    \item Let \( \text{availableHours} \) be the current available machine hours.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_i \) be the quantity produced of product \( i \).
    \item Let \( \text{upgrade} \in \{0, 1\} \) be a binary variable indicating whether the company chooses to upgrade its machine capacity (1 for yes, 0 for no).
\end{itemize}

\textbf{Objective Function:}
We aim to maximize the total net income given by:
\[
\max \quad \text{net\_income} = \sum_{i=1}^{P} \left( ( \text{price}_i - \text{cost}_i - \text{investPercentage}_i \cdot \text{price}_i ) \cdot x_i \right) - \text{upgradeCost} \cdot \text{upgrade}
\]

\textbf{Constraints:}
1. **Cash Constraint:**
\[
\sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} - \text{investPercentage}_i \cdot \text{price}_i \cdot \sum_{i=1}^{P} x_i \cdot \text{upgrade}
\]

2. **Machine Hours Constraint:**
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + \text{upgradeHours} \cdot \text{upgrade}
\]

3. **Non-negativity Constraints:**
\[
x_i \geq 0 \quad \forall i \in \{1, 2, \ldots, P\}
\]
\[
\text{upgrade} \in \{0, 1\}
\]

\textbf{Output Variables:}
\begin{itemize}
    \item The net income is given by \( \text{net\_income} \).
    \item The production quantities are given by \( x_i \) for \( i \in \{1, 2, \ldots, P\} \).
    \item The variable \( \text{upgrade} \) indicates whether an upgrade is performed or not.
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
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 
        'UpgradeCost': 400, 'AvailableHours': 2000}

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

#### Problem Definition
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')
upgrade = pulp.LpVariable("upgrade", cat='Binary')

#### Objective Function
net_income = pulp.lpSum((price[i] - cost[i] - investPercentage[i] * price[i]) * x[i] for i in range(P))
                        - upgradeCost * upgrade
problem += net_income

#### Constraints
#### Cash Constraint
problem += (pulp.lpSum(cost[i] * x[i] for i in range(P)) <= 
             cash - pulp.lpSum(investPercentage[i] * price[i] * x[i] for i in range(P)) * upgrade)

#### Machine Hours Constraint
problem += (pulp.lpSum(hour[i] * x[i] for i in range(P)) <= 
             availableHours + upgradeHours * upgrade)

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

