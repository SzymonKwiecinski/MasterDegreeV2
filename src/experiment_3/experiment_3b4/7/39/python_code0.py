import pulp

# Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
N = len(data['num'])
M = 50  # Assuming a large enough number for potential employees
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Problem
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

# Variables
z = [pulp.LpVariable(f'z_{i}', cat='Binary') for i in range(M)]
x = [[pulp.LpVariable(f'x_{i}_{n}', cat='Binary') for n in range(N)] for i in range(M)]

# Objective
problem += pulp.lpSum(z)

# Constraints
# Ensure enough employees work each day
for n in range(N):
    problem += pulp.lpSum(x[i][n] for i in range(M)) >= data['num'][n]

# Ensure z_i = 1 if any x_i_n = 1
for i in range(M):
    for n in range(N):
        problem += z[i] >= x[i][n]

# Ensure working and resting cycles
# Each employee works for n_working_days followed by n_resting_days
for i in range(M):
    is_working = False
    for n in range(N):
        if is_working:
            # If within working days
            if n % (n_working_days + n_resting_days) < n_working_days:
                # Employee can work this day
                continue
            else:
                # Employee must not work on resting days
                problem += x[i][n] == 0

# Solve the problem
problem.solve()

# Output the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')