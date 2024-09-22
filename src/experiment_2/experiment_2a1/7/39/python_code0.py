import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
num_needed = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_needed)

# Problem definition
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable("total_number", lowBound=1, cat='Integer')  # Total number of employees
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), cat='Binary')

# Objective Function
problem += total_number

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number)) >= num_needed[n]

for i in range(total_number):
    for n in range(N):
        for j in range(n_working_days):
            if (n + j) < N:
                problem += is_work[(n, i)] <= pulp.lpSum(is_work[(n + j, k)] for k in range(total_number))

# Solve the problem
problem.solve()

# Extracting results
total_employees = int(pulp.value(total_number))
is_work_schedule = [[int(is_work[(n, i)].value()) for n in range(N)] for i in range(total_employees)]

# Prepare the output
output = {
    "total_number": total_employees,
    "is_work": is_work_schedule
}

print(json.dumps(output))

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')