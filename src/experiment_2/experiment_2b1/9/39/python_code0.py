import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
num_required = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
total_days = len(num_required)

# Create a linear programming problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(total_days) for i in range(1, total_number + 1)), cat='Binary')

# Objective function: Minimize the total number of employees
problem += total_number

# Constraints for the required staff
for n in range(total_days):
    problem += pulp.lpSum(is_work[n, i] for i in range(1, total_number + 1)) >= num_required[n]

# Constraints for work-rest cycle
for i in range(1, total_number + 1):
    for n in range(total_days):
        if n - n_working_days >= 0:
            problem += is_work[n, i] + pulp.lpSum(is_work[n - j, i] for j in range(1, n_working_days + 1)) <= 1
        if n + n_resting_days < total_days:
            problem += is_work[n, i] + pulp.lpSum(is_work[n + j, i] for j in range(1, n_resting_days + 1)) <= 1

# Solve the problem
problem.solve()

# Prepare output
output = {
    "total_number": int(pulp.value(total_number)),
    "is_work": [[int(is_work[n, i].varValue) for n in range(total_days)] for i in range(1, int(pulp.value(total_number)) + 1)]
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')