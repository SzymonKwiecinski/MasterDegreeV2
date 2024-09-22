import pulp

# Input data
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

# Unpack data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# LP Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function: Maximize net income
net_income = pulp.lpSum([(price[i] - cost[i]) * production[i] - investPercentage[i] * price[i] * production[i] for i in range(P)])
problem += net_income

# Constraints
# Cash constraint
problem += pulp.lpSum([cost[i] * production[i] for i in range(P)]) + upgrade * upgradeCost <= cash

# Machine hours constraint
problem += pulp.lpSum([hour[i] * production[i] for i in range(P)]) <= availableHours + upgrade * upgradeHours

# Solve the problem
problem.solve()

# Results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_decision = bool(pulp.value(upgrade))

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": upgrade_decision,
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')