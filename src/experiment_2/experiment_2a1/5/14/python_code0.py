import pulp
import json

# Input data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 
        'AvailableHours': 2000}

P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Create the problem variable
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective function: Maximize total net income
net_income = pulp.lpSum((prices[i] - costs[i]) * production[i] - 
                         (prices[i] * investPercentage[i]) * production[i] for i in range(P))
problem += net_income, "Total_Net_Income"

# Constraints
# Cash constraint
problem += pulp.lpSum(costs[i] * production[i] for i in range(P)) + \
           upgradeCost * upgrade <= cash, "Cash_Constraint"

# Machine hours constraint
problem += pulp.lpSum(hours[i] * production[i] for i in range(P)) <= \
           availableHours + upgradeHours * upgrade, "Machine_Hours_Constraint"

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade)

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": bool(upgrade_value)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{net_income_value}</OBJ>')