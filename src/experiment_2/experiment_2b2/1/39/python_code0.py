import pulp

# Define the problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

# Extract data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Decision variables
# x_i indicates if employee i is hired
# is_work[n][i] indicates if employee i is working on day n
x = [pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(N)]
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(N)), 
                                cat='Binary')

# Objective function: Minimize the total number of employees
problem += pulp.lpSum(x)

# Constraints
# Each day's requirement must be met
for n in range(N):
    problem += pulp.lpSum(is_work[n, i] for i in range(N)) >= num[n]

# Employee schedule constraints
for i in range(N):
    for n in range(N):
        # Employee can only work if hired
        problem += is_work[n, i] <= x[i]
    
    # Ensure each employee works consecutively for n_working_days and rests for n_resting_days
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(is_work[k, i] for k in range(n, n + n_working_days)) == n_working_days * x[i]

    for n in range(n_working_days, N - n_resting_days + 1):
        problem += pulp.lpSum(is_work[k, i] for k in range(n, n + n_resting_days)) == 0

# Solve the problem
problem.solve()

# Extract the results
total_number = sum(x[i].varValue for i in range(N))
is_work_schedule = [[int(is_work[n, i].varValue) for n in range(N)] for i in range(N) if x[i].varValue > 0]

# Prepare the output in the specified format
output = {
    "total_number": int(total_number),
    "is_work": is_work_schedule
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')