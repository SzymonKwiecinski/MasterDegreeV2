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

\section*{Linear Programming Model for Production Optimization}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: quantity produced of product $i$ for $i = 1, \ldots, P$
    \item $y$: boolean variable indicating whether to upgrade the machine capacity (1 for yes, 0 for no)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $cash$: available cash
    \item $hour_i$: machine hours required for product $i$
    \item $cost_i$: production cost per unit of product $i$
    \item $price_i$: selling price per unit of product $i$
    \item $investPercentage_i$: investment percentage from sales revenue of product $i$
    \item $upgradeHours$: additional machine hours available if upgraded
    \item $upgradeCost$: cost to upgrade machine capacity
    \item $availableHours$: current available machine hours
\end{itemize}

\textbf{Objective Function:}
Maximize total net income:
\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( price_i \cdot x_i - cost_i \cdot x_i - investPercentage_i \cdot (price_i \cdot x_i) \right) - upgradeCost \cdot y
\]

\textbf{Constraints:}
\begin{align*}
1. & \quad \sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot y \quad \text{(Machine Hours Constraint)} \\
2. & \quad \sum_{i=1}^{P} cost_i \cdot x_i \leq cash \quad \text{(Cash Availability Constraint)} \\
3. & \quad x_i \geq 0 \quad \forall i \quad \text{(Non-negativity Constraint)} \\
4. & \quad y \in \{0, 1\} \quad \text{(Boolean Upgrade Decision)}
\end{align*}

\textbf{Output Variables:}
\begin{itemize}
    \item $net\_income$: total net income of the company
    \item $production_i$: production quantity of product $i$
    \item $upgrade$: whether to upgrade the machine capacity (true/false)
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

\section*{Linear Programming Model for Production Optimization}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: quantity produced of product $i$ for $i = 1, \ldots, P$
    \item $y$: boolean variable indicating whether to upgrade the machine capacity (1 for yes, 0 for no)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $cash$: available cash
    \item $hour_i$: machine hours required for product $i$
    \item $cost_i$: production cost per unit of product $i$
    \item $price_i$: selling price per unit of product $i$
    \item $investPercentage_i$: investment percentage from sales revenue of product $i$
    \item $upgradeHours$: additional machine hours available if upgraded
    \item $upgradeCost$: cost to upgrade machine capacity
    \item $availableHours$: current available machine hours
\end{itemize}

\textbf{Objective Function:}
Maximize total net income:
\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( price_i \cdot x_i - cost_i \cdot x_i - investPercentage_i \cdot (price_i \cdot x_i) \right) - upgradeCost \cdot y
\]

\textbf{Constraints:}
\begin{align*}
1. & \quad \sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot y \quad \text{(Machine Hours Constraint)} \\
2. & \quad \sum_{i=1}^{P} cost_i \cdot x_i \leq cash \quad \text{(Cash Availability Constraint)} \\
3. & \quad x_i \geq 0 \quad \forall i \quad \text{(Non-negativity Constraint)} \\
4. & \quad y \in \{0, 1\} \quad \text{(Boolean Upgrade Decision)}
\end{align*}

\textbf{Output Variables:}
\begin{itemize}
    \item $net\_income$: total net income of the company
    \item $production_i$: production quantity of product $i$
    \item $upgrade$: whether to upgrade the machine capacity (true/false)
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

P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

#### Define problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(P)]
y = pulp.LpVariable('y', cat='Binary')

#### Objective Function
problem += pulp.lpSum([(price[i] * x[i] - cost[i] * x[i] - investPercentage[i] * price[i] * x[i]) for i in range(P)]) - upgradeCost * y, "Net_Income"

#### Constraints
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= availableHours + upgradeHours * y, "Machine_Hours_Constraint"
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash, "Cash_Constraint"

#### Solve
problem.solve()

print("Optimization Results:")
for i in range(P):
    print(f"Production of product {i+1}: {x[i].varValue}")

print(f"Upgrade Machine: {'Yes' if y.varValue == 1 else 'No'}")
print(f"Net Income (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

