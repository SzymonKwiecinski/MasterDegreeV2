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

# Extract data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_rate = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = sum((price[i] - cost[i]) * production[i] for i in range(P)) - upgrade_cost * upgrade
problem += net_income

# Constraints
# Cash constraint
problem += sum(cost[i] * production[i] for i in range(P)) + upgrade_cost * upgrade <= cash

# Machine hours constraint
problem += sum(hour[i] * production[i] for i in range(P)) <= available_hours + upgrade_hours * upgrade

# Solve
problem.solve()

# Results
output = {
    "net_income": pulp.value(net_income),
    "production": [pulp.value(production[i]) for i in range(P)],
    "upgrade": bool(pulp.value(upgrade))
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')