import pulp
import json

# Data input
data = json.loads("{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}")
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)

# Define the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Define the total number of employees variable
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

# Define the binary decision variables
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(total_number.name)), cat='Binary')

# Objective function: Minimize the number of employees
problem += total_number, "Minimize_Total_Employees"

# Constraints to ensure required employees for each day
for n in range(N):
    problem += (pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num_n[n]), f"Employee_Requirement_Day_{n+1}"

# Constraints for working and resting days for each employee
for i in range(total_number):
    # Each employee should not exceed the working limit
    problem += (pulp.lpSum(is_work[n][i] for n in range(N)) <= n_working, f"Max_Work_Days_Employee_{i+1}")

    # Enforce resting days
    for n in range(N - n_working - n_resting):
        for d in range(1, n_resting + 1):
            problem += (is_work[n][i] + is_work[n + d][i] <= 1, f"Rest_Employee_{i+1}_Day_{n+1}_After_Rest_{d}")

# Solve the problem
problem.solve()

# Output the results
total_employees = pulp.value(total_number)
print(f' (Objective Value): <OBJ>{total_employees}</OBJ>')

# Optionally, you can also print the work schedule matrix
schedule_matrix = [[pulp.value(is_work[n][i]) for i in range(total_employees)] for n in range(N)]
print("Schedule Matrix:")
for row in schedule_matrix:
    print(row)