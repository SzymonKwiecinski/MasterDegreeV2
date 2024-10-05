import pulp

# Extracting data from JSON
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

P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentages = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create a Linear Programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'Production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('Upgrade', cat='Binary')

# Objective function
net_income = pulp.lpSum(
    [(prices[i] - costs[i] - prices[i] * invest_percentages[i]) * production[i] for i in range(P)]
)
problem += net_income

# Constraints
# Cash constraint
problem += pulp.lpSum([(costs[i] + prices[i] * invest_percentages[i]) * production[i] for i in range(P)]) + upgrade_cost * upgrade <= cash

# Machine hours constraint
problem += pulp.lpSum([hours[i] * production[i] for i in range(P)]) <= available_hours + upgrade_hours * upgrade

# Solve the problem
problem.solve()

# Results
output = {
    "net_income": pulp.value(net_income),
    "production": [pulp.value(production[i]) for i in range(P)],
    "upgrade": bool(pulp.value(upgrade))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')