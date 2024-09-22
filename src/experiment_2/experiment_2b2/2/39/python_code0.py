import pulp

# Load data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data["num"]
n_working_days = data["n_working_days"]
n_resting_days = data["n_resting_days"]
N = len(num)  # Total number of days

# Initialize the problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

# Define the variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = []
for i in range(N):
    is_work_i = pulp.LpVariable.dicts(f"is_work_{i}", range(N), lowBound=0, upBound=1, cat='Binary')
    is_work.append(is_work_i)

# Objective function: Minimize total number of employees
problem += total_number

# Constraints
for day in range(N):
    # The number of employees working on any given day must be at least num[day]
    problem += pulp.lpSum([is_work[i][day] for i in range(N)]) >= num[day]

# Each employee must work consecutively n_working_days and then rest for n_resting_days.
# This constraint is applied cyclically over the N days.
for i in range(N):
    for start_day in range(N):
        work_days = [is_work[i][(start_day + d) % N] for d in range(n_working_days)]
        rest_days = [is_work[i][(start_day + n_working_days + r) % N] for r in range(n_resting_days)]
        # If working, all work_days must be 1, all rest_days must be 0
        problem += pulp.lpSum(work_days) >= n_working_days * is_work[i][start_day]
        problem += pulp.lpSum(rest_days) <= (1 - is_work[i][start_day]) * n_resting_days

# Each employee's total work days over the period must be less than or equal to total_number
for i in range(N):
    problem += pulp.lpSum(is_work[i][day] for day in range(N)) <= total_number

# Solve the problem
problem.solve()

# Extract the solution
total_number = int(pulp.value(problem.objective))
is_work_solution = [[int(pulp.value(is_work[i][n])) for n in range(N)] for i in range(N)]

# Prepare the output
output_data = {
    "total_number": total_number,
    "is_work": is_work_solution
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(output_data)