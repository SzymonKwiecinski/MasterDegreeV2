import pulp
import json

# Data input
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create the linear programming problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)  # x[i][j]
y = pulp.LpVariable.dicts("y", range(N), lowBound=0)                # y[i]

# Objective function: maximize y[N-1]
problem += y[N-1], "Objective"

# Constraints
for i in range(N):
    # Initial Amount Constraint
    problem += (y[i] == Start[i] + sum(x[j][i] for j in range(N)) - sum(x[i][j] for j in range(N))), f"Initial_Amount_Constraint_{i}"

    # Limit Constraints
    problem += (sum(x[i][j] for j in range(N)) + sum(x[j][i] for j in range(N)) <= Limit[i]), f"Limit_Constraint_{i}"

    # Exchange Rate Constraints
    for j in range(N):
        problem += (x[i][j] <= Start[i] * Rate[i][j]), f"Exchange_Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')