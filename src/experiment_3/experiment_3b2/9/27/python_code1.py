import pulp
import json

data = json.loads('{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}')

K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of cities

# Create a linear programming problem
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(K), range(L)), cat='Binary')

# Objective function
problem += -pulp.lpSum(data['benefit'][k][l] * x[k][l] for k in range(K) for l in range(L)) + \
    pulp.lpSum(data['communication'][k][j] * data['cost'][j][m] * x[k][l] * x[j][m]
                for k in range(K) for j in range(K) for l in range(L) for m in range(L))

# Constraints
for k in range(K):
    problem += pulp.lpSum(x[k][l] for l in range(L)) == 1  # Each department must be in one city

for l in range(L):
    problem += pulp.lpSum(x[k][l] for k in range(K)) <= 3  # No city can have more than 3 departments

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')