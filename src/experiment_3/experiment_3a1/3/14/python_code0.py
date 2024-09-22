import pulp

# Data from provided JSON format
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

# Define the linear programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Define decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0) for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Define the objective function
net_income = pulp.lpSum((data['Price'][i] * production[i] - data['Cost'][i] * production[i] - 
                          data['InvestPercentage'][i] * data['Price'][i] * production[i]) 
                        for i in range(data['P']))
problem += net_income

# Define constraints
# Machine Capacity Constraint
problem += (pulp.lpSum(data['Hour'][i] * production[i] for i in range(data['P'])) 
             <= data['AvailableHours'] + (upgrade * data['UpgradeHours']))

# Cash Availability Constraint
problem += (pulp.lpSum(data['Cost'][i] * production[i] for i in range(data['P'])) 
             + upgrade * data['UpgradeCost'] <= data['Cash'])

# Solve the problem
problem.solve()

# Outputs
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(data['P'])]
upgrade_value = pulp.value(upgrade)

print(f'(Net Income): {net_income_value}')
print(f'(Production Quantities): {production_values}')
print(f'(Upgrade): {upgrade_value}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')