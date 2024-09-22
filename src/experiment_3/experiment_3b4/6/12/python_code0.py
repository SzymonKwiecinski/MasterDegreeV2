import pulp

# Data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Problem
problem = pulp.LpProblem("Currency_Exchange_Optimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(x[i, N-1] * rate[i][N-1] for i in range(N)), "Total Amount of Currency N"

# Constraints
# Currency Exchange Limit Constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Starting Currency Constraints
for i in range(N):
    problem += pulp.lpSum(x[j, i] for j in range(N)) <= start[i], f"Start_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')