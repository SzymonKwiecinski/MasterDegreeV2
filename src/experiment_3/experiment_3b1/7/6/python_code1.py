import pulp

# Data input
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Parameters
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create the Linear Programming problem
problem = pulp.LpProblem("RocketTrajectory", pulp.LpMinimize)

# Decision Variables
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]  # Acceleration variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]  # Position variables
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]  # Velocity variables

# Objective Function: Minimize the sum of the absolute values of the accelerations
problem += pulp.lpSum([pulp.lpVar('abs_a_' + str(t), lowBound=0) for t in range(T)])

# Constraints
problem += (x[0] == x0)  # Initial position constraint
problem += (v[0] == v0)  # Initial velocity constraint

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])  # Position update
    problem += (v[t + 1] == v[t] + a[t])  # Velocity update

problem += (x[T] == xT)  # Final position constraint
problem += (v[T] == vT)  # Final velocity constraint

# Solve the problem
problem.solve()

# Output results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
total_fuel = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_fuel}</OBJ>')