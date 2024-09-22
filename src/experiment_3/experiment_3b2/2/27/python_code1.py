import pulp
import json

# Data input
data = json.loads('{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}')

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(benefit[0])  # Number of cities

# Problem definition
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(K), range(L)), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(benefit[k][l] * x[k][l] for k in range(K) for l in range(L)) 
    - pulp.lpSum(communication[k][j] * cost[j][l] * x[k][l] * x[j][l] 
                 for k in range(K) for j in range(K) for l in range(L)),
    "Total_Benefit"
)

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += (pulp.lpSum(x[k][l] for l in range(L)) == 1, f"Dept_{k+1}_One_City")

# No city can host more than three departments
for l in range(L):
    problem += (pulp.lpSum(x[k][l] for k in range(K)) <= 3, f"City_{l+1}_Max_3_Depts")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')