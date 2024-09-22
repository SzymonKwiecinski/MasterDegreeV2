import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Extracting data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = pulp.LpVariable.dicts("Production", range(P), lowBound=0, cat='Continuous')
upgrade = pulp.LpVariable("Upgrade", cat='Binary')

# Objective function: Maximize net income
net_income = pulp.lpSum((price[i] - cost[i] - investPercentage[i] * (price[i] - cost[i])) * production[i] for i in range(P))
problem += net_income

# Constraints
# Cash constraint
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) <= cash + upgrade * upgradeCost

# Machine hours constraint
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= availableHours + upgrade * upgradeHours

# Solve the problem
problem.solve()

# Prepare the output
results = {
    "net_income": pulp.value(problem.objective),
    "production": [pulp.value(production[i]) for i in range(P)],
    "upgrade": pulp.value(upgrade) == 1
}

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')