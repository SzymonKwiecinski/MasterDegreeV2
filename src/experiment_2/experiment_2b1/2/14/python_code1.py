import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Problem setup
P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Define objective function: maximize total net income
net_income = pulp.lpSum((prices[i] - costs[i] - (prices[i] * invest_percentage[i])) * production[i] for i in range(P)) \
                        - upgrade_cost * upgrade)

problem += net_income

# Constraints
# Machine hours constraint
total_hours = pulp.lpSum(hours[i] * production[i] for i in range(P)) 
problem += total_hours <= available_hours + (upgrade_hours * upgrade)

# Cash availability constraint
total_investment = pulp.lpSum(prices[i] * production[i] * invest_percentage[i] for i in range(P)) 
problem += total_investment <= cash 

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade)

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')