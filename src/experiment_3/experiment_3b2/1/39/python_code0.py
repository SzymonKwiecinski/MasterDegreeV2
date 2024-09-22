import pulp

# Data from JSON
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)  # Number of days

# Create the LP problem
problem = pulp.LpProblem("Employee_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), cat='Binary')  # Employee hired
y = pulp.LpVariable.dicts("y", (range(N), range(N)), cat='Binary')  # Employee work schedule

# Objective function: Minimize number of employees hired
problem += pulp.lpSum(x[i] for i in range(N))

# Constraints
# 1. Required number of employees for each day
for n in range(N):
    problem += pulp.lpSum(y[n][i] for i in range(N)) >= num[n]

# 2. An employee can only work if they are hired
for n in range(N):
    for i in range(N):
        problem += y[n][i] <= x[i]

# 3. Work/rest cycle constraints
for i in range(N):
    for n in range(N - n_working_days - n_resting_days + 1):
        problem += (1 - pulp.lpSum(y[n + j][i] for j in range(n_working_days))) + \
                   pulp.lpSum(y[n + j][i] for j in range(n_working_days, n_working_days + n_resting_days)) <= \
                   n_resting_days * (1 - x[i])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')