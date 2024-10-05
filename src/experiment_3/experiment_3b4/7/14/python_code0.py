import pulp

# Data from the provided JSON
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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable('y', cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(
        (data['Price'][i] * x[i] - data['Cost'][i] * x[i] - data['InvestPercentage'][i] * data['Price'][i] * x[i])
        for i in range(data['P'])
    ) - data['UpgradeCost'] * y
)

# Constraints
problem += (
    pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <=
    data['AvailableHours'] + data['UpgradeHours'] * y
)

problem += (
    pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) +
    data['UpgradeCost'] * y <=
    data['Cash'] + pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P']))
)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')