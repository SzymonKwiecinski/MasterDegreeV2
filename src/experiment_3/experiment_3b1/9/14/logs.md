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

\subsection*{Variables}
Let \( x_i \) be the production quantity of the \( i \)-th product, where \( i = 1, \ldots, P \).  
Let \( u \) be a binary variable indicating whether the company should upgrade its machine capacity (1 if upgrade is performed, 0 otherwise).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{cash} \): Available cash
    \item \( \text{hour}_i \): Machine hours required for the \( i \)-th product
    \item \( \text{cost}_i \): Production cost of the \( i \)-th product
    \item \( \text{price}_i \): Selling price of the \( i \)-th product
    \item \( \text{investPercentage}_i \): Investment percentage of the sales revenue from the \( i \)-th product
    \item \( \text{upgradeHours} \): Additional machine hours available after upgrade
    \item \( \text{upgradeCost} \): Cost of upgrading machine capacity
    \item \( \text{availableHours} \): Initial available machine hours
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} (price_i \cdot x_i - cost_i \cdot x_i - investPercentage_i \cdot price_i \cdot x_i) - upgradeCost \cdot u
\]
This can be simplified to:
\[
\text{Net Income} = \sum_{i=1}^{P} (price_i \cdot (1 - investPercentage_i) \cdot x_i) - upgradeCost \cdot u
\]

\subsection*{Constraints}
1. Cash availability constraint:
\[
\sum_{i=1}^{P} cost_i \cdot x_i + upgradeCost \cdot u \leq cash
\]

2. Machine hours constraint:
\[
\sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot u
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, \ldots, P
\]
\[
u \in \{0, 1\}
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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( x_i \) be the production quantity of the \( i \)-th product, where \( i = 1, \ldots, P \).  
Let \( u \) be a binary variable indicating whether the company should upgrade its machine capacity (1 if upgrade is performed, 0 otherwise).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{cash} \): Available cash
    \item \( \text{hour}_i \): Machine hours required for the \( i \)-th product
    \item \( \text{cost}_i \): Production cost of the \( i \)-th product
    \item \( \text{price}_i \): Selling price of the \( i \)-th product
    \item \( \text{investPercentage}_i \): Investment percentage of the sales revenue from the \( i \)-th product
    \item \( \text{upgradeHours} \): Additional machine hours available after upgrade
    \item \( \text{upgradeCost} \): Cost of upgrading machine capacity
    \item \( \text{availableHours} \): Initial available machine hours
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} (price_i \cdot x_i - cost_i \cdot x_i - investPercentage_i \cdot price_i \cdot x_i) - upgradeCost \cdot u
\]
This can be simplified to:
\[
\text{Net Income} = \sum_{i=1}^{P} (price_i \cdot (1 - investPercentage_i) \cdot x_i) - upgradeCost \cdot u
\]

\subsection*{Constraints}
1. Cash availability constraint:
\[
\sum_{i=1}^{P} cost_i \cdot x_i + upgradeCost \cdot u \leq cash
\]

2. Machine hours constraint:
\[
\sum_{i=1}^{P} hour_i \cdot x_i \leq availableHours + upgradeHours \cdot u
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, \ldots, P
\]
\[
u \in \{0, 1\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
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

#### Define decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

#### Objective function
net_income = pulp.lpSum([(data['Price'][i] * (1 - data['InvestPercentage'][i]) * x[i]) for i in range(data['P'])]) - (data['UpgradeCost'] * u)
problem += net_income

#### Constraints
#### Cash availability constraint
problem += (pulp.lpSum([data['Cost'][i] * x[i] for i in range(data['P'])]) + (data['UpgradeCost'] * u) <= data['Cash']), "Cash_Constraint")

#### Machine hours constraint
problem += (pulp.lpSum([data['Hour'][i] * x[i] for i in range(data['P'])]) <= (data['AvailableHours'] + data['UpgradeHours'] * u)), "Machine_Hours_Constraint")

#### Solve the problem
problem.solve()

#### Result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
```python
import pulp
import json

#### Given data
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

#### Define decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

#### Objective function
net_income = pulp.lpSum([(data['Price'][i] * (1 - data['InvestPercentage'][i]) * x[i]) for i in range(data['P'])]) - (data['UpgradeCost'] * u)
problem += net_income

#### Constraints
#### Cash availability constraint
problem += (pulp.lpSum([data['Cost'][i] * x[i] for i in range(data['P'])]) + (data['UpgradeCost'] * u) <= data['Cash']), "Cash_Constraint")

#### Machine hours constraint
problem += (pulp.lpSum([data['Hour'][i] * x[i] for i in range(data['P'])]) <= (data['AvailableHours'] + data['UpgradeHours'] * u)), "Machine_Hours_Constraint")

#### Solve the problem
problem.solve()

#### Result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/9/14/python_code0.py", line 30
    problem += (pulp.lpSum([data['Cost'][i] * x[i] for i in range(data['P'])]) + (data['UpgradeCost'] * u) <= data['Cash']), "Cash_Constraint")
                                                                                                                                              ^
SyntaxError: unmatched ')'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
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

#### Define decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

#### Objective function
net_income = pulp.lpSum([(data['Price'][i] * (1 - data['InvestPercentage'][i]) * x[i]) for i in range(data['P'])]) - (data['UpgradeCost'] * u)
problem += net_income

#### Constraints
#### Cash availability constraint
problem += (pulp.lpSum([data['Cost'][i] * x[i] for i in range(data['P'])]) + (data['UpgradeCost'] * u) <= data['Cash']), "Cash_Constraint")

#### Machine hours constraint
problem += (pulp.lpSum([data['Hour'][i] * x[i] for i in range(data['P'])]) <= (data['AvailableHours'] + data['UpgradeHours'] * u)), "Machine_Hours_Constraint")

#### Solve the problem
problem.solve()

#### Result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

