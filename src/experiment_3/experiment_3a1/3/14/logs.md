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

Let:
\begin{itemize}
    \item \( P \) be the number of different products.
    \item \( production_i \) be the quantity produced of product \( i \) (for \( i=1, \ldots, P \)).
    \item \( upgrade \) be a binary variable indicating whether to upgrade machine capacity (1 for yes, 0 for no).
\end{itemize}

Define the parameters:
\begin{itemize}
    \item \( cash \): available cash.
    \item \( hour_i \): machine hours required for each unit of product \( i \).
    \item \( cost_i \): production cost per unit of product \( i \).
    \item \( price_i \): selling price per unit of product \( i \).
    \item \( investPercentage_i \): percentage of sales revenue from product \( i \) that will be reinvested.
    \item \( upgradeHours \): additional machine hours available after upgrades.
    \item \( upgradeCost \): cost incurred for upgrading the machine.
    \item \( availableHours \): initial machine hours available.
\end{itemize}

\subsection*{Objective Function}
We aim to maximize the total net income:

\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( (price_i \times production_i) - (cost_i \times production_i) - (investPercentage_i \times price_i \times production_i) \right)
\]

\subsection*{Constraints}

1. **Machine Capacity Constraint**:
\[
\sum_{i=1}^{P} hour_i \times production_i \leq availableHours + (upgrade \times upgradeHours)
\]

2. **Cash Availability Constraint**:
\[
\sum_{i=1}^{P} cost_i \times production_i + upgrade \times upgradeCost \leq cash
\]

3. **Non-negativity Constraints**:
\[
production_i \geq 0 \quad \text{for } i=1, \ldots, P
\]
\[
upgrade \in \{0, 1\}
\]

\subsection*{Outputs}
The results will include:
\begin{itemize}
    \item \( net\_income \): total net income of the company.
    \item \( production \): array of production quantities \( [production_1, production_2, \ldots, production_P] \).
    \item \( upgrade \): a boolean variable indicating whether to upgrade the machine capacity.
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

Let:
\begin{itemize}
    \item \( P \) be the number of different products.
    \item \( production_i \) be the quantity produced of product \( i \) (for \( i=1, \ldots, P \)).
    \item \( upgrade \) be a binary variable indicating whether to upgrade machine capacity (1 for yes, 0 for no).
\end{itemize}

Define the parameters:
\begin{itemize}
    \item \( cash \): available cash.
    \item \( hour_i \): machine hours required for each unit of product \( i \).
    \item \( cost_i \): production cost per unit of product \( i \).
    \item \( price_i \): selling price per unit of product \( i \).
    \item \( investPercentage_i \): percentage of sales revenue from product \( i \) that will be reinvested.
    \item \( upgradeHours \): additional machine hours available after upgrades.
    \item \( upgradeCost \): cost incurred for upgrading the machine.
    \item \( availableHours \): initial machine hours available.
\end{itemize}

\subsection*{Objective Function}
We aim to maximize the total net income:

\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( (price_i \times production_i) - (cost_i \times production_i) - (investPercentage_i \times price_i \times production_i) \right)
\]

\subsection*{Constraints}

1. **Machine Capacity Constraint**:
\[
\sum_{i=1}^{P} hour_i \times production_i \leq availableHours + (upgrade \times upgradeHours)
\]

2. **Cash Availability Constraint**:
\[
\sum_{i=1}^{P} cost_i \times production_i + upgrade \times upgradeCost \leq cash
\]

3. **Non-negativity Constraints**:
\[
production_i \geq 0 \quad \text{for } i=1, \ldots, P
\]
\[
upgrade \in \{0, 1\}
\]

\subsection*{Outputs}
The results will include:
\begin{itemize}
    \item \( net\_income \): total net income of the company.
    \item \( production \): array of production quantities \( [production_1, production_2, \ldots, production_P] \).
    \item \( upgrade \): a boolean variable indicating whether to upgrade the machine capacity.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from provided JSON format
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

#### Define the linear programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Define decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0) for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

#### Define the objective function
net_income = pulp.lpSum((data['Price'][i] * production[i] - data['Cost'][i] * production[i] - 
                          data['InvestPercentage'][i] * data['Price'][i] * production[i]) 
                        for i in range(data['P']))
problem += net_income

#### Define constraints
#### Machine Capacity Constraint
problem += (pulp.lpSum(data['Hour'][i] * production[i] for i in range(data['P'])) 
             <= data['AvailableHours'] + (upgrade * data['UpgradeHours']))

#### Cash Availability Constraint
problem += (pulp.lpSum(data['Cost'][i] * production[i] for i in range(data['P'])) 
             + upgrade * data['UpgradeCost'] <= data['Cash'])

#### Solve the problem
problem.solve()

#### Outputs
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(data['P'])]
upgrade_value = pulp.value(upgrade)

print(f'(Net Income): {net_income_value}')
print(f'(Production Quantities): {production_values}')
print(f'(Upgrade): {upgrade_value}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

