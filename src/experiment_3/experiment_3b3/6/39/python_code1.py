import pulp

# Define the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(int(total_number.name))), cat='Binary')

# Objective
problem += total_number

# Constraints
# Constraint 1: Meet required number of employees each day
for n in range(N):
    problem += pulp.lpSum(is_work[n, i] for i in range(int(total_number.name))) >= num[n]

# Constraint 2: Consecutive working and resting days
for i in range(int(total_number.name)):
    for k in range(N - n_working_days + 1):
        # Working days constraint
        problem += pulp.lpSum(is_work[k + j, i] for j in range(n_working_days)) == n_working_days
    for k in range(N - n_working_days - n_resting_days + 1):
        # Resting days constraint
        problem += pulp.lpSum(is_work[k + n_working_days + j, i] for j in range(n_resting_days)) == 0

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')