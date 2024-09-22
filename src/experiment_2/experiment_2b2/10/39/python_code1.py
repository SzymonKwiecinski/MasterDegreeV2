import pulp

# Parse the input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Extract parameters
num = data["num"]
n_working_days = data["n_working_days"]
n_resting_days = data["n_resting_days"]
N = len(num)

# Problem definition
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Variables
# binary variables indicate if employee i starts working on day n
# maximum possible employees can be equal to sum(num), but initializing variables with this should be optimized
x = pulp.LpVariable.dicts("x", ((i, n) for i in range(sum(num)) for n in range(N)), 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum(x[i, n] for i in range(sum(num)) for n in range(N)), "Minimize total employees hired"

# Constraints
for n in range(N):
    problem += (
        pulp.lpSum(x[i, (n - d) % N] for i in range(sum(num)) for d in range(n_working_days) if (n - d) % N >= 0) >= num[n],
        f"Requirement_Day_{n+1}"
    )

# Solve the problem
problem.solve()

# Retrieve the results
hired_employees = set()
is_work = []

for i in range(sum(num)):
    work_schedule = [0] * N
    for n in range(N):
        if pulp.value(x[i, n]) == 1:
            hired_employees.add(i)
            for d in range(n_working_days):
                work_schedule[(n + d) % N] = 1
            break  # Exit early if an employee is found working on a start day
    if i in hired_employees:
        is_work.append(work_schedule)

total_number = len(is_work)

# Output the results
output = {
    "total_number": total_number,
    "is_work": is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')