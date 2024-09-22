import pulp

# Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)

# Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Variables
x = pulp.LpVariable('x', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts('is_work', ((n, i) for n in range(N) for i in range(N)), cat='Binary')

# Objective Function
problem += x

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(N)) >= num_n[n]

for i in range(N):
    for n in range(N):
        # Working days constraint
        if n + n_working_days - 1 < N:
            problem += pulp.lpSum(is_work[(n + k, i)] for k in range(n_working_days)) <= n_working_days
        # Resting days constraint
        if n + n_working_days + n_resting_days - 1 < N:
            problem += pulp.lpSum(is_work[(n + n_working_days + k, i)] for k in range(n_resting_days)) == 0

# Solve the problem
problem.solve()

# Display results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
total_number = pulp.value(x)
is_work_status = {(n, i): is_work[(n, i)].varValue for n in range(N) for i in range(N)}

print("Total number of employees hired:", total_number)
print("Working Status Matrix:")
for n in range(N):
    for i in range(N):
        print(f"Day {n} Employee {i}: ", is_work_status[(n, i)])