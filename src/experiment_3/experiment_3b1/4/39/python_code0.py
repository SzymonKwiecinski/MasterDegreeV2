import pulp
import json

# Data input
data = json.loads("{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}")
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts('is_work', (range(1, N + 1), range(1, 100)), cat='Binary')

# Problem definition
problem = pulp.LpProblem("Cafeteria Staffing Problem", pulp.LpMinimize)

# Objective Function
problem += total_number

# Constraints
# Each day's staffing requirement must be satisfied
for n in range(1, N + 1):
    problem += pulp.lpSum(is_work[n][i] for i in range(1, 100)) >= num_n[n-1]

# Employees' work and rest period constraints
for i in range(1, 100):
    for n in range(1, N - n_working_days + 1):
        # Working days constraint
        problem += pulp.lpSum(is_work[n + k][i] for k in range(n_working_days)) == n_working_days
        # Resting days constraint
        problem += pulp.lpSum(is_work[n + n_working_days + k][i] for k in range(n_resting_days)) == 0

# Total number of employees used must equal total_number
for i in range(1, 100):
    problem += pulp.lpSum(is_work[n][i] for n in range(1, N + 1)) <= total_number

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')