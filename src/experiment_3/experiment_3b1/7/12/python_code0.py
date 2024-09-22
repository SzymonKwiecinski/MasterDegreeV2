import pulp
import json

# Data provided as JSON
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the problem variable
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Create decision variables for the amounts exchanged
x = pulp.LpVariable.dicts("x", (range(1, N + 1), range(1, N + 1)), lowBound=0)

# Define the objective function
y_N = pulp.LpVariable("y_N", lowBound=0)
problem += y_N, "Maximize_Final_Currency_N"

# Set constraints for each currency i
for i in range(1, N + 1):
    problem += pulp.lpSum(x[i][j] for j in range(1, N + 1)) <= limit[i - 1], f"Limit_{i}"

# Define the equation for final amount of currency N
problem += y_N == start[N - 1] + pulp.lpSum(x[j][N] for j in range(1, N + 1)) - pulp.lpSum(x[N][k] for k in range(1, N + 1)), "Final_Amount_Currency_N"

# Set constraints for outflow of currency i
for i in range(1, N + 1):
    problem += pulp.lpSum(x[i][j] for j in range(1, N + 1)) - pulp.lpSum(x[k][i] for k in range(1, N + 1)) <= start[i - 1], f"Outflow_Constraint_{i}"

# Set rate constraints
for i in range(1, N + 1):
    for j in range(1, N + 1):
        problem += x[i][j] <= rate[i - 1][j - 1] * start[i - 1], f"Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')