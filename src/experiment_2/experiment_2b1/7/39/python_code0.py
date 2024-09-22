import pulp
import json

# Given data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

N = len(num)

# Create the problem variable
problem = pulp.LpProblem("Cafeteria Staffing Problem", pulp.LpMinimize)

# Define the total number of employees
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

# Create a binary variable for each employee's work schedule
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(int(total_number))), cat='Binary')

# Add constraints for each day
for day in range(N):
    # The total number of employees working on day 'day'
    problem += (pulp.lpSum(is_work[day][i] for i in range(int(total_number))) >= num[day]), f"Staffing_Constraint_day_{day}")

# Add constraints for each employee's working and resting schedule
for i in range(int(total_number)):
    for day in range(N):
        # Ensure that if an employee is working on a day, they follow their work/rest schedule
        problem += (is_work[day][i] <= pulp.lpSum(is_work[day2][i] for day2 in range(day - n_working_days + 1, day + 1) if day2 >= 0) + \
                                                    pulp.lpSum(is_work[day2][i] for day2 in range(day + n_working_days, day + n_working_days + n_resting_days) if day2 < N)), f"Resting_days_Employee_{i}_on_day_{day}"

# Objective function: Minimize the number of employees
problem += total_number

# Solve the problem
problem.solve()

# Extract the results
total_number_value = pulp.value(total_number)
is_work_schedule = [[int(is_work[n][i].value()) for n in range(N)] for i in range(int(total_number_value))]

# Output the results
output_result = {
    "total_number": total_number_value,
    "is_work": is_work_schedule
}

print(output_result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')