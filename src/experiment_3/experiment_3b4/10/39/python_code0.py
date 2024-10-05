import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Constants
N = len(num)
M = sum(num)  # Upper bound on the total number of employees

# Problem
problem = pulp.LpProblem("Minimize_Hiring", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(M), cat='Binary')
is_work = pulp.LpVariable.dicts("is_work", [(n, i) for n in range(N) for i in range(M)], cat='Binary')

# Objective
problem += pulp.lpSum(x[i] for i in range(M)), "Minimize total employees"

# Constraints
# 1. Demand Satisfaction
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(M)) >= num[n], f"Demand_satisfaction_{n}"

# 2. Work and Rest Cycle
for i in range(M):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(is_work[(n + k, i)] for k in range(n_working_days)) <= n_working_days * x[i], f"Work_cycle_{n}_{i}"

    for n in range(n_working_days, N):
        if n + n_resting_days <= N:
            problem += is_work[(n, i)] == 0, f"Rest_{n}_{i}"

# 3. Binary Constraints (implicitly declared in variable definition)

# Solve the problem
problem.solve()

# Output the result
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')