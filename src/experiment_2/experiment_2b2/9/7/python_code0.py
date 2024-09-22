import pulp

# Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Unpack data
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Problem definition
problem = pulp.LpProblem("Rocket Optimization", pulp.LpMinimize)

# Define Variables
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None, upBound=None, cat="Continuous")
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None, upBound=None, cat="Continuous")
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, upBound=None, cat="Continuous")
max_thrust = pulp.LpVariable("max_thrust", lowBound=0, upBound=None, cat="Continuous")

# Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Constraints for rocket position and velocity dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Constraint_{t}")

# Final conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Objective: Minimize the maximum thrust
problem += max_thrust, "Objective_Function"

# Constraints for maximum thrust as absolute value of acceleration
for t in range(T):
    problem += a[t] <= max_thrust
    problem += -a[t] <= max_thrust

# Solve the problem
problem.solve()

# Gather the results
x_values = [x[t].varValue for t in range(1, T+1)]
v_values = [v[t].varValue for t in range(1, T+1)]
a_values = [a[t].varValue for t in range(T)]
fuel_spent = sum([abs(a[t].varValue) for t in range(T)])

output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')