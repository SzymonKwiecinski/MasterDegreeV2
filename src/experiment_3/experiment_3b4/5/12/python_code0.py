import pulp

# Data
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

# Variables
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(x[(i, N-1)] * rate[i][N-1] for i in range(N)), "Maximize_Final_Currency"

# Constraints
# Constraint 1: Sum of exchanges cannot exceed start amount plus received amounts
for i in range(N):
    problem += pulp.lpSum(x[(i, j)] for j in range(N) if i != j) <= start[i] + pulp.lpSum(x[(k, i)] * rate[k][i] for k in range(N) if k != i)

# Constraint 2: Exchanged amount cannot exceed its limit
for i in range(N):
    problem += pulp.lpSum(x[(i, j)] for j in range(N) if i != j) <= limit[i]

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')