import pulp

# Parsing the input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision variables
# is_work[i][n] represents if employee i is working on day n
is_work = []
for i in range(sum(num)):
    is_work.append([pulp.LpVariable(f'is_work_{i}_{n}', cat='Binary') for n in range(N)])

# Objective function: minimize number of employees
num_employees = pulp.LpVariable('num_employees', lowBound=0, cat='Integer')
problem += num_employees

# Constraints
for n in range(N):
    # Ensure the number of employees working each day is at least the number required
    problem += sum(is_work[i][n] for i in range(sum(num))) >= num[n]

    # Define working patterns: working "n_working_days" followed by "n_resting_days" rest
    for i in range(sum(num)):
        for start_day in range(N):
            end_day = start_day + n_working_days + n_resting_days
            if end_day <= N:
                problem += sum(is_work[i][day] for day in range(start_day, start_day + n_working_days)) >= n_working_days * is_work[i][start_day]
                if end_day < N:
                    problem += is_work[i][end_day] <= 1 - is_work[i][start_day]

# Constraint to determine num_employees
for i in range(sum(num)):
    problem += num_employees >= pulp.lpSum(is_work[i][n] for n in range(N))

# Solve the problem
problem.solve()

# Extracting results
is_work_result = [[int(is_work[i][n].varValue) for n in range(N)] for i in range(sum(num)) if any(is_work[i][n].varValue for n in range(N))]
total_number = len(is_work_result)

output = {
    "total_number": total_number,
    "is_work": is_work_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')