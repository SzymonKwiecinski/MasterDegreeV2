import pulp

# Data from input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Unpack data
num_employees_required = data["num"]
n_working_days = data["n_working_days"]
n_resting_days = data["n_resting_days"]
N = len(num_employees_required)

# Define the LP problem
problem = pulp.LpProblem("Minimum_Employees_Hiring", pulp.LpMinimize)

# Decision variables
# Let's assume a large enough upper bound for the number of employees
max_possible_employees = sum(num_employees_required)
is_work = [
    [
        pulp.LpVariable(f"is_work_{i}_{n}", cat='Binary')
        for n in range(N)
    ]
    for i in range(max_possible_employees)
]

# Objective function
# Minimize total number of employees hired
total_number = pulp.LpVariable("total_number", lowBound=0, cat="Continuous")
problem += total_number

# Constraints
# Each day n must have at least num_employees_required[n] employees working
for n in range(N):
    problem += pulp.lpSum(is_work[i][n] for i in range(max_possible_employees)) >= num_employees_required[n]

# Working and resting pattern constraint
for i in range(max_possible_employees):
    for n in range(N):
        if n + n_working_days + n_resting_days <= N:
            # If working day starts on day n, ensure it forms a cycle with working and resting days
            for j in range(n_working_days):
                problem += is_work[i][n + j] <= 1
            for j in range(n_working_days, n_working_days + n_resting_days):
                problem += is_work[i][n + j] == 0

# Additional constraint to link total_number with actual employee usage
for i in range(max_possible_employees):
    for n in range(N):
        problem += total_number >= is_work[i][n]

# Solve the problem
problem.solve()

# Extract the results
hired_employees = [
    [int(pulp.value(is_work[i][n])) for n in range(N)]
    for i in range(max_possible_employees)
]

# Filter out employees who are not working at all
final_hired_employees = [emp for emp in hired_employees if sum(emp) > 0]

output = {
    "total_number": len(final_hired_employees),
    "is_work": final_hired_employees
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')