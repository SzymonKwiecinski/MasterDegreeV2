import pulp

# Data from the JSON
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Problem parameters
P = data['P']
cash = data['Cash']
hours = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function: Maximize Net Income
problem += pulp.lpSum([(price[i] - cost[i]) * production[i] - invest_percentage[i] * price[i] * production[i] for i in range(P)])

# Constraints
# Cash constraint
problem += pulp.lpSum([cost[i] * production[i] for i in range(P)]) + upgrade_cost * upgrade <= cash

# Machine capacity constraint
problem += pulp.lpSum([hours[i] * production[i] for i in range(P)]) <= available_hours + upgrade_hours * upgrade

# Solve the problem
problem.solve()

# Collect results
net_income = pulp.value(problem.objective)
production_results = [pulp.value(production[i]) for i in range(P)]
upgrade_decision = bool(pulp.value(upgrade))

# Output format
output = {
    "net_income": net_income,
    "production": production_results,
    "upgrade": upgrade_decision,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')