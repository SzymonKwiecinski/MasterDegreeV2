import pulp

# Data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

# Parameters
N = len(data['num'])
n_working = data['n_working_days']
n_resting = data['n_resting_days']

# Problem
problem = pulp.LpProblem("Cafeteria Staffing Problem", pulp.LpMinimize)

# Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(N*max(data['num']))), cat='Binary')

# Objective Function
problem += total_number

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n, i] for i in range(N*max(data['num']))) >= data['num'][n]

# Work and Rest Schedule Constraint
for i in range(N*max(data['num'])):
    for n in range(N - n_working):
        problem += pulp.lpSum(is_work[j, i] for j in range(n, n + n_working)) == n_working
    for n in range(N - n_working - n_resting):
        problem += pulp.lpSum(is_work[j, i] for j in range(n + n_working, n + n_working + n_resting)) == 0

# Total number constraint
for i in range(N*max(data['num'])):
    problem += pulp.lpSum(is_work[n, i] for n in range(N)) <= total_number

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')