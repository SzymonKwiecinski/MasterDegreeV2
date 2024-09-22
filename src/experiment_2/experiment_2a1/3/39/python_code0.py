import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)
total_days = N

# Define the problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(total_days), range(total_number)), cat='Binary')

# Constraints
for day in range(total_days):
    problem += pulp.lpSum(is_work[day][i] for i in range(total_number) if is_work[day][i] == 1) >= num[day]

# Working days and resting days constraints
for i in range(total_number):
    for day in range(total_days):
        for wd in range(n_working_days):
            if day + wd < total_days:
                problem += is_work[day + wd][i] <= 1  # Cannot work more than one shift in a day
        for rd in range(n_resting_days):
            if day + n_working_days + rd < total_days:
                problem += is_work[day + n_working_days + rd][i] == 0  # Resting days

# Objective function
problem += total_number, "Objective"

# Solve the problem
problem.solve()

# Prepare the output
is_work_output = [[int(is_work[n][i].value()) for n in range(total_days)] for i in range(int(total_number.value()))]

# Print result
output = {
    "total_number": int(total_number.value()),
    "is_work": is_work_output
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')