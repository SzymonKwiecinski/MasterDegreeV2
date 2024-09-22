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
    \item \( P \) be the number of products.
    \item \( production_i \) be the production quantity of the \( i \)-th product.
    \item \( upgrade \) be a binary variable indicating whether to upgrade machine capacity (1 if yes, 0 otherwise).
    \item \( cash \) be the total available cash.
    \item \( hour_i \) be the machine hours required for product \( i \).
    \item \( cost_i \) be the production cost per unit of product \( i \).
    \item \( price_i \) be the selling price per unit of product \( i \).
    \item \( investPercentage_i \) be the investment percentage for product \( i \).
    \item \( upgradeHours \) be the additional hours gained through upgrading.
    \item \( upgradeCost \) be the cost of the upgrade.
    \item \( availableHours \) be the initial available machine hours.
\end{itemize}

\subsection*{Objective Function}

We aim to maximize the total net income:

\[
\text{Maximize } Z = \sum_{i=1}^{P} (price_i \cdot production_i - cost_i \cdot production_i - investPercentage_i \cdot (price_i \cdot production_i)) 
\]

This simplifies to:

\[
Z = \sum_{i=1}^{P} \left( (price_i - cost_i - investPercentage_i \cdot price_i) \cdot production_i \right)
\]

\subsection*{Constraints}

1. \textbf{Machine Hours Constraint:}
\[
\sum_{i=1}^{P} hour_i \cdot production_i \leq availableHours + upgrade \cdot upgradeHours
\]

2. \textbf{Cash Availability Constraint:}
\[
\sum_{i=1}^{P} (cost_i \cdot production_i + investPercentage_i \cdot (price_i \cdot production_i)) \leq cash + upgrade \cdot upgradeCost
\]

3. \textbf{Non-negativity Constraints:}
\[
production_i \geq 0 \quad \forall i = 1, \ldots, P
\]
\[
upgrade \in \{0, 1\}
\]

\subsection*{Output Variables}

\begin{itemize}
    \item \( net\_income = Z \)
    \item \( production = [production_1, production_2, \ldots, production_P] \)
    \item \( upgrade = true \text{ or } false \)
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
    \item \( P \) be the number of products.
    \item \( production_i \) be the production quantity of the \( i \)-th product.
    \item \( upgrade \) be a binary variable indicating whether to upgrade machine capacity (1 if yes, 0 otherwise).
    \item \( cash \) be the total available cash.
    \item \( hour_i \) be the machine hours required for product \( i \).
    \item \( cost_i \) be the production cost per unit of product \( i \).
    \item \( price_i \) be the selling price per unit of product \( i \).
    \item \( investPercentage_i \) be the investment percentage for product \( i \).
    \item \( upgradeHours \) be the additional hours gained through upgrading.
    \item \( upgradeCost \) be the cost of the upgrade.
    \item \( availableHours \) be the initial available machine hours.
\end{itemize}

\subsection*{Objective Function}

We aim to maximize the total net income:

\[
\text{Maximize } Z = \sum_{i=1}^{P} (price_i \cdot production_i - cost_i \cdot production_i - investPercentage_i \cdot (price_i \cdot production_i)) 
\]

This simplifies to:

\[
Z = \sum_{i=1}^{P} \left( (price_i - cost_i - investPercentage_i \cdot price_i) \cdot production_i \right)
\]

\subsection*{Constraints}

1. \textbf{Machine Hours Constraint:}
\[
\sum_{i=1}^{P} hour_i \cdot production_i \leq availableHours + upgrade \cdot upgradeHours
\]

2. \textbf{Cash Availability Constraint:}
\[
\sum_{i=1}^{P} (cost_i \cdot production_i + investPercentage_i \cdot (price_i \cdot production_i)) \leq cash + upgrade \cdot upgradeCost
\]

3. \textbf{Non-negativity Constraints:}
\[
production_i \geq 0 \quad \forall i = 1, \ldots, P
\]
\[
upgrade \in \{0, 1\}
\]

\subsection*{Output Variables}

\begin{itemize}
    \item \( net\_income = Z \)
    \item \( production = [production_1, production_2, \ldots, production_P] \)
    \item \( upgrade = true \text{ or } false \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0) for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

#### Objective Function
net_income = pulp.lpSum([(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * production[i] for i in range(data['P'])])
problem += net_income, "Total_Net_Income"

#### Constraints
#### Machine Hours Constraint
problem += (pulp.lpSum(data['Hour'][i] * production[i] for i in range(data['P'])) <= data['AvailableHours'] + upgrade * data['UpgradeHours'], "Machine_Hours_Constraint")

#### Cash Availability Constraint
problem += (pulp.lpSum((data['Cost'][i] + data['InvestPercentage'][i] * data['Price'][i]) * production[i] for i in range(data['P'])) <= data['Cash'] + upgrade * data['UpgradeCost'], "Cash_Availability_Constraint")

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

