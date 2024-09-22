import pulp
import json

# Data
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)

# Create the problem
problem = pulp.LpProblem("CafeteriaStaffingProblem", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=1, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(int(total_number))), cat='Binary')

# Objective Function
problem += total_number, "Minimize Total Employees"

# Constraints for required number of employees
for n in range(N):
    problem += pulp.lpSum(is_work[n, i] for i in range(int(total_number))) >= num_n[n], f"MinEmployees_day_{n}"

# Constraints for working and resting days for each employee
for i in range(int(total_number)):
    for n in range(N - n_working - n_resting + 1):
        # Working days
        for j in range(n_working):
            problem += is_work[n + j, i] == 1, f"Work_days_{i}_from_day_{n + j}"
        # Resting days
        for j in range(n_resting):
            problem += is_work[n + n_working + j, i] == 0, f"Rest_days_{i}_after_work_{n + j + n_working}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')