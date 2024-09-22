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
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable("y", cat='Binary')

# Objective Function
net_income = pulp.lpSum(
    [(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]
) - data['UpgradeCost'] * y
problem += net_income

# Constraints
# Machine hours constraint
machine_hours_constraint = pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * y
problem += machine_hours_constraint

# Cash constraint
cash_constraint = pulp.lpSum(
    [(data['Cost'][i] + data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]
) + data['UpgradeCost'] * y <= data['Cash']
problem += cash_constraint

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')