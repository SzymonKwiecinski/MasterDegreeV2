import pulp

# Given data
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

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

# Objective Function
profit_terms = [data['Price'][i] * x[i] - data['Cost'][i] * x[i] - data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P'])]
objective = pulp.lpSum(profit_terms) - data['UpgradeCost'] * u
problem += objective

# Constraints
# Machine Capacity Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + u * data['UpgradeHours']

# Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash'] + pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P']))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')