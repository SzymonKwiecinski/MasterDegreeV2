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

# Define the Linear Program
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Constraints
# Machine hour constraint
problem += (pulp.lpSum(hours[i] * production[i] for i in range(P)) <= available_hours + upgrade * upgrade_hours)

# Cash constraint
problem += (pulp.lpSum((costs[i] + (prices[i] - costs[i]) * invest_percentages[i]) * production[i] for i in range(P)) 
             + upgrade * upgrade_cost <= cash)

# Objective Function
# Net income is the sum of (selling price - cost - investment) * production for each product minus the upgrade cost
net_income = pulp.lpSum((prices[i] - costs[i] - (prices[i] - costs[i]) * invest_percentages[i]) * production[i] for i in range(P)) - upgrade * upgrade_cost
problem += net_income

# Solve the problem
problem.solve()

# Prepare the output
net_income_value = pulp.value(net_income)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_decision = pulp.value(upgrade) > 0.5

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": upgrade_decision
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')