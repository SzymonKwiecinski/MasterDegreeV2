import pulp

# Data from JSON
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

# Number of products
P = data['P']

# Initialize the problem
problem = pulp.LpProblem("Product_Production", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Continuous') for i in range(P)]
u = pulp.LpVariable('u', cat='Binary')

# Objective function
problem += pulp.lpSum((data['Price'][i] * x[i] - data['Cost'][i] * x[i] - data['InvestPercentage'][i] * data['Price'][i] * x[i]) for i in range(P))

# Constraints
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(P)) + u * data['UpgradeCost'] <= data['Cash'], "Cash_Constraint"
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(P)) <= data['AvailableHours'] + u * data['UpgradeHours'], "Hours_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')