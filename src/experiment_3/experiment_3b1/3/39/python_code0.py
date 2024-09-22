import pulp
import json

# Data input
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Problem definition
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # 100 is a safe upper limit for employees

# Objective Function
problem += total_number

# Constraints for number of employees needed each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num[n], f"EmployeeRequirement_day_{n}"

# Constraints for working and resting cycles for each employee
for i in range(100):  # Iterate over possible employees
    for k in range((N // (n_working_days + n_resting_days)) + 1):  # Calculate k for cycles
        for j in range(n_working_days):
            day = k * (n_working_days + n_resting_days) + j
            if day < N:
                problem += is_work[day][i] == 1, f"Work_day_{day}_employee_{i}"
        for j in range(n_working_days, n_working_days + n_resting_days):
            day = k * (n_working_days + n_resting_days) + j
            if day < N:
                problem += is_work[day][i] == 0, f"Rest_day_{day}_employee_{i}"

# Constraint to define the total number of employees based on is_work variables
problem += total_number == pulp.lpSum(is_work[n][i] for n in range(N) for i in range(100)), "TotalEmployees"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')