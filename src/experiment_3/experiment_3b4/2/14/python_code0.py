import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(1, data['P'] + 1)]
u = pulp.LpVariable('u', cat='Binary')

# Objective Function
problem += pulp.lpSum([
    (data['Price'][i] * x[i] - data['Cost'][i] * x[i] - data['Price'][i] * data['InvestPercentage'][i] * x[i])
    for i in range(data['P'])
]) - data['UpgradeCost'] * u

# Constraints
# Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash'], "Cash_Constraint"

# Machine Capacity Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * u, "Machine_Capacity_Constraint"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')