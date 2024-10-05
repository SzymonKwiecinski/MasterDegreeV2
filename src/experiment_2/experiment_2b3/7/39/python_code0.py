import pulp

# Data input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Unpacking the data
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

# Decision variable for the number of employees
x = pulp.LpVariable('x', lowBound=0, cat='Integer')

# Decision variables for whether an employee is working on a given day
is_work = [[pulp.LpVariable(f'is_work_{n}_{i}', cat='Binary') for n in range(N)] for i in range(N)]

# Objective: Minimize the number of employees
problem += x

# Constraints:
# Ensure the minimum required employees are working on each day
for n in range(N):
    problem += pulp.lpSum(is_work[i][n] for i in range(N)) >= num[n]

# Ensure each employee works n_working_days followed by n_resting_days off
for i in range(N):
    for n in range(N):
        if n + n_working_days + n_resting_days <= N:
            problem += pulp.lpSum(is_work[i][j] for j in range(n, n + n_working_days)) <= n_working_days
            for k in range(n + n_working_days, n + n_working_days + n_resting_days):
                problem += is_work[i][k] == 0

# Solve the problem
problem.solve()

# Extract the number of employees and their schedules
total_number = int(pulp.value(x))
is_work_result = [[int(pulp.value(is_work[i][n])) for n in range(N)] for i in range(total_number)]

# Output result
output = {
    "total_number": total_number,
    "is_work": is_work_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')