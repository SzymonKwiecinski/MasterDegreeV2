import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable('total_number', lowBound=1, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(1, total_number+1)), cat='Binary')

# Objective function: Minimize the number of employees
problem += total_number

# Constraints: Ensure enough staff on each day
for day in range(N):
    problem += pulp.lpSum(is_work[day][i] for i in range(1, total_number+1) if i <= total_number) >= num[day]

# Each employee works n_working_days and rests n_resting_days
for i in range(1, total_number + 1):
    for day in range(N):
        for j in range(n_working_days):
            if day + j < N:
                problem += is_work[day + j][i] <= 1  # They cannot work on overlapping days
        for j in range(n_resting_days):
            if day + n_working_days + j < N:
                problem += is_work[day + n_working_days + j][i] == 0  # They must rest after working days

# Solve the problem
problem.solve()

# Prepare output
total_employees = int(pulp.value(total_number))
work_schedule = [[int(pulp.value(is_work[day][i])) for day in range(N)] for i in range(1, total_employees + 1)]

# Print output in required format
output = {
    "total_number": total_employees,
    "is_work": work_schedule
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')