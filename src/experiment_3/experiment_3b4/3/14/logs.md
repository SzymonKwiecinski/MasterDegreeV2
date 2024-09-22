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
To solve this problem, we need to formulate a linear programming model to maximize the total net income of the company. The decision variables will be the production quantities of each product and a binary variable indicating whether to upgrade the machine capacity. The constraints will include cash availability, machine capacity, and other problem specifics.

Let's define the decision variables:

- \( x_i \): the production quantity of the \( i \)-th product.
- \( y \): a binary variable indicating whether to upgrade machine capacity (1 if yes, 0 otherwise).

The objective is to maximize the total net income:

\[
\text{maximize} \quad \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right) - \text{upgradeCost} \cdot y
\]

Subject to the following constraints:

1. Machine hours constraint (including potential upgrade):
   \[
   \sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + \text{upgradeHours} \cdot y
   \]

2. Cash availability constraint:
   \[
   \sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \cdot \text{price}_i \cdot x_i - \text{upgradeCost} \cdot y
   \]

3. Binary constraint for the upgrade decision:
   \[
   y \in \{0, 1\}
   \]

Now, let's write this in \(\LaTeX\) format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textit{Decision Variables:}
\begin{itemize}
    \item \( x_i \): Production quantity of product \( i \).
    \item \( y \): Binary variable for machine upgrade, \( y \in \{0, 1\} \).
\end{itemize}

\textit{Objective:} 
\[
\text{Maximize} \quad \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right) - \text{upgradeCost} \cdot y
\]

\textit{Subject to:}
\begin{align*}
    & \sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + \text{upgradeHours} \cdot y \\
    & \sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \cdot \text{price}_i \cdot x_i - \text{upgradeCost} \cdot y \\
    & y \in \{0, 1\}
\end{align*}

\end{document}
```

This model will allow you to determine the optimal production quantities for each product and whether it's beneficial to upgrade the machine capacity in order to maximize the net income.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textit{Decision Variables:}
\begin{itemize}
    \item \( x_i \): Production quantity of product \( i \).
    \item \( y \): Binary variable for machine upgrade, \( y \in \{0, 1\} \).
\end{itemize}

\textit{Objective:} 
\[
\text{Maximize} \quad \sum_{i=1}^{P} \left( \text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i \right) - \text{upgradeCost} \cdot y
\]

\textit{Subject to:}
\begin{align*}
    & \sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + \text{upgradeHours} \cdot y \\
    & \sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \cdot \text{price}_i \cdot x_i - \text{upgradeCost} \cdot y \\
    & y \in \{0, 1\}
\end{align*}

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

#### Create the Linear Programming Problem
problem = pulp.LpProblem("ProductionPlanning", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable('y', cat='Binary')

#### Objective Function
problem += pulp.lpSum([(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]) - data['UpgradeCost'] * y

#### Constraints
problem += pulp.lpSum([data['Hour'][i] * x[i] for i in range(data['P'])]) <= data['AvailableHours'] + data['UpgradeHours'] * y
problem += pulp.lpSum([data['Cost'][i] * x[i] for i in range(data['P'])]) <= data['Cash'] + pulp.lpSum([data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P'])]) - data['UpgradeCost'] * y

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

