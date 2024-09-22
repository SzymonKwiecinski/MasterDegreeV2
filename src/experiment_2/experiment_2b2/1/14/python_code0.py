import pulp

# Problem data from JSON format
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

# Initialize LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = pulp.lpSum([(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * production[i] for i in range(data['P'])])
problem += net_income

# Constraints
# Cash constraint
problem += (pulp.lpSum([data['Cost'][i] * production[i] for i in range(data['P'])]) + upgrade * data['UpgradeCost'] <= data['Cash'])

# Machine hours constraint
problem += (pulp.lpSum([data['Hour'][i] * production[i] for i in range(data['P'])]) <= data['AvailableHours'] + upgrade * data['UpgradeHours'])

# Solve the problem
problem.solve()

# Results
net_income_result = pulp.value(net_income)
production_result = [pulp.value(production[i]) for i in range(data['P'])]
upgrade_result = bool(pulp.value(upgrade))

# Output in the specified format
output = {
    "net_income": net_income_result,
    "production": production_result,
    "upgrade": upgrade_result,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')