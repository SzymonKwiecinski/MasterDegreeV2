import pulp

# Data from JSON
data = {
    'P': 2,
    'Cash': 3000,
    'Hour': [2, 6],
    'Cost': [3, 2],
    'Price': [6, 5],
    'InvestPercentage': [0.4, 0.3],
    'UpgradeHours': 2000,
    'UpgradeCost': 400,
    'AvailableHours': 2000
}

# Extract data
P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentages = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Define the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f"production_{i}", lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable("upgrade", cat='Binary')

# Define the net income
net_income = pulp.lpSum([(prices[i] - costs[i] - invest_percentages[i] * prices[i]) * production[i] for i in range(P)])

# Add objective function
problem += net_income, "Total_Net_Income"

# Add constraints
problem += pulp.lpSum([hours[i] * production[i] for i in range(P)]) <= available_hours + upgrade * upgrade_hours, "Machine_Hours"
problem += pulp.lpSum([(costs[i] * production[i]) + (upgrade * upgrade_cost) for i in range(P)]) <= cash, "Cash_Constraint"

# Solve the problem
problem.solve()

# Extract data for output
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade)

# Create output
output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": True if upgrade_value == 1.0 else False
}

# Print result
print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')