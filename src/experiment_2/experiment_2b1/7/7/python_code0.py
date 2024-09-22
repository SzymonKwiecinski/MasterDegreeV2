import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Optimization", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]
max_a = pulp.LpVariable("max_a", lowBound=0)

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Define the dynamics
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])
    problem += (a[t] <= max_a)
    problem += (a[t] >= -max_a)

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Objective function
problem += max_a

# Solve the problem
problem.solve()

# Extract results
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Prepare output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')