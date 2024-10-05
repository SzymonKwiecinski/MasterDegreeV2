import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable('total_number', lowBound=0, cat='Integer')  # Total number of employees
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(100)), cat='Binary')

# Objective
problem += x

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(100)) >= num[n]

for i in range(100):
    for n in range(N):
        if n < n_working_days:
            problem += is_work[(n, i)] <= is_work[(n, i)]
        else:
            sum_of_previous_periods = pulp.lpSum(is_work[(n-j, i)] for j in range(n_working_days))
            sum_of_resting_period = pulp.lpSum(is_work[(n-j, i)] for j in range(n_working_days, n_working_days + n_resting_days))
            problem += sum_of_previous_periods - sum_of_resting_period >= 0

# Solve
problem.solve()

# Retrieve results
total_number = int(pulp.value(x))
is_work_schedule = [[int(pulp.value(is_work[(n, i)])) for n in range(N)] for i in range(total_number)]

# Output result
result = {
    "total_number": total_number,
    "is_work": is_work_schedule
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
result