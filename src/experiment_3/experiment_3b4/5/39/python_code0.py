import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Number of days and large M value representing the potential pool of employees
N = len(num)
M = sum(num)  # a safe upper bound on the number of employees

# Define the problem
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(M), cat=pulp.LpBinary)
y = pulp.LpVariable.dicts("y", ((n, i) for n in range(N) for i in range(M)), cat=pulp.LpBinary)

# Objective function: Minimize the number of employees hired
problem += pulp.lpSum(x[i] for i in range(M))

# Constraints

# 1. Each day must have the required number of employees
for n in range(N):
    problem += pulp.lpSum(y[(n, i)] for i in range(M)) >= num[n]

# 2. Work/rest cycle constraints
for i in range(M):
    for n in range(N):
        # If the employee is hired, ensure they follow the working and resting pattern
        if n + n_working_days + n_resting_days <= N:
            for k in range(n_working_days):
                problem += y[(n + k, i)] <= x[i]
            for k in range(n_working_days, n_working_days + n_resting_days):
                problem += y[(n + k, i)] == 0
        # Ensure no working without being hired
        problem += y[(n, i)] <= x[i]

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')