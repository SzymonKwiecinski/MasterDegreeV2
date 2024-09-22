import pulp
import json

data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

# Parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Create the problem instance
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0) for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = pulp.lpSum(price[i] * production[i] - cost[i] * production[i] - investPercentage[i] * (price[i] * production[i]) for i in range(P)) - upgradeCost * upgrade
problem += net_income

# Constraints
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= availableHours + upgradeHours * upgrade
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) + pulp.lpSum(investPercentage[i] * (price[i] * production[i]) for i in range(P)) <= cash

# Solve the problem
problem.solve()

# Output the results
production_values = [production[i].varValue for i in range(P)]
upgrade_value = upgrade.varValue
net_income_value = pulp.value(problem.objective)

print(f'Production quantities: {production_values}')
print(f'Upgrade machine: {bool(upgrade_value)}')
print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')