import pulp

# Problem data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Initialize the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(data['T'] + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(data['T'] + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(data['T']), cat='Continuous')
max_thrust = pulp.LpVariable("Max_Thrust", lowBound=0, cat='Continuous')

# Objective function
problem += max_thrust, "Minimize_Max_Thrust"

# Add constraints
problem += (x[0] == data['X0'], "Initial_Position")
problem += (v[0] == data['V0'], "Initial_Velocity")

# Equation constraints
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")
    problem += (-max_thrust <= a[t], f"Negative_Acceleration_Bound_{t}")
    problem += (a[t] <= max_thrust, f"Positive_Acceleration_Bound_{t}")

# Final position and velocity constraints
problem += (x[data['T']] == data['XT'], "Final_Position")
problem += (v[data['T']] == data['VT'], "Final_Velocity")

# Solve the problem
problem.solve()

# Prepare the output
x_result = [x[i].varValue for i in range(data['T'] + 1)]
v_result = [v[i].varValue for i in range(data['T'] + 1)]
a_result = [a[i].varValue for i in range(data['T'])]
fuel_spend = sum(abs(a[i].varValue) for i in range(data['T']))

output = {
    "x": x_result,
    "v": v_result,
    "a": a_result,
    "fuel_spend": fuel_spend
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')