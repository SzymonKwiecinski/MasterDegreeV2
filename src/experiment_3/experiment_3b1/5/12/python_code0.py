import pulp
import json

# Data in JSON format
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

# Extract data
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("exchange", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective Function
problem += pulp.lpSum(x[(N-1, j)] * rate[N-1][j] for j in range(N)), "Total_Amount_in_Currency_N"

# Constraints
# Limit on the amount of currency that can be exchanged
for i in range(N):
    problem += pulp.lpSum(x[(i, j)] for j in range(N)) <= limit[i], f"Limit_Currency_{i+1}"

# Start amount constraints
for i in range(N):
    problem += pulp.lpSum(x[(j, i)] for j in range(N)) <= start[i], f"Start_Amount_Currency_{i+1}"

# Flow conservation
for i in range(N):
    problem += (pulp.lpSum(x[(i, j)] for j in range(N)) - 
                 pulp.lpSum(x[(j, i)] for j in range(N))) == 0, f"Flow_Conservation_Currency_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')