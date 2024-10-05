import pulp

# Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
N = len(data['num'])  # Number of days
M = 20  # Maximum number of employees considered
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', cat='Binary') for i in range(M)]
is_work = [[pulp.LpVariable(f'is_work_{n}_{i}', cat='Binary') for i in range(M)] for n in range(N)]

# Objective function
problem += pulp.lpSum(x)

# Constraints
# Staffing requirements
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(M)) >= data['num'][n]

# Employee working schedule constraints
for i in range(M):
    for n in range(N):
        # Employee working constraint
        problem += is_work[n][i] <= x[i]
        
        # Consecutive working days and resting days constraints
        if n + n_working_days <= N:
            problem += pulp.lpSum(is_work[n+k][i] for k in range(n_working_days)) <= n_working_days * x[i]
        if n + n_working_days + n_resting_days <= N:
            problem += pulp.lpSum(is_work[n+n_working_days+k][i] for k in range(n_resting_days)) == 0

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')