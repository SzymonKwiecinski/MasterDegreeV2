import pulp

# Given data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Define the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Variables
T = data['T']
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity
a = pulp.LpVariable.dicts("a", range(T + 1), lowBound=None)  # acceleration

# Initial conditions
problem += (x[0] == data['X0'], "Initial_Position")
problem += (v[0] == data['V0'], "Initial_Velocity")

# Target conditions
problem += (x[T] == data['XT'], "Target_Position")
problem += (v[T] == data['VT'], "Target_Velocity")

# Discrete-time model constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

# Objective function: Minimize max acceleration
max_acceleration = pulp.LpVariable("max_a", lowBound=0)
for t in range(T + 1):
    problem += (a[t] <= max_acceleration, f"Max_Acceleration_Constraint_{t}")
    problem += (a[t] >= -max_acceleration, f"Min_Acceleration_Constraint_{t}")

problem += max_acceleration, "Minimize_Max_Acceleration"

# Solve the problem
problem.solve()

# Collect the output
output = {
    "x": [x[t].varValue for t in range(T + 1)],
    "v": [v[t].varValue for t in range(T + 1)],
    "a": [a[t].varValue for t in range(T + 1)],
    "fuel_spend": sum(abs(a[t].varValue) for t in range(T + 1))
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')