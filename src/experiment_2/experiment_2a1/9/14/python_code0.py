import pulp
import json

# Input data
data_json = '''{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}'''
data = json.loads(data_json.replace("'", "\""))

# Problem parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function
net_income = pulp.lpSum((price[i] - cost[i]) * production[i] for i in range(P)) - upgrade_cost * upgrade
problem += net_income

# Constraints for cash availability
cash_investment = pulp.lpSum(invest_percentage[i] * price[i] * production[i] for i in range(P))
problem += cash_investment <= cash - upgrade_cost * upgrade

# Constraints for machine hours
used_hours = pulp.lpSum(hour[i] * production[i] for i in range(P))
if available_hours > 0:
    problem += used_hours <= available_hours + upgrade_hours * upgrade

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(prod) for prod in production]
upgrade_value = pulp.value(upgrade)

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')