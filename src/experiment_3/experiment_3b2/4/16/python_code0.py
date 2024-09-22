import pulp

# Data
data = {
    'O': 2,
    'P': 2,
    'L': 3,
    'Allocated': [8000, 5000],
    'Price': [38, 33],
    'Input': [[3, 5], [1, 1], [5, 3]],
    'Output': [[4, 3], [1, 1], [3, 4]],
    'Cost': [51, 11, 40]
}

# Problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['L']), lowBound=0, cat='Continuous')

# Objective Function
total_revenue = pulp.lpSum(data['Output'][l][p] * x[l] * data['Price'][p] for l in range(data['L']) for p in range(data['P']))
total_cost = pulp.lpSum(data['Output'][l][p] * x[l] * data['Cost'][l] for l in range(data['L']) for p in range(data['P']))
problem += total_revenue - total_cost

# Constraints
for i in range(data['O']):
    problem += pulp.lpSum(data['Input'][l][i] * x[l] for l in range(data['L'])) <= data['Allocated'][i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')