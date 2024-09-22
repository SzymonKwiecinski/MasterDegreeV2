import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the linear programming problem
problem = pulp.LpProblem("CafeteriaStaffing", pulp.LpMinimize)

# Define decision variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # Assume a maximum of 100 employees for the formulation

# Objective function: Minimize total_number of employees
problem += total_number

# Constraints: Ensure that the number of working employees meets the requirement on each day
for day in range(N):
    problem += pulp.lpSum(is_work[day][i] for i in range(total_number)) >= num[day]

# Additional constraints for working/resting schedule
for i in range(100):  # For each potential employee
    for day in range(N):
        if day >= n_working_days:
            problem += pulp.lpSum(is_work[(day - j) % N][i] for j in range(n_working_days)) == n_working_days * is_work[day][i]
        if day < n_working_days:
            problem += pulp.lpSum(is_work[(day - j) % N][i] for j in range(day + 1)) <= (day + 1) * is_work[day][i]

# Solve the problem
problem.solve()

# Extract the results
total_employees = int(pulp.value(total_number))
work_schedule = [[int(pulp.value(is_work[n][i])) for n in range(N)] for i in range(total_employees)]

# Prepare output
output = {
    "total_number": total_employees,
    "is_work": work_schedule
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')