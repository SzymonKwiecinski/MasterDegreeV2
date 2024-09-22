import pulp

# Data from the provided JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)  # Total number of days

# Define the problem
problem = pulp.LpProblem("Cafeteria_Staffing_Optimization", pulp.LpMinimize)

# Define variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(1, total_number.name+1)), cat='Binary')

# Objective Function
problem += total_number

# Constraints for each day
for n in range(N):
    problem += pulp.lpSum([is_work[n][i] for i in range(1, total_number.name+1)]) >= num_n[n]

# Constraints for working and resting days
for i in range(1, total_number.name+1):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum([is_work[n + j][i] for j in range(n_working_days)]) == n_working_days

    for n in range(N - n_working_days):
        for rest in range(1, n_resting_days + 1):
            problem += is_work[n + n_working_days + rest][i] == 0

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')