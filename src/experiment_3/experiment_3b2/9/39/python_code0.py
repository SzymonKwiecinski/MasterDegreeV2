import pulp

# Data from the JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
N = len(data['num'])
M = N  # Number of decision variables x_i corresponds to N
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Create the LP problem
problem = pulp.LpProblem("Minimize_x", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(M), cat='Binary')
y = pulp.LpVariable.dicts("y", (range(M), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(x[i] for i in range(M))

# Constraints
# Constraint 1: sum_{i=1}^{M} y_{i,n} >= num_n for all n
for n in range(N):
    problem += pulp.lpSum(y[i][n] for i in range(M)) >= data['num'][n], f"Constraint_1_n_{n}"

# Constraint 2: sum_{j=0}^{n_working_days-1} y_{i,n+j} <= n_working_days * x_i for all i, n
for i in range(M):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(y[i][n + j] for j in range(n_working_days)) <= n_working_days * x[i], f"Constraint_2_i_{i}_n_{n}"

# Constraint 3: sum_{j=n_working_days}^{n_working_days+n_resting_days-1} y_{i,n+j} = 0 for all i, n
for i in range(M):
    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(y[i][n + j] for j in range(n_working_days, n_working_days + n_resting_days)) == 0, f"Constraint_3_i_{i}_n_{n}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')