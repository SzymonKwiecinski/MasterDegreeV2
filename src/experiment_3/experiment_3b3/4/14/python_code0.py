import pulp

# Data provided in JSON format
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

# Create the problem variable to contain the problem data
problem = pulp.LpProblem("Production_and_Investment_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable('y', cat='Binary')

# Objective function
profit_terms = [
    (data['Price'][i] - data['Cost'][i]) * x[i] - data['InvestPercentage'][i] * data['Price'][i] * x[i]
    for i in range(data['P'])
]
problem += pulp.lpSum(profit_terms) - data['UpgradeCost'] * y

# Constraints

# Machine Hours Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * y

# Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')