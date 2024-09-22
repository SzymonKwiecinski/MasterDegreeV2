import pulp
import json

# Given data
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Number of days
N = len(num)

# Create the problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable("Total_Employees", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(1, N+1), range(1, 100)), cat='Binary')  # Assuming a maximum of 100 employees for initialization

# Objective function
problem += x, "Minimize_Total_Employees"

# Constraints
# Each day's staffing requirement must be met
for n in range(1, N + 1):
    problem += pulp.lpSum(is_work[n][i] for i in range(1, 100)) >= num[n - 1], f"Staffing_Requirement_Day_{n}"

# Each employee's working and resting days schedule must be consistent
for i in range(1, 100):
    for k in range(1, N + 1 - n_working_days):
        problem += pulp.lpSum(is_work[n][i] for n in range(k, k + n_working_days)) == n_working_days, f"Work_Consistency_Employee_{i}_Start_{k}"
        problem += is_work[k + n_working_days][i] == 0, f"Rest_Employee_{i}_After_Start_{k}"

# The number of employees hired must match the binary variables
for i in range(1, 100):
    problem += pulp.lpSum(is_work[n][i] for n in range(1, N + 1)) <= n_working_days + n_resting_days, f"Max_Work_Rest_Employee_{i}"

problem += x == pulp.lpSum(1 for i in range(1, 100) if pulp.lpSum(is_work[n][i] for n in range(1, N + 1)) > 0), "Total_Employees_Constraint"

# Solve the problem
problem.solve()

# Output the results
total_number = pulp.value(x)
is_work_schedule = {i: [pulp.value(is_work[n][i]) for n in range(1, N + 1)] for i in range(1, 100) if pulp.value(is_work[1][i]) is not None}

print(f' (Objective Value): <OBJ>{total_number}</OBJ>')
print(f' (Work Schedule): {is_work_schedule}')