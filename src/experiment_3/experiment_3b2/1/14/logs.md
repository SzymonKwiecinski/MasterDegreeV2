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
To address this linear programming problem, we need to develop a mathematical model that maximizes the total net income while considering the constraints given. Below is the LaTeX representation of the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_i &: \text{Production quantity of product } i, \quad i = 1, 2, \ldots, P \\
y &: \text{Binary variable indicating if machine capacity is upgraded (1 if yes, 0 otherwise)}
\end{align*}

\subsection*{Objective Function}
Maximize the total net income:
\begin{align*}
\text{Maximize } & \quad \sum_{i=1}^{P} \left( (price_i - cost_i) \cdot x_i - investPercentage_i \cdot price_i \cdot x_i \right) - upgradeCost \cdot y
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{Cash Constraint: } & \quad \sum_{i=1}^{P} cost_i \cdot x_i \leq cash + \sum_{i=1}^{P} investPercentage_i \cdot price_i \cdot x_i \\
\text{Machine Capacity Constraint: } & \quad \sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot y \\
\text{Binary Constraint: } & \quad y \in \{0, 1\} \\
\text{Non-negativity: } & \quad x_i \geq 0, \quad i = 1, 2, \ldots, P
\end{align*}

\end{document}
```

This model seeks to maximize the total net income derived from producing and selling the products, considering the production costs, selling prices, and potential investment returns as per the constraints of cash availability and machine capacity. The decision variable \( y \) is a binary variable that determines whether or not to upgrade machine capacity, factoring in the associated cost.

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

\subsection*{Decision Variables}
\begin{align*}
x_i &: \text{Production quantity of product } i, \quad i = 1, 2, \ldots, P \\
y &: \text{Binary variable indicating if machine capacity is upgraded (1 if yes, 0 otherwise)}
\end{align*}

\subsection*{Objective Function}
Maximize the total net income:
\begin{align*}
\text{Maximize } & \quad \sum_{i=1}^{P} \left( (price_i - cost_i) \cdot x_i - investPercentage_i \cdot price_i \cdot x_i \right) - upgradeCost \cdot y
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{Cash Constraint: } & \quad \sum_{i=1}^{P} cost_i \cdot x_i \leq cash + \sum_{i=1}^{P} investPercentage_i \cdot price_i \cdot x_i \\
\text{Machine Capacity Constraint: } & \quad \sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot y \\
\text{Binary Constraint: } & \quad y \in \{0, 1\} \\
\text{Non-negativity: } & \quad x_i \geq 0, \quad i = 1, 2, \ldots, P
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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

#### Initialize the Linear Programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]  #### Production quantities
y = pulp.LpVariable('y', cat='Binary')  #### Upgrade variable

#### Objective Function
profit = pulp.lpSum((data['Price'][i] - data['Cost'][i]) * x[i] - data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P']))
problem += profit - data['UpgradeCost'] * y, "Total_Net_Income"

#### Constraints
#### Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash'] + pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P'])), "Cash_Constraint"

#### Machine Capacity Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * y, "Machine_Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

