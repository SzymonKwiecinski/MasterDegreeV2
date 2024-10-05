import pulp

# Data
benefit = [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]]
communication = [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]]
cost = [[5, 14, 13], [15, 5, 9], [13, 9, 10]]

num_departments = len(benefit)
num_cities = len(benefit[0])

departments = range(num_departments)
cities = range(num_cities)

# Problem
problem = pulp.LpProblem("DepartmentRelocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (departments, cities), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(benefit[k][l] * islocated[k][l] for k in departments for l in cities) +
    pulp.lpSum(communication[k][j] * cost[j][m] * islocated[k][l] * islocated[j][m] 
               for k in departments for j in departments for l in cities for m in cities)
)

# Constraints

# Each department can only be located in one city
for k in departments:
    problem += pulp.lpSum(islocated[k][l] for l in cities) == 1

# No more than three departments may be located in any city
for l in cities:
    problem += pulp.lpSum(islocated[k][l] for k in departments) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')