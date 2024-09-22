import pulp

# Data extracted from the JSON format
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

# Create the problem variable
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function
net_income = pulp.lpSum(
    (data['Price'][i] * production[i] - 
     data['Cost'][i] * production[i] - 
     data['InvestPercentage'][i] * data['Price'][i] * production[i]) 
    for i in range(data['P'])
)
problem += net_income

# Constraints
# Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * production[i] for i in range(data['P'])) + data['UpgradeCost'] * upgrade <= data['Cash']

# Machine Hours Constraint
problem += pulp.lpSum(data['Hour'][i] * production[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * upgrade

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')