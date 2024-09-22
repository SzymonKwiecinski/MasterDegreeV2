import pulp

# Data from the provided JSON format
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
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

# Objective function
net_income = pulp.lpSum(data['Price'][i] * x[i] - data['Cost'][i] * x[i] for i in range(data['P'])) \
             - pulp.lpSum(data['Price'][i] * x[i] * data['InvestPercentage'][i] for i in range(data['P'])) \
             - u * data['UpgradeCost']

problem += net_income, "Total_Net_Income"

# Constraints
# Cash constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) + u * data['UpgradeCost'] <= data['Cash'], "Cash_Constraint"

# Machine hours constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + u * data['UpgradeHours'], "Machine_Hour_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')