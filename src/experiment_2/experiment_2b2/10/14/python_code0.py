import pulp

# Define the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Extract the data from the JSON
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Decision variables
production = [pulp.LpVariable(f'Production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('Upgrade', cat='Binary')

# Objective function
net_income = pulp.lpSum([(prices[i] - costs[i] - prices[i] * invest_percentage[i]) * production[i] for i in range(P)])
problem += net_income

# Constraints
problem += pulp.lpSum([hours[i] * production[i] for i in range(P)]) <= available_hours + upgrade * upgrade_hours, "Machine Hours"
problem += pulp.lpSum([costs[i] * production[i] for i in range(P)]) <= cash + pulp.lpSum([prices[i] * invest_percentage[i] * production[i] for i in range(P)]) - upgrade * upgrade_cost, "Cash Flow"

# Solve the problem
problem.solve()

# Prepare the output
solution = {
    "net_income": pulp.value(problem.objective),
    "production": [pulp.value(prod) for prod in production],
    "upgrade": bool(pulp.value(upgrade))
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')