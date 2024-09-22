import pulp

# Data from JSON
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [
        [0.99, 0.9, 1.02],
        [0.95, 0.99, 0.92],
        [0.9, 0.91, 0.99]
    ]
}

# Parameters
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Problem Initialization
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision Variables
x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0) for j in range(N)] for i in range(N)]

# Objective Function
problem += pulp.lpSum(x[i][N-1] * rate[i][N-1] for i in range(N))

# Constraints

# 1. Exchange Limit Constraint
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limit[i]

# 2. Initial Currency Constraint
for i in range(N):
    problem += pulp.lpSum(x[j][i] * rate[j][i] for j in range(N)) <= start[i] + pulp.lpSum(x[i][k] for k in range(N))

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')