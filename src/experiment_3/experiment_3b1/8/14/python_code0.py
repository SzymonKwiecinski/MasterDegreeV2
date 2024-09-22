import pulp
import json

# Given data in JSON format
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

# Extracting data from the dictionary
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, P + 1), lowBound=0, cat='Integer')
u = pulp.LpVariable("u", cat='Binary')

# Objective function
problem += pulp.lpSum([(x[i] * (price[i-1] - cost[i-1] - investPercentage[i-1] * price[i-1])) for i in range(1, P + 1)]) - (upgradeCost * u), "Objective"

# Constraints
problem += pulp.lpSum([hour[i-1] * x[i] for i in range(1, P + 1)]) <= availableHours + upgradeHours * u, "Machine_Hours_Constraint"
problem += pulp.lpSum([cost[i-1] * x[i] for i in range(1, P + 1)]) <= cash, "Cash_Constraint"

# Solve the problem
problem.solve()

# Output results
net_income = pulp.value(problem.objective)
production = [x[i].varValue for i in range(1, P + 1)]
upgrade = u.varValue

print(f' (Objective Value): <OBJ>{net_income}</OBJ>')
print(f'Production: {production}')
print(f'Upgrade: {upgrade}')