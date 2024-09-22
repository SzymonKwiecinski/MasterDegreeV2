import pulp
import json

# Data input
data = json.loads("{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}")

# Parameters
P = data['P']
availableHours = data['AvailableHours']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']

# Define the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i+1}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function
net_income = pulp.lpSum([(price[i] - cost[i]) * production[i] - investPercentage[i] * (price[i] * production[i]) for i in range(P)]) - upgradeCost * upgrade
problem += net_income

# Constraints
problem += pulp.lpSum([hour[i] * production[i] for i in range(P)]) <= availableHours + upgradeHours * upgrade
problem += pulp.lpSum([cost[i] * production[i] for i in range(P)]) <= cash

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')