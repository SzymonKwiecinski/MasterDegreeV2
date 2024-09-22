import pulp
import json

# Data parsing
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Currency", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function
problem += pulp.lpSum(x[i][j] for j in range(N) for i in range(N) if i != j)

# Constraints
for i in range(N):
    # Exchange Limit
    problem += pulp.lpSum(x[i][j] for j in range(N) if i != j) <= Limit[i]
    
    # Starting Amount Constraint
    problem += Start[i] + pulp.lpSum(x[j][i] for j in range(N) if j != i) - pulp.lpSum(x[i][j] for j in range(N) if i != j) == 0

    # Transaction Rates
    for j in range(N):
        if i != j:
            problem += x[i][j] <= Rate[i][j] * Start[i]

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')