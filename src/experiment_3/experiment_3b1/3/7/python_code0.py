import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the optimization problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # Acceleration (thrust)
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocity
M = pulp.LpVariable("M", lowBound=0)  # Maximum thrust (objective)

# Objective Function: Minimize M
problem += M

# Initial conditions
x[0] = x0
v[0] = v0

# Constraints for position and velocity updates
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"

# Final conditions
problem += x[T] == xT, "Final_Position_Constraint"
problem += v[T] == vT, "Final_Velocity_Constraint"

# Max thrust constraints
for t in range(T):
    problem += a[t] <= M, f"Max_Thrust_Upper_{t}"  # a_t <= M
    problem += a[t] >= -M, f"Max_Thrust_Lower_{t}"  # a_t >= -M

# Solve the problem
problem.solve()

# Extracting results
x_values = [pulp.value(x[i]) for i in range(T + 1)]
v_values = [pulp.value(v[i]) for i in range(T + 1)]
a_values = [pulp.value(a[i]) for i in range(T)]
total_fuel_spent = sum(abs(a[i]) for i in range(T))  # Assuming fuel is spent proportional to |a|

# Output results
result = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": total_fuel_spent
}

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')