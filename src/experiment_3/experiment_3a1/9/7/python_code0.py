import pulp

# Extracting data from the provided JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Defining variables
T = data['T']
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
M = 10  # Assuming a maximum allowable thrust

# Create a linear programming problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

# Defining the variables for positions, velocities, and accelerations
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=-M, upBound=M) for t in range(T)]

# Setting the initial conditions
problem += (x[0] == x0), "InitialPosition"
problem += (v[0] == v0), "InitialVelocity"

# Adding the state update equations as constraints
for t in range(T):
    problem += (x[t + 1] - x[t] - v[t] == 0), f"PositionUpdate_{t}"
    problem += (v[t + 1] - v[t] - a[t] == 0), f"VelocityUpdate_{t}"

# Adding the target conditions
problem += (x[T] == xT), "FinalPosition"
problem += (v[T] == vT), "FinalVelocity"

# Objective function: minimize the maximum thrust (acceleration)
max_thrust = pulp.LpVariable('max_thrust', lowBound=0)
for t in range(T):
    problem += (a[t] <= max_thrust), f"MaxThrustUpper_{t}"
    problem += (-a[t] <= max_thrust), f"MaxThrustLower_{t}"
problem += pulp.lpSum(a[t] for t in range(T))  # Assuming thrust relates to fuel spent

# Solve the problem
problem.solve()

# Extracting the results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]

# Assuming total fuel spent relates to the sum of the absolute values of accelerations
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

# Output the results
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')