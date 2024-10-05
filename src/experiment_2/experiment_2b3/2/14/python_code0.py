import pulp

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f"production_{i}", lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable("upgrade", cat='Binary')

# Objective Function: Maximize Net Income
net_income = pulp.lpSum([(prices[i] - costs[i] - invest_percentage[i] * prices[i]) * production[i] for i in range(P)])
problem += net_income

# Constraints
# Cash constraint
problem += pulp.lpSum([costs[i] * production[i] for i in range(P)]) \
           + upgrade_cost * upgrade <= cash, "Cash"

# Machine hours constraint
problem += pulp.lpSum([hours[i] * production[i] for i in range(P)]) \
           <= available_hours + upgrade_hours * upgrade, "MachineHours"

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(net_income)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade)

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value),
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')