import pulp

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

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

# Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function: Maximize net income
net_income = pulp.lpSum((price[i] * production[i] - cost[i] * production[i] - (price[i] * production[i] * invest_percentage[i])) for i in range(P))
                        - upgrade_cost * upgrade
problem += net_income

# Constraints
# Cash constraint
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) <= cash - upgrade_cost * upgrade

# Machine hours constraint
total_hours = pulp.lpSum(hour[i] * production[i] for i in range(P))
problem += total_hours <= available_hours + upgrade_hours * upgrade

# Solve the problem
problem.solve()

# Prepare output
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(var) for var in production]
upgrade_value = pulp.value(upgrade)

# Output format
output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": upgrade_value == 1
}

print(output)
print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')