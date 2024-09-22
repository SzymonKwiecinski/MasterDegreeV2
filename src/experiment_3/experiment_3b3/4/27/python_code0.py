import pulp

# Data 
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], 
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

K = range(len(data['benefit']))  # Set of departments
L = range(len(data['benefit'][0]))  # Set of cities

# Initialize the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in K for l in L), cat='Binary')

# Objective Function
total_cost = pulp.lpSum(data['communication'][k][j] * data['cost'][l][m] * islocated[k, l] for k in K for j in K for l in L for m in L) 
total_benefit = pulp.lpSum(data['benefit'][k][l] * islocated[k, l] for k in K for l in L)

problem += total_cost - total_benefit

# Constraints

# Each department must be located in exactly one city
for k in K:
    problem += pulp.lpSum(islocated[k, l] for l in L) == 1

# No city can have more than three departments
for l in L:
    problem += pulp.lpSum(islocated[k, l] for k in K) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')