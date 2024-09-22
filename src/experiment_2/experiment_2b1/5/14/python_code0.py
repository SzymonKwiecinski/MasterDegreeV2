import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Extracting parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = pulp.LpVariable.dicts("Production", range(P), lowBound=0, cat='Integer')
upgrade = pulp.LpVariable("Upgrade", cat='Binary')

# Objective function
net_income = pulp.lpSum((price[i] - cost[i] - investPercentage[i] * price[i]) * production[i] for i in range(P)) - upgradeCost * upgrade
problem += net_income

# Constraints
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= availableHours + upgradeHours * upgrade
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) <= cash

# Solve the problem
problem.solve()

# Collecting results
net_income_value = pulp.value(problem.objective)
productions = [production[i].varValue for i in range(P)]
upgrade_value = int(upgrade.varValue)

# Output the results
output = {
    "net_income": net_income_value,
    "production": productions,
    "upgrade": bool(upgrade_value),
}

print(output)
print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')