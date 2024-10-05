import pulp

# Parse the data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Variables
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'Production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('Upgrade', cat='Binary')

# Objective function: Maximize net income
net_income = pulp.lpSum([(price[i] - cost[i]) * production[i] - invest_percentage[i] * price[i] * production[i] for i in range(P)])
problem += net_income

# Constraints

# Cash constraint
problem += pulp.lpSum([cost[i] * production[i] for i in range(P)]) + upgrade_cost * upgrade <= cash

# Machine hours constraint
problem += pulp.lpSum([hour[i] * production[i] for i in range(P)]) <= available_hours + upgrade_hours * upgrade

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade)

result = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')