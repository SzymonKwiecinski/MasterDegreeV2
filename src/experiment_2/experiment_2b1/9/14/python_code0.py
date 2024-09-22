import pulp
import json

# Input data
data_json = '{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}'
data = json.loads(data_json)

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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = pulp.LpVariable.dicts("Production", range(P), lowBound=0, cat='Continuous')
upgrade = pulp.LpVariable("Upgrade", cat='Binary')

# Objective function
net_income = pulp.lpSum((price[i] - cost[i]) * production[i] for i in range(P))
investment_cost = pulp.lpSum(investPercentage[i] * price[i] * production[i] for i in range(P))
problem += net_income - investment_cost - (upgrade * upgradeCost), "Total_Net_Income"

# Constraints
# Cash constraint
problem += pulp.lpSum(price[i] * production[i] for i in range(P)) <= cash, "Cash_Constraint"

# Machine hour constraints
problem += pulp.lpSum(hour[i] * production[i] for i in range(P)) <= availableHours + (upgrade * upgradeHours), "Machine_Hour_Constraint"

# Solve the problem
problem.solve()

# Collect results
net_income_value = pulp.value(problem.objective)
production_values = [production[i].varValue for i in range(P)]
upgrade_value = upgrade.varValue

# Output results
output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')