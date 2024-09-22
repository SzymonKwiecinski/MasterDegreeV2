import pulp
import json

# Input data in JSON format
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 
        'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 
        'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Extract data
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

# Decision variables
production = pulp.LpVariable.dicts("Production", range(P), lowBound=0, cat='Continuous')
upgrade = pulp.LpVariable("Upgrade", cat='Binary')

# Objective function: Maximize total net income
net_income = pulp.lpSum((price[i] * production[i] * (1 - investPercentage[i])) - (cost[i] * production[i]) 
                         for i in range(P))

# Add the cost of upgrading machine capacity
if upgrade:
    available_hours = availableHours + upgradeHours
else:
    available_hours = availableHours

# Constraints
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= available_hours, "Machine_Hour_Capacity"
problem += pulp.lpSum((price[i] * production[i]) * investPercentage[i] for i in range(P)) <= cash - upgradeCost * upgrade, "Cash_Availability"

# Define the objective
problem += net_income

# Solve the problem
problem.solve()

# Extract results
net_income_value = pulp.value(problem.objective)
production_values = [production[i].varValue for i in range(P)]
upgrade_value = upgrade.varValue

# Print results
output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')