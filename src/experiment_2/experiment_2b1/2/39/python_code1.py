import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Variables
total_number = pulp.LpVariable("total_number", lowBound=1, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # Large upper limit for employees

# Objective function
problem += total_number, "Minimize Employees"

# Constraints
for day in range(N):
    problem += pulp.lpSum(is_work[day][i] for i in range(100)) >= num[day], f"Staffing_Requirement_{day}"

for i in range(100):  # Considering a maximum of 100 employees for constraints
    for day in range(N):
        for j in range(n_working_days):
            if day + j < N:
                problem += is_work[day][i] <= pulp.lpSum(is_work[day+j][k] for k in range(100)), f"Shift_Assignment_{day}_{j}_{i}"

# Solve the problem
problem.solve()

# Prepare the output
is_work_output = [[int(is_work[n][i].value()) for n in range(N)] for i in range(total_number.value())]
total_number_value = total_number.value()

# Resulting output
output = {
    "total_number": total_number_value,
    "is_work": is_work_output
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')