import pulp
import json

# Data provided in JSON format
data = json.loads("{'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}")

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Maximize_Z", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective function
problem += pulp.lpSum(Rate[i][N-1] * x[i, N-1] for i in range(N-1)), "Objective"

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= Start[i], f"Start_Constraint_{i}"

for i in range(N):
    problem += (pulp.lpSum(x[i, j] for j in range(N)) +
                 pulp.lpSum(x[j, i] / Rate[j][i] for j in range(N))) <= Limit[i], f"Limit_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')