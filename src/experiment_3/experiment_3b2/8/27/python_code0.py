import pulp
import json

# Data in JSON format
data_json = '{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}'
data = json.loads(data_json)

# Extract data from json
benefit = data['benefit']
communication = data['communication']
cost = data['cost']
K = len(benefit)  # Number of k
L = len(benefit[0])  # Number of l
M = len(cost)  # Number of m

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost_Benefit", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(K), range(L)), cat='Binary')

# Objective function
problem += (
    -pulp.lpSum(benefit[k][l] * x[k][l] for k in range(K) for l in range(L)) +
    pulp.lpSum(communication[k][j] * cost[l][m] * x[k][l] * x[j][m]
                for k in range(K) for j in range(K) for l in range(L) for m in range(M))
)

# Constraints
for k in range(K):
    problem += pulp.lpSum(x[k][l] for l in range(L)) == 1, f"Constraint_1_for_k_{k}"

for l in range(L):
    problem += pulp.lpSum(x[k][l] for k in range(K)) <= 3, f"Constraint_2_for_l_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')