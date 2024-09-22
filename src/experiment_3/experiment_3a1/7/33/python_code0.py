import pulp

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create a linear programming problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision Variables
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum([values[k] * isincluded[k] for k in range(K)])

# Capacity constraint
problem += pulp.lpSum([sizes[k] * isincluded[k] for k in range(K)]) <= C

# Solve the problem
problem.solve()

# Retrieve the values of the decision variables
result = [isincluded[k].varValue for k in range(K)]

# Output the results
print(f'Included items: {result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')