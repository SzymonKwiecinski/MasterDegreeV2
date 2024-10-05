import pulp

# Data input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Parameters
N = len(num)  # Number of tasks
I = N  # Assuming each task corresponds to a decision variable x_i

# Problem setup
problem = pulp.LpProblem("Minimize_X", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(I), cat='Binary')
y = pulp.LpVariable.dicts("y", (range(N), range(I)), cat='Binary')

# Objective Function
problem += pulp.lpSum(x[i] for i in range(I)), "Minimize_Total_X"

# Constraints
for n in range(N):
    problem += pulp.lpSum(y[n][i] for i in range(I)) >= num[n], f"Sum_Y_Constraint_{n}"

for i in range(I):
    for n in range(N):
        problem += (pulp.lpSum(y[n + k][i] for k in range(n_working_days)) 
                     <= n_working_days * x[i], 
                     f"Working_Days_Constraint_{n}_{i}")

for i in range(I):
    for n in range(N):
        if n + n_working_days < N:
            problem += y[n + n_working_days][i] == 0, f"Resting_Days_Zero_{n}_{i}"

for n in range(N):
    for i in range(I):
        problem += y[n][i] <= x[i], f"Y_Less_Equal_X_{n}_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')