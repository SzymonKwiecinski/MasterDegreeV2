import pulp

# Data from JSON
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

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Continuous') for i in range(1, data['P'] + 1)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function
profit_terms = [
    (data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i]
    for i in range(data['P'])
]
objective = pulp.lpSum(profit_terms) - data['UpgradeCost'] * upgrade
problem += objective

# Constraints
# Cash Availability Constraint
cash_constraint = pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= \
                  data['Cash'] - pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P']))
problem += cash_constraint

# Machine Capacity Constraint
machine_hours_constraint = pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= \
                           data['AvailableHours'] + data['UpgradeHours'] * upgrade
problem += machine_hours_constraint

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')