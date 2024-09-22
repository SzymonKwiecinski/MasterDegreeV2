import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Problem definition
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Parameters
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
available_hours = data['AvailableHours']
upgrade_cost = data['UpgradeCost']
upgrade_hours = data['UpgradeHours']

# Objective function
net_income = pulp.lpSum([(price[i] * production[i] - cost[i] * production[i] - invest_percentage[i] * price[i] * production[i]) for i in range(data['P'])])
problem += net_income

# Constraints
# Cash availability constraint
problem += pulp.lpSum([cost[i] * production[i] for i in range(data['P'])]) <= cash - upgrade * upgrade_cost, "CashAvailability"
# Machine hour constraint
problem += pulp.lpSum([hour[i] * production[i] for i in range(data['P'])]) <= available_hours + upgrade * upgrade_hours, "MachineCapacity"

# Solve problem
problem.solve()

# Output results
production_quantities = [pulp.value(production[i]) for i in range(data['P'])]
net_income_value = pulp.value(problem.objective)
upgrade_value = bool(pulp.value(upgrade))

# Prepare output
output = {
    "net_income": net_income_value,
    "production": production_quantities,
    "upgrade": upgrade_value,
}

# Print objective value
print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')