import pulp
import json

# Load data
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)
y = pulp.LpVariable.dicts("y", (i for i in range(N)))

# Objective function
problem += y[N - 1], "Maximize_Final_Currency"

# Constraints
for i in range(N):
    # Constraint for final amounts
    problem += y[i] == start[i] + sum(rate[j][i] * x[j, i] for j in range(N)) - sum(x[i, j] for j in range(N)), f"Final_Amount_Constraint_{i}"
    
    # Constraint for limits
    problem += sum(x[i, j] + x[j, i] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')