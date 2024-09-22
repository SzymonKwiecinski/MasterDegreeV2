import pulp
import json

# Data input
data = '''{
    "N": 3,
    "Start": [100.0, 50.0, 200.0],
    "Limit": [1000.0, 200.0, 3000.0],
    "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}'''

input_data = json.loads(data)

# Extracting data
N = input_data['N']
Start = input_data['Start']
Limit = input_data['Limit']
Rate = input_data['Rate']

# Define the problem
problem = pulp.LpProblem("Maximize_Currency", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), lowBound=0)

# Objective Function
problem += pulp.lpSum(x[i][N-1] * Rate[i][N-1] for i in range(N-1))

# Constraints
for i in range(N):
    # Initial Amount Constraint
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) <= Start[i] + \
                pulp.lpSum(x[j][i] * Rate[j][i] for j in range(N) if j != i), f"Initial_Amount_Constraint_{i}"

    # Exchange Limit Constraint
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) + \
                pulp.lpSum(x[j][i] * Rate[j][i] for j in range(N) if j != i) <= Limit[i], f"Exchange_Limit_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')