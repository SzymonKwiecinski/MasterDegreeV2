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

# Unpacking data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(P)]
u = pulp.LpVariable(f'u', cat='Binary')

# Objective Function
objective = pulp.lpSum([(price[i] - cost[i] - investPercentage[i] * price[i]) * x[i] for i in range(P)]) - u * upgradeCost
problem += objective

# Constraints
# Cash Availability Constraint
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash - pulp.lpSum([investPercentage[i] * price[i] * x[i] for i in range(P)])

# Machine Capacity Constraint
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= availableHours + u * upgradeHours

# Solve the problem
problem.solve()

# Print results
print("Optimal Production Quantities:")
for i in range(P):
    print(f'Product {i+1}: {pulp.value(x[i])}')

print(f'Upgrade Decision (1=Yes, 0=No): {pulp.value(u)}')

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')