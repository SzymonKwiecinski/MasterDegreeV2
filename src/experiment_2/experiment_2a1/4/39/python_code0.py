import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create a linear programming problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # 100 is an arbitrary upper guess for employees

# Objective function: minimize the number of employees
problem += total_number

# Constraints to ensure sufficient staff is available on each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num[n]  # ensure enough staff on each day
    for d in range(n_working_days):
        if n + d < N:  # ensure we do not go out of bounds
            for i in range(total_number):
                problem += is_work[n + d][i] <= 1  # each employee can only work 1 shift

# Constraints for working/resting schedule
for i in range(100):
    for n in range(N):
        for w in range(n_working_days):
            if n + w < N:
                problem += is_work[n + w][i] <= total_number  # link employees to total number
        
        for r in range(n_resting_days):
            if n + n_working_days + r < N:
                problem += is_work[n + n_working_days + r][i] == 0  # resting days

# Solve the problem
problem.solve()

# Extracting results
total_employees = int(pulp.value(total_number))
work_schedule = [[int(pulp.value(is_work[n][i])) for n in range(N)] for i in range(total_employees)]

# Output
result = {
    'total_number': total_employees,
    'is_work': work_schedule
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')