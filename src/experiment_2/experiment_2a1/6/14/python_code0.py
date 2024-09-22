import json
import pulp

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 
        'AvailableHours': 2000}

# Problem Variables
P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function: Maximize Net Income
net_income = pulp.lpSum((prices[i] - costs[i]) * production[i] for i in range(P)) \
                       - upgrade_cost * upgrade

problem += net_income, "Total_Net_Income"

# Constraints
# Total machine hours used must not exceed available hours (and may include upgrade)
total_hours = pulp.lpSum(hours[i] * production[i] for i in range(P)) \
              <= (available_hours + upgrade_hours * upgrade)
problem += total_hours

# Budget constraint: cash available for production
total_costs = pulp.lpSum(costs[i] * production[i] for i in range(P)) \
              <= cash - pulp.lpSum((prices[i] * invest_percentage[i]) * production[i] for i in range(P))
problem += total_costs

# Solve the problem
problem.solve()

# Output the results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(prod) for prod in production]
upgrade_value = pulp.value(upgrade)

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value),
}

print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')