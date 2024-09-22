import pulp

# Input Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Trajectory_Control", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)      # acceleration
max_a = pulp.LpVariable("max_a", lowBound=0)                 # max acceleration

# Objective Function
problem += max_a, "Minimize_Max_Thrust"

# Constraints
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"
    problem += a[t] <= max_a, f"Max_Thrust_Upper_{t}"
    problem += a[t] >= -max_a, f"Max_Thrust_Lower_{t}"

problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

# Solve the problem
problem.solve()

# Collecting Outputs
x_values = [x[t].varValue for t in range(T + 1)]
v_values = [v[t].varValue for t in range(T + 1)]
a_values = [a[t].varValue for t in range(T)]
fuel_spent = sum(abs(a[t].varValue) for t in range(T))

# Print Results
print(f"x = {x_values}")
print(f"v = {v_values}")
print(f"a = {a_values}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Total fuel spent: {fuel_spent}')