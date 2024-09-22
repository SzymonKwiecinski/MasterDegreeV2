import pulp

# Given data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Max_Thrust", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position variables
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity variables

# Objective Function: Minimize the maximum thrust required
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

# Constraints
problem += (x[0] == X0, "Initial_Position_Constraint")
problem += (v[0] == V0, "Initial_Velocity_Constraint")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")
    problem += (a[t] <= max_thrust, f"Max_Thrust_Upper_{t}")  # a_t <= max_thrust
    problem += (a[t] >= -max_thrust, f"Max_Thrust_Lower_{t}")  # a_t >= -max_thrust

# Last position and velocity constraints
problem += (x[T] == XT, "Target_Position_Constraint")
problem += (v[T] == VT, "Target_Velocity_Constraint")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')