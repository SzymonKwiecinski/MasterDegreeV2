import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Extract data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Create a problem variable
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = pulp.lpSum((price[i] - cost[i] - (investPercentage[i] * (price[i] - cost[i]))) * production[i] for i in range(P))
problem += net_income

# Constraints
# Cash constraint
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) + (upgradeCost * upgrade) <= cash

# Machine hours constraint
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= availableHours + (upgradeHours * upgrade)

# Solve the problem
problem.solve()

# Preparing output
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade)

# Output result
output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(output)
print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')