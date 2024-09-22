import pulp

# Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Problem
problem = pulp.LpProblem("Staff_Scheduling", pulp.LpMinimize)

# Variables
T = 100  # Assumed large number of potential employees to cover all days requirement
x = pulp.LpVariable.dicts("x", range(T), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, i) for n in range(N) for i in range(T)), cat='Binary')

# Objective
problem += pulp.lpSum(x[i] for i in range(T))

# Constraints
for n in range(N):
    problem += pulp.lpSum(y[n, i] for i in range(T)) >= num[n]

for i in range(T):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(y[n+k, i] for k in range(n_working_days)) <= n_working_days * x[i]

for i in range(T):
    for n in range(N):
        if (n % (n_working_days + n_resting_days)) >= n_working_days:
            problem += y[n, i] == 0

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')