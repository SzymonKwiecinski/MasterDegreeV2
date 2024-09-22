import pulp

# Parse the data
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

P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentages = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function
net_income = pulp.lpSum([(prices[i] - costs[i] - (invest_percentages[i] * prices[i])) * production[i] for i in range(P)])
problem += net_income

# Constraints
# Cash availability
problem += pulp.lpSum([(costs[i] + (invest_percentages[i] * prices[i])) * production[i] for i in range(P)]) + upgrade_cost * upgrade <= cash

# Machine capacity with upgrade possibility
problem += pulp.lpSum([hours[i] * production[i] for i in range(P)]) <= available_hours + upgrade_hours * upgrade

# Solve the problem
problem.solve()

# Extract results
net_income_val = pulp.value(net_income)
production_val = [pulp.value(production[i]) for i in range(P)]
upgrade_val = bool(pulp.value(upgrade))

# Output results
output = {
    "net_income": net_income_val,
    "production": production_val,
    "upgrade": upgrade_val
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')