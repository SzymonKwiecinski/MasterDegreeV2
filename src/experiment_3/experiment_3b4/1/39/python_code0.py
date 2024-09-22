import pulp

# Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_demand = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Parameters
N = len(num_demand)
M = sum(num_demand)  # an upper bound on the number of employees

# Create the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(M), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, i) for n in range(N) for i in range(M)), cat='Binary')
z = pulp.LpVariable.dicts("z", ((n, i) for n in range(N) for i in range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(x[i] for i in range(M))

# Constraints

# 1. Demand satisfaction
for n in range(N):
    problem += pulp.lpSum(y[n, i] for i in range(M)) >= num_demand[n]

# 2. Working and resting cycle
for n in range(N):
    for i in range(M):
        problem += y[n, i] <= x[i]
        
        # Consistent working days for working cycle
        if n <= N - n_working_days:
            problem += pulp.lpSum(y[n+k, i] for k in range(n_working_days)) == n_working_days * z[n, i]
        
        # Consistent resting days for resting cycle
        if n <= N - (n_working_days + n_resting_days):
            problem += pulp.lpSum(1 - y[n_working_days+n+k, i] for k in range(n_resting_days)) == n_resting_days * (1 - z[n, i])

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')