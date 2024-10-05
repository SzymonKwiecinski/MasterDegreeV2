from pulp import LpProblem, LpVariable, LpMinimize, lpSum, value
import json

# Data input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Problem definition
problem = LpProblem("Minimize_Employees", LpMinimize)

# Decision variables
is_work = LpVariable.dicts("Is_Work", [(i, j) for i in range(N) for j in range(N)], cat='Binary')

# Objective function: minimize total number of employees
problem += lpSum(is_work[i][j] for i in range(N) for j in range(N))

# Constraints

# Ensuring the required number of employees at each day
for j in range(N):
    problem += lpSum(is_work[i][j] for i in range(N)) >= num[j]

# Ensuring each employee works n_working_days followed by n_resting_days
for i in range(N):
    for j in range(N):
        if j + n_working_days + n_resting_days <= N:
            problem += lpSum(is_work[i][j+k] for k in range(n_working_days)) <= n_working_days * is_work[i][j]
            problem += lpSum(is_work[i][j+k] for k in range(n_working_days, n_working_days + n_resting_days)) == 0

# Solving the problem
problem.solve()

# Gathering the results
total_number = sum(1 for i in range(N) if sum(value(is_work[i][j]) for j in range(N)) > 0)
is_work_result = [[int(value(is_work[i][j])) for j in range(N)] for i in range(N) if sum(value(is_work[i][j]) for j in range(N)) > 0]

# Output format
output = {
    "total_number": total_number,
    "is_work": is_work_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')