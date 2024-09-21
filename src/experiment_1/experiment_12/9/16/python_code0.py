import pulp

# Load data from the JSON structure
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Create a LP problem
problem = pulp.LpProblem("Minimize_Transmission_Costs", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(P) for j in range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['transmission_costs'][i][j] * x[i, j] for i in range(P) for j in range(C))

# Constraints
# Supply constraints
for i in range(P):
    problem += pulp.lpSum(x[i, j] for j in range(C)) <= data['supply'][i]

# Demand constraints
for j in range(C):
    problem += pulp.lpSum(x[i, j] for i in range(P)) == data['demand'][j]

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')