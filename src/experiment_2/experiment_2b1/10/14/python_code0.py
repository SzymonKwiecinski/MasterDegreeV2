import pulp
import json

data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 
        'AvailableHours': 2000}

# Unpacking the data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function: Maximize total net income
net_income = pulp.lpSum((price[i] - cost[i] - investPercentage[i] * price[i]) * production[i] for i in range(P))
problem += net_income

# Constraints
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= availableHours + upgrade * upgradeHours, "Machine_Capacity_Constraint"
problem += pulp.lpSum(cost[i] * production[i] for i in range(P)) <= cash - upgrade * upgradeCost, "Cash_Availability_Constraint"

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(problem.objective)
production_values = [production[i].varValue for i in range(P)]
upgrade_value = upgrade.varValue > 0.5

print(f'{{"net_income": {net_income_value}, "production": {production_values}, "upgrade": {upgrade_value}}}')
print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')