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

# Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
profit = [
    (data['Price'][i] - data['Cost'][i]) * x[i] - 
    data['InvestPercentage'][i] * data['Price'][i] * x[i]
    for i in range(data['P'])
]
problem += pulp.lpSum(profit) - data['UpgradeCost'] * upgrade

# Constraints
# Machine Hour Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= \
           data['AvailableHours'] + data['UpgradeHours'] * upgrade

# Cash Availability Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash']

# Solve
problem.solve()

# Results
net_income = pulp.value(problem.objective)
production = [pulp.value(x[i]) for i in range(data['P'])]
should_upgrade = bool(pulp.value(upgrade))

# Output
print(f'(Objective Value): <OBJ>{net_income}</OBJ>')
print(f'Production: {production}')
print(f'Upgrade: {should_upgrade}')