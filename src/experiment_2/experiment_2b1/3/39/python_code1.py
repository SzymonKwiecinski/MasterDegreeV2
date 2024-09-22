import pulp
import json

# Input data
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')

# Parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts('is_work', (range(N), range(n_working_days + n_resting_days)), cat='Binary')

# Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Objective: Minimize the total number of employees
problem += total_number

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(n_working_days)) >= num[n]

# Each employee's working pattern
for i in range(total_number):
    for n in range(N):
        for j in range(n_working_days):
            problem += is_work[n][j] <= 1  # Employee can only work one shift per working day

# Adding rest days constraint
for n in range(N):
    for i in range(total_number):
        for j in range(n_working_days):
            problem += is_work[n][j] + is_work[n + n_working_days][j] <= 1

# Solve the problem
problem.solve()

# Prepare output
output = {
    "total_number": pulp.value(total_number),
    "is_work": [[pulp.value(is_work[n][i]) for n in range(N)] for i in range(total_number)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')