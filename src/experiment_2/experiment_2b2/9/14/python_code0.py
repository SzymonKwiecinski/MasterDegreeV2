import pulp

# Read data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Objective function
net_income = sum((price[i] - cost[i] - investPercentage[i] * price[i]) * production[i] for i in range(P))
problem += net_income

# Constraints
# Cash constraint
cash_constraint = sum(cost[i] * production[i] for i in range(P)) + upgradeCost * upgrade <= cash
problem += cash_constraint

# Machine hours constraint
machine_hours_constraint = sum(hour[i] * production[i] for i in range(P)) <= availableHours + upgradeHours * upgrade
problem += machine_hours_constraint

# Solve
problem.solve()

# Results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade)

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value),
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')