import pulp

# Parse the input data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
P = data['P']
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function: Maximize total net income
net_income_expressions = [
    (data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * production[i]
    for i in range(P)
]
problem += pulp.lpSum(net_income_expressions) - upgrade * data['UpgradeCost']

# Constraint: Cash availability
cash_constraints = [
    data['Cost'][i] * production[i] <= data['Cash'] + pulp.lpSum(
        data['InvestPercentage'][j] * data['Price'][j] * production[j] for j in range(P)
    )
    for i in range(P)
]
for constraint in cash_constraints:
    problem += constraint

# Constraint: Machine capacity (with possible upgrade)
problem += pulp.lpSum(data['Hour'][i] * production[i] for i in range(P)) <= data['AvailableHours'] + upgrade * data['UpgradeHours']

# Solve the problem
problem.solve()

# Output the results
output = {
    "net_income": pulp.value(problem.objective),
    "production": [pulp.value(production[i]) for i in range(P)],
    "upgrade": bool(pulp.value(upgrade))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')