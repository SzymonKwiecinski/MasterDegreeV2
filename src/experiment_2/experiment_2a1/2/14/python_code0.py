import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}
cash = data['Cash']
available_hours = data['AvailableHours']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentage = data['InvestPercentage']
P = data['P']

# Problem Definition
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = pulp.lpSum((prices[i] - costs[i]) * production[i] - (prices[i] * invest_percentage[i] * production[i]) for i in range(P))
problem += net_income - upgrade_cost * upgrade, "Total_Net_Income"

# Constraints
# Machine hours constraint
problem += pulp.lpSum(hours[i] * production[i] for i in range(P)) <= available_hours + upgrade_hours * upgrade, "Machine_Hours_Constraint"

# Cash availability constraint
problem += pulp.lpSum(costs[i] * production[i] for i in range(P)) <= cash, "Cash_Availability_Constraint"

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

print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')