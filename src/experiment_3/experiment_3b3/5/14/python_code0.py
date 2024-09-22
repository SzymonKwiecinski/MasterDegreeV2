import pulp

# Define the data
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Define decision variables
production_quantities = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
upgrade_decision = pulp.LpVariable('u', cat='Binary')

# Define the objective function
net_income = sum(
    (data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * production_quantities[i]
    for i in range(data['P'])
) - upgrade_decision * data['UpgradeCost']

problem += net_income

# Add constraints
# Cash constraint
problem += (
    sum(data['Cost'][i] * production_quantities[i] for i in range(data['P'])) + upgrade_decision * data['UpgradeCost']
    <= data['Cash']
)

# Machine hours constraint
problem += (
    sum(data['Hour'][i] * production_quantities[i] for i in range(data['P'])) 
    <= data['AvailableHours'] + upgrade_decision * data['UpgradeHours']
)

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')