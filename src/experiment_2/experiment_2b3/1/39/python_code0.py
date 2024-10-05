import pulp

# Data input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Unpack the data
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Define the problem
problem = pulp.LpProblem("Minimum_Employees", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = [
    [pulp.LpVariable(f'is_work_{n}_{i}', cat='Binary') for n in range(N)]
    for i in range(N)
]

# Objective function: Minimize the total number of employees
problem += total_number

# Constraints
# Each day must be staffed by the required number of employees
for n in range(N):
    problem += pulp.lpSum(is_work[i][n] for i in range(N)) >= num[n]

# Working and Rest periods constraint for each possible employee
for i in range(N):
    for n in range(N):
        # Employee works n_working_days and rests n_resting_days in a cycle
        for k in range(n_working_days):
            if n + k < N:
                problem += is_work[i][n + k] <= total_number
        for k in range(n_working_days, n_working_days + n_resting_days):
            if n + k < N:
                problem += is_work[i][n + k] == 0

# Solve the problem
problem.solve()

# Extract results
total_number_result = int(pulp.value(total_number))
is_work_result = [[int(pulp.value(is_work[i][n])) for n in range(N)] for i in range(total_number_result)]

# Output
output = {
    "total_number": total_number_result,
    "is_work": is_work_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')