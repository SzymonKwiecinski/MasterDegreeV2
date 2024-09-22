import pulp

# Data from the problem
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Number of days
N = len(num)

# Problem
problem = pulp.LpProblem("MinimizeEmployees", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Employee_", range(N), 0, cat=pulp.LpInteger)

# Objective function: Minimize the total number of employees (sum of x)
problem += pulp.lpSum(x[i] for i in range(N)), "TotalEmployees"

# Constraints
for day in range(N):
    problem += pulp.lpSum(x[(day - start) % N] for start in range(n_working_days)) >= num[day], f"StaffRequirement_day{day}"

# Solve the problem
problem.solve()

# Extract the results
total_number = sum(x[i].varValue for i in range(N))
is_work = [[0]*N for _ in range(int(total_number))]

# Assign working days to each employee
employee_counter = 0
for start in range(N):
    for e in range(int(x[start].varValue)):
        for k in range(n_working_days):
            is_work[employee_counter][(start + k) % N] = 1
        employee_counter += 1

# Format the result
result = {
    "total_number": int(total_number),
    "is_work": is_work
}

result