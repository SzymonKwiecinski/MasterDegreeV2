import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function: Maximize total net income
net_income = pulp.lpSum(
    (price[i] - cost[i] - (price[i] * investPercentage[i]) ) * production[i] for i in range(P)
)
problem += net_income

# Constraints
# Machine hours constraint
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= (availableHours + upgrade * upgradeHours)

# Cash availability constraint
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) <= cash + upgrade * (upgradeCost - cash)

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(prod) for prod in production]
upgrade_value = pulp.value(upgrade) == 1

# Structure the output
output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": upgrade_value,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')