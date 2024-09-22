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

\subsection*{Parameters}
\begin{itemize}
    \item \( P \): Number of different products
    \item \( \text{cash} \): Available cash
    \item \( \text{hour}_i \): Machine hours required for product \( i \)
    \item \( \text{cost}_i \): Production cost per unit of product \( i \)
    \item \( \text{price}_i \): Selling price per unit of product \( i \)
    \item \( \text{investPercentage}_i \): Investment percentage for product \( i \)
    \item \( \text{upgradeHours} \): Additional machine hours available through upgrade
    \item \( \text{upgradeCost} \): Cost of machine upgrade
    \item \( \text{availableHours} \): Current available machine hours
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_i \) be the production quantity of product \( i \) for \( i = 1, \ldots, P \).
    \item Let \( y \) be a binary variable indicating whether to upgrade the machine capacity (1 if upgrade, 0 otherwise).
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:
\[
Z = \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right) - y \cdot \text{upgradeCost}
\]

\subsection*{Constraints}
1. Cash availability constraint:
\[
\sum_{i=1}^{P} \text{cost}_i \cdot x_i + y \cdot \text{upgradeCost} \leq \text{cash}
\]

2. Machine capacity constraint:
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + y \cdot \text{upgradeHours}
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, \ldots, P
\]
\[
y \in \{0, 1\}
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

\subsection*{Parameters}
\begin{itemize}
    \item \( P \): Number of different products
    \item \( \text{cash} \): Available cash
    \item \( \text{hour}_i \): Machine hours required for product \( i \)
    \item \( \text{cost}_i \): Production cost per unit of product \( i \)
    \item \( \text{price}_i \): Selling price per unit of product \( i \)
    \item \( \text{investPercentage}_i \): Investment percentage for product \( i \)
    \item \( \text{upgradeHours} \): Additional machine hours available through upgrade
    \item \( \text{upgradeCost} \): Cost of machine upgrade
    \item \( \text{availableHours} \): Current available machine hours
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_i \) be the production quantity of product \( i \) for \( i = 1, \ldots, P \).
    \item Let \( y \) be a binary variable indicating whether to upgrade the machine capacity (1 if upgrade, 0 otherwise).
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:
\[
Z = \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right) - y \cdot \text{upgradeCost}
\]

\subsection*{Constraints}
1. Cash availability constraint:
\[
\sum_{i=1}^{P} \text{cost}_i \cdot x_i + y \cdot \text{upgradeCost} \leq \text{cash}
\]

2. Machine capacity constraint:
\[
\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + y \cdot \text{upgradeHours}
\]

3. Non-negativity constraints:
\[
x_i \geq 0 \quad \text{for } i = 1, \ldots, P
\]
\[
y \in \{0, 1\}
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

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['P']), lowBound=0)  #### Production quantities
y = pulp.LpVariable("y", cat='Binary')  #### Upgrade decision

#### Objective Function
problem += pulp.lpSum((data['Price'][i] * x[i] - 
                        data['Cost'][i] * x[i] - 
                        data['InvestPercentage'][i] * data['Price'][i] * x[i]) 
                       for i in range(data['P'])) - y * data['UpgradeCost'], "Total_Net_Income"

#### Constraints
#### Cash availability constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) + y * data['UpgradeCost'] <= data['Cash'], "Cash_Constraint"

#### Machine capacity constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + y * data['UpgradeHours'], "Machine_Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

