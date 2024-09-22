# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
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
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data in JSON format
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 
        'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 
        'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

#### Extract data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

#### Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision variables
production = pulp.LpVariable.dicts("Production", range(P), lowBound=0, cat='Continuous')
upgrade = pulp.LpVariable("Upgrade", cat='Binary')

#### Objective function: Maximize total net income
net_income = pulp.lpSum((price[i] * production[i] * (1 - investPercentage[i])) - (cost[i] * production[i]) 
                         for i in range(P))

#### Add the cost of upgrading machine capacity
if upgrade:
    available_hours = availableHours + upgradeHours
else:
    available_hours = availableHours

#### Constraints
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= available_hours, "Machine_Hour_Capacity"
problem += pulp.lpSum((price[i] * production[i]) * investPercentage[i] for i in range(P)) <= cash - upgradeCost * upgrade, "Cash_Availability"

#### Define the objective
problem += net_income

#### Solve the problem
problem.solve()

#### Extract results
net_income_value = pulp.value(problem.objective)
production_values = [production[i].varValue for i in range(P)]
upgrade_value = upgrade.varValue

#### Print results
output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')
```

