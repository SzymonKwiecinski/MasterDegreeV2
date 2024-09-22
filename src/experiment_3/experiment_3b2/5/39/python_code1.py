import pulp
import json

# Input data
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

I = len(num)  # Number of variables
N = len(num)  # Number of constraints

# Create the problem
problem = pulp.LpProblem("Minimize_X", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(I), cat='Binary')
y = pulp.LpVariable.dicts("y", (range(I), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(x[i] for i in range(I))

# Constraints
for n in range(N):
    problem += pulp.lpSum(y[i, n] for i in range(I)) >= num[n]

for i in range(I):
    for n in range(N):
        problem += y[i, n] <= x[i]

for i in range(I):
    for n in range(N - (n_working_days + n_resting_days)):
        problem += y[i, n] == y[i, n + n_working_days + n_resting_days]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')