import pulp

# Data input
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']
M = 10  # Maximum allowable thrust

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Variables for position, velocity, and acceleration
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=-M, upBound=M) for t in range(T)]

# Objective function: Minimize the maximum thrust required |a_t|
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

# Constraints
problem += x[0] == x0  # Initial position
problem += v[0] == v0  # Initial velocity
problem += x[T] == xT  # Final position
problem += v[T] == vT  # Final velocity

for t in range(T - 1):
    problem += x[t + 1] == x[t] + v[t]  # Position update
    problem += v[t + 1] == v[t] + a[t]  # Velocity update

# Constraints for thrust
for t in range(T):
    problem += a[t] <= max_thrust
    problem += -a[t] <= max_thrust

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')