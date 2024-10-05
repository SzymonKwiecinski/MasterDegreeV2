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

\section*{Linear Programming Model for Production Planning}

We are tasked with creating a linear programming model for maximizing the total net income of a company that produces \( P \) different products, subject to cash availability and machine capacity limitations. Below is the formulation of the problem:

\subsection*{Decision Variables}
\begin{align*}
x_i &: \text{Number of units of product } i \text{ to produce, for } i = 1, 2, \ldots, P. \\
y &: \text{Boolean variable indicating whether to upgrade the machine capacity or not (0/1).}
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{cash} &: \text{Available cash.} \\
\text{hour}_i &: \text{Machine hours required per unit of product } i. \\
\text{cost}_i &: \text{Production cost per unit of product } i. \\
\text{price}_i &: \text{Selling price per unit of product } i. \\
\text{investPercentage}_i &: \text{Investment rate from sales revenue for product } i. \\
\text{upgradeHours} &: \text{Additional machine hours if upgrade is chosen.} \\
\text{upgradeCost} &: \text{Cost required to upgrade the machine capacity.} \\
\text{availableHours} &: \text{Total available machine hours without upgrade.}
\end{align*}

\subsection*{Objective Function}

The objective is to maximize the total net income:
\[
\text{Maximize } \sum_{i=1}^{P} \left( ( \text{price}_i - \text{cost}_i - \text{price}_i \times \text{investPercentage}_i ) x_i \right) - y \times \text{upgradeCost}
\]

\subsection*{Constraints}

1. Machine capacity constraint (with conditional upgrade):
\[
\sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + y \times \text{upgradeHours}
\]

2. Cash constraint:
\[
\sum_{i=1}^{P} \text{cost}_i \times x_i \leq \text{cash} + \sum_{i=1}^{P} \text{price}_i \times \text{investPercentage}_i \times x_i
\]

3. Binary constraint for upgrade decision:
\[
y \in \{0, 1\}
\]

4. Non-negativity constraint for production:
\[
x_i \geq 0, \quad \text{for } i = 1, 2, \ldots, P
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

\section*{Linear Programming Model for Production Planning}

We are tasked with creating a linear programming model for maximizing the total net income of a company that produces \( P \) different products, subject to cash availability and machine capacity limitations. Below is the formulation of the problem:

\subsection*{Decision Variables}
\begin{align*}
x_i &: \text{Number of units of product } i \text{ to produce, for } i = 1, 2, \ldots, P. \\
y &: \text{Boolean variable indicating whether to upgrade the machine capacity or not (0/1).}
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{cash} &: \text{Available cash.} \\
\text{hour}_i &: \text{Machine hours required per unit of product } i. \\
\text{cost}_i &: \text{Production cost per unit of product } i. \\
\text{price}_i &: \text{Selling price per unit of product } i. \\
\text{investPercentage}_i &: \text{Investment rate from sales revenue for product } i. \\
\text{upgradeHours} &: \text{Additional machine hours if upgrade is chosen.} \\
\text{upgradeCost} &: \text{Cost required to upgrade the machine capacity.} \\
\text{availableHours} &: \text{Total available machine hours without upgrade.}
\end{align*}

\subsection*{Objective Function}

The objective is to maximize the total net income:
\[
\text{Maximize } \sum_{i=1}^{P} \left( ( \text{price}_i - \text{cost}_i - \text{price}_i \times \text{investPercentage}_i ) x_i \right) - y \times \text{upgradeCost}
\]

\subsection*{Constraints}

1. Machine capacity constraint (with conditional upgrade):
\[
\sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + y \times \text{upgradeHours}
\]

2. Cash constraint:
\[
\sum_{i=1}^{P} \text{cost}_i \times x_i \leq \text{cash} + \sum_{i=1}^{P} \text{price}_i \times \text{investPercentage}_i \times x_i
\]

3. Binary constraint for upgrade decision:
\[
y \in \{0, 1\}
\]

4. Non-negativity constraint for production:
\[
x_i \geq 0, \quad \text{for } i = 1, 2, \ldots, P
\]

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

#### Create the Linear Programming problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable("y", cat='Binary')

#### Objective Function
profit_contributions = [
    (data['Price'][i] - data['Cost'][i] - data['Price'][i] * data['InvestPercentage'][i]) * x[i]
    for i in range(data['P'])
]
problem += pulp.lpSum(profit_contributions) - y * data['UpgradeCost'], "Total_Net_Income"

#### Constraints
#### Machine capacity constraint with upgrade option
problem += (pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= 
            data['AvailableHours'] + y * data['UpgradeHours']), "Machine_Capacity"

#### Cash constraint
cash_constraints = [
    data['Cost'][i] * x[i] for i in range(data['P'])
]
investment_return = [
    data['Price'][i] * data['InvestPercentage'][i] * x[i] for i in range(data['P'])
]
problem += pulp.lpSum(cash_constraints) <= data['Cash'] + pulp.lpSum(investment_return), "Cash_Availability"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

