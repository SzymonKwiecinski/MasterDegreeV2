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
To solve this problem, we will create a linear programming model. We'll define decision variables, an objective function, and constraints based on the given problem description. Here's the mathematical formulation of the problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different products.
    \item $\text{cash}$: Available cash for operations.
    \item $\text{hour}_i$: Machine hours required per unit of product $i$, for $i = 1, \dots, P$.
    \item $\text{cost}_i$: Production cost per unit of product $i$, for $i = 1, \dots, P$.
    \item $\text{price}_i$: Selling price per unit of product $i$, for $i = 1, \dots, P$.
    \item $\text{investPercentage}_i$: Investment rate of the revenue from product $i$, for $i = 1, \dots, P$.
    \item $\text{upgradeHours}$: Additional machine hours if the upgrade is performed.
    \item $\text{upgradeCost}$: Cost to upgrade the machine capacity.
    \item $\text{availableHours}$: Available machine hours without upgrade.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Production quantity of product $i$, for $i = 1, \dots, P$.
    \item $y$: Binary variable, $y = 1$ if the machine capacity is upgraded, $y = 0$ otherwise.
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income, which is defined as:
\[
\text{Net Income} = \sum_{i=1}^{P} \left( (\text{price}_i - \text{cost}_i - \text{investPercentage}_i \cdot \text{price}_i) \cdot x_i \right) - \text{upgradeCost} \cdot y
\]

\subsection*{Constraints}
\begin{align}
    &\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + \text{upgradeHours} \cdot y \\
    &\sum_{i=1}^{P} (\text{cost}_i + \text{investPercentage}_i \cdot \text{price}_i) \cdot x_i + \text{upgradeCost} \cdot y \leq \text{cash} \\
    &x_i \geq 0, \quad \text{for all } i = 1, \dots, P \\
    &y \in \{0, 1\}
\end{align}

\end{document}
```

This linear programming model aims to determine the optimal production quantities for each product and whether to upgrade the machine capacity to maximize the total net income under the constraints of cash availability and machine capacity.

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
    \item $P$: Number of different products.
    \item $\text{cash}$: Available cash for operations.
    \item $\text{hour}_i$: Machine hours required per unit of product $i$, for $i = 1, \dots, P$.
    \item $\text{cost}_i$: Production cost per unit of product $i$, for $i = 1, \dots, P$.
    \item $\text{price}_i$: Selling price per unit of product $i$, for $i = 1, \dots, P$.
    \item $\text{investPercentage}_i$: Investment rate of the revenue from product $i$, for $i = 1, \dots, P$.
    \item $\text{upgradeHours}$: Additional machine hours if the upgrade is performed.
    \item $\text{upgradeCost}$: Cost to upgrade the machine capacity.
    \item $\text{availableHours}$: Available machine hours without upgrade.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Production quantity of product $i$, for $i = 1, \dots, P$.
    \item $y$: Binary variable, $y = 1$ if the machine capacity is upgraded, $y = 0$ otherwise.
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income, which is defined as:
\[
\text{Net Income} = \sum_{i=1}^{P} \left( (\text{price}_i - \text{cost}_i - \text{investPercentage}_i \cdot \text{price}_i) \cdot x_i \right) - \text{upgradeCost} \cdot y
\]

\subsection*{Constraints}
\begin{align}
    &\sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + \text{upgradeHours} \cdot y \\
    &\sum_{i=1}^{P} (\text{cost}_i + \text{investPercentage}_i \cdot \text{price}_i) \cdot x_i + \text{upgradeCost} \cdot y \leq \text{cash} \\
    &x_i \geq 0, \quad \text{for all } i = 1, \dots, P \\
    &y \in \{0, 1\}
\end{align}

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
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable("y", cat='Binary')

#### Objective Function
net_income = pulp.lpSum(
    [(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]
) - data['UpgradeCost'] * y
problem += net_income

#### Constraints
#### Machine hours constraint
machine_hours_constraint = pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * y
problem += machine_hours_constraint

#### Cash constraint
cash_constraint = pulp.lpSum(
    [(data['Cost'][i] + data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]
) + data['UpgradeCost'] * y <= data['Cash']
problem += cash_constraint

#### Solve
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

