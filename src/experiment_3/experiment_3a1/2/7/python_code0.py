import pulp

# Data from the provided JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']
M = 10  # Define a maximum thrust limit

# Define the problem
problem = pulp.LpProblem("Rocket_Trajectory_Control", pulp.LpMinimize)

# Define decision variables
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=-M, upBound=M) for t in range(T)]

# Objective function: Minimize the maximum thrust (acceleration)
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

# Constraints
problem += x[0] == x0  # Initial position
problem += v[0] == v0  # Initial velocity

for t in range(T):
    problem += x[t + 1] == x[t] + v[t]  # Position constraint
    problem += v[t + 1] == v[t] + a[t]  # Velocity constraint

problem += x[T] == xT  # Final position constraint
problem += v[T] == vT  # Final velocity constraint

# Maximum thrust constraints
for t in range(T):
    problem += max_thrust >= a[t]  # Ensures max_thrust is at least a[t]
    problem += max_thrust >= -a[t]  # Ensures max_thrust is at least -a[t]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')