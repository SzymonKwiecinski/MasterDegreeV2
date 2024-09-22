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
problem = pulp.LpProblem("Product_Production", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

# Objective Function
profit_terms = [(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]
problem += pulp.lpSum(profit_terms) - u * data['UpgradeCost'], "Net Income"

# Constraints
# Cash Availability Constraint
problem += pulp.lpSum([data['Cost'][i] * x[i] for i in range(data['P'])]) <= data['Cash'], "Cash Constraint"

# Machine Capacity Constraint
problem += pulp.lpSum([data['Hour'][i] * x[i] for i in range(data['P'])]) <= data['AvailableHours'] + u * data['UpgradeHours'], "Machine Capacity"

# Solve
problem.solve()

# Output
production = [pulp.value(x[i]) for i in range(data['P'])]
upgrade = bool(pulp.value(u))
net_income = pulp.value(problem.objective)

for i, qty in enumerate(production):
    print(f'Production quantity for product {i+1}: {qty}')
print(f'Upgrade status of the machine: {upgrade}')
print(f'Net Income: {net_income}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')