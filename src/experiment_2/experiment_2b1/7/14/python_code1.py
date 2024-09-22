import pulp
import json

data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Extract data from JSON
P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentages = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Variables
production = pulp.LpVariable.dicts("production", range(P), lowBound=0, cat='Continuous')
upgrade = pulp.LpVariable("upgrade", cat='Binary')

# Objective Function: Maximize net income
net_income = pulp.lpSum((prices[i] - costs[i]) * production[i] for i in range(P)) - upgrade_cost * upgrade
problem += net_income

# Constraints
# Cash availability constraint
problem += pulp.lpSum(invest_percentages[i] * (prices[i] * production[i]) for i in range(P)) <= cash + upgrade * upgrade_hours , "CashConstraint")

# Machine capacity constraint
problem += pulp.lpSum(hours[i] * production[i] for i in range(P)) <= available_hours + (upgrade * upgrade_hours), "MachineCapacityConstraint"

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(problem.objective)
production_values = [production[i].varValue for i in range(P)]
upgrade_value = upgrade.varValue

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')