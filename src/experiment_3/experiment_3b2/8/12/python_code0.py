import pulp
import json

# Data input in JSON format
data = '{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}'
data = json.loads(data)

# Extract data
N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function
problem += (Start[2] + pulp.lpSum(x[i][2] * Rate[i][2] for i in range(N-1)) - 
            pulp.lpSum(x[2][j] for j in range(N-1))), "Objective"

# Constraints
for i in range(N):
    if i != 2:  # for currencies other than N (index 2)
        problem += (pulp.lpSum(x[i][j] for j in range(N)) - 
                     pulp.lpSum(x[j][i] for j in range(N)) <= Start[i]), f"Balance_Constraint_{i}"

for i in range(N):
    problem += (pulp.lpSum(x[i][j] + x[j][i] for j in range(N)) <= Limit[i]), f"Limit_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')