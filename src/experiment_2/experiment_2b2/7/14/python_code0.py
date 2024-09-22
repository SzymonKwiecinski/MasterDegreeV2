import pulp

# Data from JSON
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Variables
P = data['P']
cash_available = data['Cash']
hours_required = data['Hour']
production_costs = data['Cost']
selling_prices = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = pulp.lpSum([(selling_prices[i] - production_costs[i] - (selling_prices[i] * invest_percentage[i])) * production[i] for i in range(P)])
problem += net_income

# Constraints
problem += pulp.lpSum([hours_required[i] * production[i] for i in range(P)]) <= available_hours + upgrade * upgrade_hours
problem += pulp.lpSum([production_costs[i] * production[i] for i in range(P)]) <= cash_available + upgrade * (-upgrade_cost)

# Solve
problem.solve()

# Extract results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = bool(pulp.value(upgrade))

# Output
result = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": upgrade_value
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')