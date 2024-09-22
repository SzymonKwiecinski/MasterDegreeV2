import pulp
import json

# Data Initialization
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective Function: Maximize the amount of currency N
problem += pulp.lpSum(x[N-1][j] for j in range(N)), "Total_Value"

# Constraints
# Exchange Limit Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Initial Amount Constraints
for i in range(N):
    for j in range(N):
        problem += x[i][j] <= start[i], f"Start_Constraint_{i}_{j}"

# Wealth Conservation Constraints
for i in range(N):
    problem += start[i] - pulp.lpSum(x[i][j] for j in range(N)) + \
               pulp.lpSum(x[j][i] * rate[j][i] for j in range(N)) == start[i], f"Wealth_Conservation_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')