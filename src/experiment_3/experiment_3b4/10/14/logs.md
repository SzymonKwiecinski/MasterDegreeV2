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
The problem at hand is a linear programming problem aiming at maximizing total net income for a company that produces \texttt{P} different products. The company has constraints in terms of cash availability and machine capacity. We will construct a mathematical model to solve this Linear Programming (LP) problem.

To set up this LP problem, let's define the decision variables:

1. \( x_i \): Number of units to produce for product \( i \).
2. \( u \): A binary decision variable that indicates whether the company should upgrade its machine hours (1 if upgrade, 0 otherwise).

The objective is to maximize the total net income. The net income for each product is the revenue from sales minus production cost and investment cost.

The LP formulation can be defined as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation}

\textbf{Objective Function:}

Maximize
\[
Z = \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right)
\]

\textbf{Subject to:}

1. Cash Constraint:
\[
\sum_{i=1}^{P} \left( \text{cost}_i \cdot x_i + \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right) + u \cdot \text{upgradeCost} \leq \text{cash}
\]

2. Machine Hours Constraint:
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + u \cdot \text{upgradeHours}
\]

3. Non-negativity and Binary Constraints:
\[
x_i \geq 0, \quad \forall i = 1, 2, \ldots, P
\]
\[
u \in \{0, 1\}
\]

\textbf{Decision Variables:}

- \( x_i \): Number of units to produce of product \( i \).
- \( u \): Binary variable for upgrading machine hours (1 if upgraded, 0 otherwise).

\end{document}
```

This LP model aims at maximizing the net income while taking into consideration the constraints on cash available and machine hours. The decision variable \( u \) determines if it's beneficial to upgrade the machinery capacity by spending the upgrade cost. The solution of this model will provide the optimal production quantities for each product, the net income, and whether the upgrade should occur.

Please ensure to replace the variables and indices with the actual data values when implementing this model in a solver.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation}

\textbf{Objective Function:}

Maximize
\[
Z = \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right)
\]

\textbf{Subject to:}

1. Cash Constraint:
\[
\sum_{i=1}^{P} \left( \text{cost}_i \cdot x_i + \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right) + u \cdot \text{upgradeCost} \leq \text{cash}
\]

2. Machine Hours Constraint:
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + u \cdot \text{upgradeHours}
\]

3. Non-negativity and Binary Constraints:
\[
x_i \geq 0, \quad \forall i = 1, 2, \ldots, P
\]
\[
u \in \{0, 1\}
\]

\textbf{Decision Variables:}

- \( x_i \): Number of units to produce of product \( i \).
- \( u \): Binary variable for upgrading machine hours (1 if upgraded, 0 otherwise).

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

#### Unpack data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(P)]
u = pulp.LpVariable("u", cat='Binary')

#### Objective Function
problem += pulp.lpSum(
    price[i] * x[i] - cost[i] * x[i] - invest_percentage[i] * price[i] * x[i] for i in range(P)
)

#### Cash Constraint
problem += pulp.lpSum(
    cost[i] * x[i] + invest_percentage[i] * price[i] * x[i] for i in range(P)
) + u * upgrade_cost <= cash

#### Machine Hours Constraint
problem += pulp.lpSum(
    hour[i] * x[i] for i in range(P)
) <= available_hours + u * upgrade_hours

#### Solve
problem.solve()

#### Result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

