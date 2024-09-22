import pulp

# Data from the JSON input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
total_days = len(num)

# Initialize the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Decision variables
x = {i: pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(total_days)}
y = {(i, n): pulp.LpVariable(f"y_{i}_{n}", cat='Binary') for i in range(total_days) for n in range(total_days)}

# Objective function
problem += pulp.lpSum(x[i] for i in range(total_days))

# Demand constraints
for n in range(total_days):
    problem += pulp.lpSum(y[i, n] for i in range(total_days)) >= num[n]

# Work-rest schedule constraints
for i in range(total_days):
    for n in range(total_days):
        if n % (n_working_days + n_resting_days) < n_working_days:
            problem += y[i, n] <= x[i]
        else:
            problem += y[i, n] == 0

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')