import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 
        'AvailableHours': 2000}

# Extract parameters from the data
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

# Define decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function: maximize net income
net_income = pulp.lpSum((price[i] * production[i] - cost[i] * production[i] - 
                          investPercentage[i] * price[i] * production[i]) for i in range(P))
problem += net_income

# Constraints
# Cash constraint
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) <= cash - upgrade * upgradeCost

# Machine hours constraint
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= availableHours + upgrade * upgradeHours

# Solve the problem
problem.solve()

# Prepare output
net_income_value = pulp.value(problem.objective)
productions = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade)

output = {
    "net_income": net_income_value,
    "production": productions,
    "upgrade": bool(upgrade_value)
}

# Print output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')