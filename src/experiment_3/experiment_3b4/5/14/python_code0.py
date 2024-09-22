import pulp

# Data
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

# Objective function
problem += pulp.lpSum([(1 - data['InvestPercentage'][i]) * data['Price'][i] - data['Cost'][i] for i in range(data['P'])] * x) - data['UpgradeCost'] * u

# Constraints
# Machine Capacity Constraint
problem += pulp.lpSum([data['Hour'][i] * x[i] for i in range(data['P'])]) <= data['AvailableHours'] + data['UpgradeHours'] * u

# Cash Availability Constraint
problem += pulp.lpSum([(data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]) + data['UpgradeCost'] * u <= data['Cash']

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')