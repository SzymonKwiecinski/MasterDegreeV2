import pulp

# Parse the input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentages = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function: Maximize total net income
net_income_vars = [
    (prices[i] - costs[i]) * production[i] - invest_percentages[i] * prices[i] * production[i]
    for i in range(P)
]
problem += pulp.lpSum(net_income_vars)

# Constraint 1: Cash availability
cash_constraint = pulp.lpSum([costs[i] * production[i] for i in range(P)]) <= cash + upgrade * upgrade_cost
problem += cash_constraint

# Constraint 2: Machine capacity
hours_constraint = pulp.lpSum([hours[i] * production[i] for i in range(P)]) <= available_hours + upgrade * upgrade_hours
problem += hours_constraint

# Solve the problem
problem.solve()

# Gather results
net_income = pulp.value(problem.objective)
production_quantities = [pulp.value(production[i]) for i in range(P)]
upgrade_decision = bool(pulp.value(upgrade))

# Prepare output
output = {
    "net_income": net_income,
    "production": production_quantities,
    "upgrade": upgrade_decision,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')