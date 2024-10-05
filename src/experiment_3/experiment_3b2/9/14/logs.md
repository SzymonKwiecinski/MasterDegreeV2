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
To formulate this problem as a Linear Programming (LP) model, we first need to define the decision variables and the constraints.

######### Decision Variables:
1. \( x_i \): Number of units produced of product \( i \) for \( i = 1, \ldots, P \).
2. \( y \): Binary variable indicating whether the company upgrades its machine capacity (\( y = 1 \)) or not (\( y = 0 \)).

######### Objective Function:
Maximize the total net income, which is the sum of net incomes from all products minus any upgrade costs if it is opted for. The net income from product \( i \) is given by:

\[
(\text{price}_i \times x_i) - (\text{cost}_i \times x_i) - (\text{investPercentage}_i \times \text{price}_i \times x_i)
\]

The LP problem can be formalized in LaTeX as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize the net income:

\[
\text{Maximize} \quad \sum_{i=1}^{P} \left( (\text{price}_i - \text{cost}_i - \text{investPercentage}_i \times \text{price}_i) \times x_i \right) - \text{upgradeCost} \times y
\]

\textbf{Subject to:}
\begin{align*}
& \sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + \text{upgradeHours} \times y & \quad \text{(Machine hours constraint)} \\
& \sum_{i=1}^{P} \text{cost}_i \times x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \times \text{price}_i \times x_i - \text{upgradeCost} \times y & \quad \text{(Cash availability constraint)} \\
& x_i \geq 0 & \quad \text{for } i = 1, \ldots, P \\
& y \in \{0, 1\} & \quad \text{(Binary upgrade decision)}
\end{align*}

\end{document}
```

The above formulation captures the constraints and objective of the given problem. The binary variable \( y \) allows us to model the decision of upgrading the machine capacity, and the objective function ensures that the decision made maximizes the net income.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize the net income:

\[
\text{Maximize} \quad \sum_{i=1}^{P} \left( (\text{price}_i - \text{cost}_i - \text{investPercentage}_i \times \text{price}_i) \times x_i \right) - \text{upgradeCost} \times y
\]

\textbf{Subject to:}
\begin{align*}
& \sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + \text{upgradeHours} \times y & \quad \text{(Machine hours constraint)} \\
& \sum_{i=1}^{P} \text{cost}_i \times x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \times \text{price}_i \times x_i - \text{upgradeCost} \times y & \quad \text{(Cash availability constraint)} \\
& x_i \geq 0 & \quad \text{for } i = 1, \ldots, P \\
& y \in \{0, 1\} & \quad \text{(Binary upgrade decision)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

#### Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)  #### Continuous variables for product quantities
y = pulp.LpVariable("y", cat='Binary')  #### Binary variable for upgrade decision

#### Objective function
problem += pulp.lpSum((price[i] - cost[i] - invest_percentage[i] * price[i]) * x[i] for i in range(P)) - upgrade_cost * y, "Net_Income"

#### Constraints
problem += pulp.lpSum(hour[i] * x[i] for i in range(P)) <= available_hours + upgrade_hours * y, "Machine_Hours_Constraint"

problem += pulp.lpSum(cost[i] * x[i] for i in range(P)) <= cash + pulp.lpSum(invest_percentage[i] * price[i] * x[i] for i in range(P)) - upgrade_cost * y, "Cash_Availability_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

