import pulp

# Parse the input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Number of days
N = len(num)

# Define the problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

# Define decision variables
# x_i: 1 if employee i is hired, 0 otherwise
x = [pulp.LpVariable(f'x{i}', cat='Binary') for i in range(N)]

# y_i_j: 1 if employee i works on day j, 0 otherwise
y = [[pulp.LpVariable(f'y{i}_{j}', cat='Binary') for j in range(N)] for i in range(N)]

# Add objective: Minimize the number of employees
problem += pulp.lpSum(x), "Minimize_Employees"

# Add constraints
# Ensure each day's staffing requirements are met
for day in range(N):
    problem += pulp.lpSum(y[i][day] for i in range(N)) >= num[day], f"Staffing_Requirement_Day_{day}"

# Ensure the scheduled working and rest days for each employee
for i in range(N):
    for j in range(N):
        if j + n_working_days <= N:
            # Employee can work for n_working_days straight
            problem += y[i][j] - pulp.lpSum(y[i][j + k] for k in range(n_working_days)) == 0, f"Working_Block_{i}_{j}"
        if j + n_working_days + n_resting_days <= N:
            # After working n_working_days, employee must rest for n_resting_days
            problem += pulp.lpSum(y[i][j + n_working_days + k] for k in range(n_resting_days)) == 0, f"Rest_Block_{i}_{j}"

# Ensure employee i works only if they are hired
for i in range(N):
    for j in range(N):
        problem += y[i][j] <= x[i], f"Working_If_Hired_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare the output
total_number = sum(pulp.value(x[i]) for i in range(N))
is_work = [[int(pulp.value(y[i][j])) for j in range(N)] for i in range(N)]

output = {
    "total_number": int(total_number),
    "is_work": [is_work[i] for i in range(N) if pulp.value(x[i]) == 1]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(output)