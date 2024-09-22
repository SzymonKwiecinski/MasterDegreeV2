import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Extract data
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Problem definition
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

# Variables
# Minimum employees needed, initialized to a large number
max_employees_possible = sum(num)  

# Create decision variables
work_plan = pulp.LpVariable.dicts("work_plan", ((i, n) for i in range(max_employees_possible) for n in range(N)), cat='Binary')
employed = pulp.LpVariable.dicts("employed", (i for i in range(max_employees_possible)), lowBound=0, upBound=1, cat='Integer')

# Objective function: Minimize total number of employees hired
problem += pulp.lpSum(employed[i] for i in range(max_employees_possible))

# Constraints
for n in range(N):
    # Ensure enough employees on each day
    problem += pulp.lpSum(work_plan[i, n] for i in range(max_employees_possible)) >= num[n]

for i in range(max_employees_possible):
    for n in range(N):
        # Employee i can only work if they are employed
        problem += work_plan[i, n] <= employed[i]

        # Ensure working schedule is consistent: n_working_days followed by n_resting_days
        if n + n_working_days + n_resting_days <= N:
            # Working days constraint
            problem += pulp.lpSum(work_plan[i, n + k] for k in range(n_working_days)) >= \
                       n_working_days * (work_plan[i, n] - work_plan[i, n + n_working_days])
            # Resting days constraint
            for k in range(n_resting_days):
                problem += work_plan[i, n + n_working_days + k] <= (1 - work_plan[i, n] + work_plan[i, n + n_working_days])

# Solve the problem
problem.solve()

# Output the results
total_number = int(pulp.value(problem.objective))
is_work = [[int(pulp.value(work_plan[i, n])) for n in range(N)] for i in range(total_number)]

output = {
    "total_number": total_number,
    "is_work": is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')