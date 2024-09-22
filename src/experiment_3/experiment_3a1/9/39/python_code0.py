import pulp
import json

# Data from the provided JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
N = len(data['num'])  # total number of days
num_n = data['num']  # required number of employees on each day
n_working = data['n_working_days']  # number of consecutive working days
n_resting = data['n_resting_days']  # number of consecutive resting days

# Create the LP problem
problem = pulp.LpProblem("Cafeteria Staffing Problem", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # assuming maximum of 100 employees

# Objective function
problem += total_number, "Minimize total number of employees"

# Constraints for the number of employees working each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n], f"Day_{n+1}_requirement"

# Working and resting schedule for each employee
for i in range(100):
    for k in range(N):
        if k + n_working <= N:
            # Working days
            problem += pulp.lpSum(is_work[n][i] for n in range(k, k + n_working)) == n_working, f"Employee_{i}_work_days_from_{k+1}"
        if k + n_working + n_resting <= N:
            # Resting days
            problem += pulp.lpSum(is_work[n][i] for n in range(k + n_working, k + n_working + n_resting)) == 0, f"Employee_{i}_rest_days_from_{k+1}"

# Additional constraint to ensure total_number is equal to the number of employees used
for i in range(100):
    problem += pulp.lpSum(is_work[n][i] for n in range(N)) <= total_number, f"Employee_{i}_usage"

# Solve the problem
problem.solve()

# Output results
solution = {
    "total_number": pulp.value(total_number),
    "is_work": [[int(is_work[n][i].varValue) for n in range(N)] for i in range(100)]
}

print(json.dumps(solution))

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')