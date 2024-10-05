import pulp

# Given data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Initialize the problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

# Auxiliary variable for maximum thrust
z = pulp.LpVariable('z', lowBound=0)

# Objective
problem += z, "Minimize maximum thrust"

# Constraints
# Initial conditions
problem += (x[0] == x0), "Initial_Position"
problem += (v[0] == v0), "Initial_Velocity"

# Dynamics equations
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"Position_Update_Time_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"Velocity_Update_Time_{t}"

# Final conditions
problem += (x[T] == xT), "Final_Position"
problem += (v[T] == vT), "Final_Velocity"

# Maximum thrust constraints
for t in range(T):
    problem += (z >= a[t]), f"Max_Thrust_Positive_Time_{t}"
    problem += (z >= -a[t]), f"Max_Thrust_Negative_Time_{t}"

# Solve the problem
problem.solve()

# Print the value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')