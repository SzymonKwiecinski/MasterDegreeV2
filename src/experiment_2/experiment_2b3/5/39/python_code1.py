import pulp

# Data input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

total_days = len(num)

# Initialize the problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

# Decision variables
max_employees = sum(num)
is_work = [[pulp.LpVariable(f"is_work_{i}_{n}", cat='Binary') for n in range(total_days)] for i in range(max_employees)]

# Objective: Minimize the number of employees
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
problem += total_number

# Constraints
for n in range(total_days):
    problem += pulp.lpSum(is_work[i][n] for i in range(max_employees)) >= num[n]

for i in range(max_employees):
    for n in range(total_days):
        if n + n_working_days <= total_days:  # Correcting the condition to avoid index error
            problem += pulp.lpSum(is_work[i][n+m] for m in range(n_working_days)) <= total_number
        if n + n_working_days < total_days:  # Adjusting to check only when within bounds
            problem += pulp.lpSum(is_work[i][n+m] for m in range(n_working_days, n_working_days + n_resting_days)) == 0

problem.solve()

# Collect results
hired_employees = []
for i in range(max_employees):
    if any(pulp.value(is_work[i][n]) == 1 for n in range(total_days)):
        hired_employees.append([int(pulp.value(is_work[i][n])) for n in range(total_days)])

output = {
    "total_number": len(hired_employees),
    "is_work": hired_employees
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')