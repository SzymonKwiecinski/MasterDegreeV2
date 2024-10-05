import pulp

# Read input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Define the LP problem
problem = pulp.LpProblem("RocketProblem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]
thrust_max = pulp.LpVariable('thrust_max', lowBound=0, cat='Continuous')

# Objective: Minimize the max thrust
problem += thrust_max

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Target conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])
    problem += (a[t] <= thrust_max)
    problem += (-a[t] <= thrust_max)

# Solve the problem
problem.solve()

# Extract results
x_values = [x[i].varValue for i in range(1, T + 1)]
v_values = [v[i].varValue for i in range(1, T + 1)]
a_values = [a[i].varValue for i in range(T)]
fuel_spent = sum(abs(a[i].varValue) for i in range(T))

# Output format
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')