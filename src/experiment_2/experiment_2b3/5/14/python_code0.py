import pulp

# Defining the problem data
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

# Extracting data for easier use
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Defining the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function
net_income = pulp.lpSum([(price[i] - cost[i]) * production[i] - (1 - investPercentage[i]) * price[i] * production[i] 
                         for i in range(P)])
problem += net_income

# Constraints
# Machine hours constraint
problem += pulp.lpSum([hour[i] * production[i] for i in range(P)]) <= availableHours + upgrade * upgradeHours

# Cash constraint
problem += pulp.lpSum([
    cost[i] * production[i] + (1 - investPercentage[i]) * price[i] * production[i] for i in range(P)
]) + upgrade * upgradeCost <= cash

# Solving the problem
problem.solve()

# Extracting results
production_values = [pulp.value(production[i]) for i in range(P)]
is_upgrade = bool(pulp.value(upgrade))

output = {
    "net_income": pulp.value(problem.objective),
    "production": production_values,
    "upgrade": is_upgrade
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')