import pulp
import json

# Given data in JSON format
data = json.loads("{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}")

# Extracting data
num_required = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_required)

# Problem definition
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision variable
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), cat='Binary')

# Objective function
problem += total_number, "Minimize_Total_Employees"

# Constraints for required employees on each day
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number)) >= num_required[n], f"Min_Employees_Day_{n+1}"

# Constraints for working days
for i in range(total_number):
    for n in range(N - n_working + 1):
        problem += pulp.lpSum(is_work[(n + d, i)] for d in range(n_working)) <= n_working, f"Working_Days_Limit_{i}_{n+1}"

    # Constraints for resting days
    for n in range(N - n_working - n_resting + 1):
        problem += pulp.lpSum(is_work[(n + d + n_working, i)] for d in range(n_resting)) == 0, f"Resting_Days_Requirement_{i}_{n+1}"

# Add a constraint to link total_number with the total hired employees
problem += total_number >= pulp.lpSum(1 for i in range(total_number) if pulp.lpSum(is_work[(n, i)] for n in range(N)) > 0), "Total_Number_Constraint"

# Solve the problem
problem.solve()

# Output results
hired_employees = pulp.value(total_number)
print(f' (Objective Value): <OBJ>{hired_employees}</OBJ>')

is_work_matrix = [[pulp.value(is_work[(n, i)]) for i in range(int(hired_employees))] for n in range(N)]
print("Work Schedule (is_work matrix):")
for row in is_work_matrix:
    print(row)