import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 
        'AvailableHours': 2000}

# Extracting data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Define the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Define decision variables
production = pulp.LpVariable.dicts("Production", range(P), lowBound=0, cat='Continuous')
upgrade = pulp.LpVariable("Upgrade", cat='Binary')

# Objective function: maximize net income
net_income = pulp.lpSum((price[i] - cost[i]) * production[i] * (1 - invest_percentage[i]) for i in range(P))
problem += net_income

# Constraints
# Cash constraint
cash_constraint = pulp.lpSum(cost[i] * production[i] for i in range(P)) <= cash
problem += cash_constraint

# Machine hours constraint
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= (available_hours + upgrade * upgrade_hours)

# Upgrade cost constraint
problem += upgrade * upgrade_cost <= cash

# Solve the problem
problem.solve()

# Prepare output
output = {
    "net_income": pulp.value(net_income),
    "production": [pulp.value(production[i]) for i in range(P)],
    "upgrade": pulp.value(upgrade) == 1
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')