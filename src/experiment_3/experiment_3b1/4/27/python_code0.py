import pulp
import json

# Data input
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], 
                     [0.0, 0.0, 1.4, 1.2, 0.0], 
                     [1.0, 1.4, 0.0, 0.0, 2.0], 
                     [1.5, 1.2, 0.0, 2.0, 0.7], 
                     [0.0, 0.0, 2.0, 0.7, 0.0]], 
    'cost': [[5, 14, 13], 
             [15, 5, 9], 
             [13, 9, 10]]
}

# Indices
K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of cities

# Create the problem variable
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variable
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective Function
objective = pulp.lpSum(data['benefit'][k][l] * islocated[(k, l)] for k in range(K) for l in range(L)) + \
            pulp.lpSum(data['communication'][k][j] * data['cost'][l][m] * islocated[(k, l)] * islocated[(j, m)] 
                        for k in range(K) for j in range(K) for l in range(L) for m in range(L))

problem += objective, "Total_Yearly_Cost"

# Constraints
# Each department can only be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(L)) == 1, f"One_City_Per_Department_{k}"

# No city may have more than three departments located in it
for l in range(L):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(K)) <= 3, f"No_More_Than_Three_In_City_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')