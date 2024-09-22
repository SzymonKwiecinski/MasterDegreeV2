import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Initialize the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Define the number of employees
max_employees = sum(num)  # An upper bound for the number of employees
employees = pulp.LpVariable.dicts("employee", range(max_employees), 0, 1, pulp.LpBinary)

# Objective function: Minimize the total number of employees
problem += pulp.lpSum(employees[i] for i in range(max_employees)), "Total_Employees"

# Constraints
for day in range(N):
    # Number of employees required on this day
    required = num[day]
    # Sum up the working employees for the required days
    problem += pulp.lpSum(employees[i] for i in range(max_employees) if (i % (n_working_days + n_resting_days)) < n_working_days) >= required, f"Day_{day+1}_Requirement"

# Solve the problem
problem.solve()

# Extract the total number of employees and their work schedules
total_number = int(pulp.value(problem.objective))
is_work = [[0]*N for _ in range(total_number)]

for i in range(total_number):
    for day in range(N):
        if (i % (n_working_days + n_resting_days)) < n_working_days:
            is_work[i][day] = 1

# Prepare the output
output = {
    "total_number": total_number,
    "is_work": is_work
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')