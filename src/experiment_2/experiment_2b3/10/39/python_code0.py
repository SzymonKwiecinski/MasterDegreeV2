import pulp

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
N = len(num)
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

# Decision variables
# x[i] is 1 if we hire the ith employee, 0 otherwise, up to some reasonable maximum number of employees
max_employees = sum(num)  # Upper bound on the number of employees needed
x = [pulp.LpVariable(f'x_{i}', cat='Binary') for i in range(max_employees)]

# y[n][i] is 1 if the ith employee works on the nth day, 0 otherwise
# This is a binary matrix of size (max_employees x N)
y = [[pulp.LpVariable(f'y_{i}_{n}', cat='Binary') for n in range(N)] for i in range(max_employees)]

# Objective: Minimize the number of employees
problem += pulp.lpSum(x)

# Constraints
# Each day `n`, the number of working employees must be at least `num[n]`
for n in range(N):
    problem += pulp.lpSum(y[i][n] for i in range(max_employees)) >= num[n]

# Working pattern constraints: If employee `i` is hired, they work `n_working_days` days in a row and then `n_resting_days` rest
for i in range(max_employees):
    for start in range(N):
        # Calculate which days the employee works if they start on a given day
        for j in range(n_working_days):
            if start + j < N:
                problem += y[i][start + j] <= x[i]
        # Calculate which days the employee rests after working
        for j in range(n_resting_days):
            if start + n_working_days + j < N:
                problem += y[i][start + n_working_days + j] == 0

# Solve the problem
problem.solve()

# Extract results
total_number = int(pulp.value(problem.objective))
is_work = [[int(pulp.value(y[i][n])) for n in range(N)] for i in range(total_number) if pulp.value(x[i]) == 1]

# Output
output = {
    "total_number": total_number,
    "is_work": is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')