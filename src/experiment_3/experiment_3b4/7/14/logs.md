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

% Define the given data 
\newcommand{\cash}{\text{cash}}
\newcommand{\hours}{\text{hour}_i}
\newcommand{\cost}{\text{cost}_i}
\newcommand{\price}{\text{price}_i}
\newcommand{\investPercentage}{\text{investPercentage}_i}
\newcommand{\upgradeHours}{\text{upgradeHours}}
\newcommand{\upgradeCost}{\text{upgradeCost}}
\newcommand{\availableHours}{\text{availableHours}}

% Decision variables
% Let x_i be the production quantity of the i-th product.
% Let y be a binary variable representing whether the company upgrades the machine capacity (1 if upgrade, 0 otherwise).

\begin{align*}
\text{Maximize} \quad & \sum_{i=1}^{P} \left(\text{price}_i \times x_i - \text{cost}_i \times x_i - \text{investPercentage}_i \times \text{price}_i \times x_i\right) - \text{upgradeCost} \times y \\
\text{Subject to:} \quad & \sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + \text{upgradeHours} \times y \\
& \sum_{i=1}^{P} \text{cost}_i \times x_i + \text{upgradeCost} \times y \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \times \text{price}_i \times x_i \\
& y \in \{0, 1\} \\
& x_i \geq 0 \quad \forall i
\end{align*}

% The objective function maximizes the net income, which is the total revenue minus the total production costs and investment costs, and the possible upgrade cost.
% The first constraint ensures that the total machine hours used do not exceed the available hours plus any additional hours obtained by upgrading.
% The second constraint ensures that the total cost of production and the upgrade (if chosen) does not exceed the available cash plus the portion of the revenue that can be reinvested.
% The decision variable y is a binary variable that indicates whether the upgrade is selected or not.

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

% Define the given data 
\newcommand{\cash}{\text{cash}}
\newcommand{\hours}{\text{hour}_i}
\newcommand{\cost}{\text{cost}_i}
\newcommand{\price}{\text{price}_i}
\newcommand{\investPercentage}{\text{investPercentage}_i}
\newcommand{\upgradeHours}{\text{upgradeHours}}
\newcommand{\upgradeCost}{\text{upgradeCost}}
\newcommand{\availableHours}{\text{availableHours}}

% Decision variables
% Let x_i be the production quantity of the i-th product.
% Let y be a binary variable representing whether the company upgrades the machine capacity (1 if upgrade, 0 otherwise).

\begin{align*}
\text{Maximize} \quad & \sum_{i=1}^{P} \left(\text{price}_i \times x_i - \text{cost}_i \times x_i - \text{investPercentage}_i \times \text{price}_i \times x_i\right) - \text{upgradeCost} \times y \\
\text{Subject to:} \quad & \sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + \text{upgradeHours} \times y \\
& \sum_{i=1}^{P} \text{cost}_i \times x_i + \text{upgradeCost} \times y \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \times \text{price}_i \times x_i \\
& y \in \{0, 1\} \\
& x_i \geq 0 \quad \forall i
\end{align*}

% The objective function maximizes the net income, which is the total revenue minus the total production costs and investment costs, and the possible upgrade cost.
% The first constraint ensures that the total machine hours used do not exceed the available hours plus any additional hours obtained by upgrading.
% The second constraint ensures that the total cost of production and the upgrade (if chosen) does not exceed the available cash plus the portion of the revenue that can be reinvested.
% The decision variable y is a binary variable that indicates whether the upgrade is selected or not.

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

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable('y', cat='Binary')

#### Objective Function
problem += (
    pulp.lpSum(
        (data['Price'][i] * x[i] - data['Cost'][i] * x[i] - data['InvestPercentage'][i] * data['Price'][i] * x[i])
        for i in range(data['P'])
    ) - data['UpgradeCost'] * y
)

#### Constraints
problem += (
    pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <=
    data['AvailableHours'] + data['UpgradeHours'] * y
)

problem += (
    pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) +
    data['UpgradeCost'] * y <=
    data['Cash'] + pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P']))
)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

