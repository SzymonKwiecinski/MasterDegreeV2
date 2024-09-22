import pulp

# Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

N = len(num)  # Number of days
I = 6  # Number of employees (assuming as per length of num)

# Create the problem
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(I), cat='Binary')  # Hiring decision
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(I)), cat='Binary')  # Work schedule

# Objective Function
problem += pulp.lpSum([x[i] for i in range(I)])

# Constraints
# (1) Ensure the required number of employees work each day
for n in range(N):
    problem += pulp.lpSum([is_work[n][i] for i in range(I)]) >= num[n]

# (2) An employee can only work if they are hired
for n in range(N):
    for i in range(I):
        problem += is_work[n][i] <= x[i]

# (3) Working days follow a set pattern
for n in range(N - n_working_days + 1):
    for i in range(I):
        problem += pulp.lpSum([is_work[n + k][i] for k in range(n_working_days)]) == n_working_days * x[i]

# (4) Resting days after working days
for n in range(N - n_working_days - n_resting_days + 1):
    for i in range(I):
        problem += pulp.lpSum([is_work[n + k][i] for k in range(n_working_days, n_working_days + n_resting_days)]) == 0

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')