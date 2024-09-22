import pulp

# Data input
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Extract data
P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentages = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Define problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Constraints
# 1. Machine hours constraint
problem += pulp.lpSum([production[i] * hours[i] for i in range(P)]) <= available_hours + upgrade * upgrade_hours, "Machine_Hours_Constraint"

# 2. Cash constraint
problem += pulp.lpSum([(prices[i] - invest_percentages[i] * prices[i]) * production[i] - costs[i] * production[i] for i in range(P)]) - upgrade_cost * upgrade <= cash, "Cash_Constraint"

# Objective function (maximize net income)
net_income_expr = pulp.lpSum([(prices[i] - costs[i] - invest_percentages[i] * prices[i]) * production[i] for i in range(P)])
problem += net_income_expr, "Net_Income_Objective"

# Solve problem
problem.solve()

# Extract results
net_income = pulp.value(net_income_expr)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = bool(pulp.value(upgrade))

# Output result
result = {
    "net_income": net_income,
    "production": production_values,
    "upgrade": upgrade_value,
}

print(result)  # Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')  # Print the objective value