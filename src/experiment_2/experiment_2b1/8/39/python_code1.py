import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Extracting input parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the LP problem
problem = pulp.LpProblem("Min_Employees", pulp.LpMinimize)

# Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # Set upper bound for total_number

# Objective: minimize total_number
problem += total_number

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num[n]

for i in range(100):
    for n in range(N):
        for d in range(n_working_days):
            if n + d < N:
                problem += is_work[n][i] <= pulp.lpSum(is_work[n + d][j] for j in range(100))

# Solve the problem
problem.solve()

# Prepare the output
result = {
    "total_number": int(pulp.value(total_number)),
    "is_work": [[int(is_work[n][i].varValue) for n in range(N)] for i in range(int(pulp.value(total_number)))]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')