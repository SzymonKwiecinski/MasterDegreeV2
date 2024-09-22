import pulp

# Data from the JSON format
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

# Create the LP problem
problem = pulp.LpProblem("Product_Production", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0) for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = pulp.lpSum((data['Price'][i] - data['Cost'][i]) * production[i] - 
                         data['InvestPercentage'][i] * (data['Price'][i] * production[i]) 
                         for i in range(data['P']))
objective = net_income - data['UpgradeCost'] * upgrade
problem += objective, "Total_Net_Income"

# Constraints
# Machine Capacity Constraint
problem += (pulp.lpSum(data['Hour'][i] * production[i] for i in range(data['P'])) <= 
             data['AvailableHours'] + data['UpgradeHours'] * upgrade), "Machine_Capacity"

# Cash Availability Constraint
problem += (pulp.lpSum(data['Cost'][i] * production[i] for i in range(data['P'])) <= 
             data['Cash']), "Cash_Availability"

# Solve the problem
problem.solve()

# Output the results
production_values = [production[i].varValue for i in range(data['P'])]
upgrade_value = upgrade.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Production quantities: {production_values}')
print(f'Upgrade performed: {bool(upgrade_value)}')