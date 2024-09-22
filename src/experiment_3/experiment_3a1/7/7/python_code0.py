import pulp
import json

# Data from JSON
data = json.loads('{"X0": 0, "V0": 0, "XT": 1, "VT": 0, "T": 20}')
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective Function: Minimize maximum acceleration
max_a = pulp.LpVariable("max_a", lowBound=0)
problem += max_a

# Dynamic Equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"

# Initial Conditions
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

# Final Conditions
problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

# Constraints for the maximum thrust
for t in range(T):
    problem += a[t] <= max_a, f"Max_Thrust_Upper_{t}"
    problem += a[t] >= -max_a, f"Max_Thrust_Lower_{t}"

# Solve the problem
problem.solve()

# Output the results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

print(f"x: {x_values}")
print(f"v: {v_values}")
print(f"a: {a_values}")
print(f"fuel_spent: {fuel_spent}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')