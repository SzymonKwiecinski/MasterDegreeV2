import pulp

# Define the LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Parse input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function: Maximize total net income
net_income = pulp.lpSum([(price[i] - cost[i] - investPercentage[i]*price[i]) * production[i] for i in range(P)])
problem += net_income, "Net Income"

# Constraints
# Cash constraint
problem += pulp.lpSum([(cost[i] + investPercentage[i]*price[i]) * production[i] for i in range(P)]) + upgradeCost * upgrade <= cash, "Cash Availability"

# Machine hours constraint
problem += pulp.lpSum([hour[i] * production[i] for i in range(P)]) <= availableHours + upgradeHours * upgrade, "Machine Capacity"

# Solve the problem
problem.solve()

# Gather results
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade) == 1

# Create the output dictionary
output = {
    "net_income": pulp.value(problem.objective),
    "production": production_values,
    "upgrade": upgrade_value,
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')