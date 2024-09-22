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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_i \) be the production quantity of the \( i \)-th product, where \( i = 1, \ldots, P \).
    \item Let \( u \) be a binary variable indicating whether the company upgrades its machine capacity (1 if upgraded, 0 otherwise).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{cash} \): Available cash.
    \item \( \text{hour}_i \): Machine hours required for the \( i \)-th product.
    \item \( \text{cost}_i \): Production cost per unit of the \( i \)-th product.
    \item \( \text{price}_i \): Selling price per unit of the \( i \)-th product.
    \item \( \text{investPercentage}_i \): Investment percentage from revenues of the \( i \)-th product.
    \item \( \text{upgradeHours} \): Additional machine hours available through upgrading.
    \item \( \text{upgradeCost} \): Cost to perform the upgrade.
    \item \( \text{availableHours} \): Current available machine hours.
\end{itemize}

\textbf{Objective Function:}
Maximize total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} \left( \text{price}_i x_i - \text{cost}_i x_i - \left( \sum_{i=1}^{P} \text{price}_i x_i \cdot \text{investPercentage}_i \right) \right) - u \cdot \text{upgradeCost}
\]

\textbf{Constraints:}
1. Cash constraint:
\[
\sum_{i=1}^{P} \text{cost}_i x_i + u \cdot \text{upgradeCost} \leq \text{cash}
\]
2. Machine hour constraint:
\[
\sum_{i=1}^{P} \text{hour}_i x_i \leq \text{availableHours} + u \cdot \text{upgradeHours}
\]
3. Non-negativity constraints:
\[
x_i \geq 0 \quad \forall i = 1, \ldots, P
\]
4. Binary constraint for upgrade:
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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_i \) be the production quantity of the \( i \)-th product, where \( i = 1, \ldots, P \).
    \item Let \( u \) be a binary variable indicating whether the company upgrades its machine capacity (1 if upgraded, 0 otherwise).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{cash} \): Available cash.
    \item \( \text{hour}_i \): Machine hours required for the \( i \)-th product.
    \item \( \text{cost}_i \): Production cost per unit of the \( i \)-th product.
    \item \( \text{price}_i \): Selling price per unit of the \( i \)-th product.
    \item \( \text{investPercentage}_i \): Investment percentage from revenues of the \( i \)-th product.
    \item \( \text{upgradeHours} \): Additional machine hours available through upgrading.
    \item \( \text{upgradeCost} \): Cost to perform the upgrade.
    \item \( \text{availableHours} \): Current available machine hours.
\end{itemize}

\textbf{Objective Function:}
Maximize total net income:
\[
\text{Net Income} = \sum_{i=1}^{P} \left( \text{price}_i x_i - \text{cost}_i x_i - \left( \sum_{i=1}^{P} \text{price}_i x_i \cdot \text{investPercentage}_i \right) \right) - u \cdot \text{upgradeCost}
\]

\textbf{Constraints:}
1. Cash constraint:
\[
\sum_{i=1}^{P} \text{cost}_i x_i + u \cdot \text{upgradeCost} \leq \text{cash}
\]
2. Machine hour constraint:
\[
\sum_{i=1}^{P} \text{hour}_i x_i \leq \text{availableHours} + u \cdot \text{upgradeHours}
\]
3. Non-negativity constraints:
\[
x_i \geq 0 \quad \forall i = 1, \ldots, P
\]
4. Binary constraint for upgrade:
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

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

#### Objective function
net_income = pulp.lpSum(data['Price'][i] * x[i] - data['Cost'][i] * x[i] for i in range(data['P'])) \
             - pulp.lpSum(data['Price'][i] * x[i] * data['InvestPercentage'][i] for i in range(data['P'])) \
             - u * data['UpgradeCost']

problem += net_income, "Total_Net_Income"

#### Constraints
#### Cash constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) + u * data['UpgradeCost'] <= data['Cash'], "Cash_Constraint"

#### Machine hours constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + u * data['UpgradeHours'], "Machine_Hour_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

