import pulp

# Parse the input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0, v_0, x_T, v_T, T = data['InitialPosition'], data['InitialVelocity'], data['FinalPosition'], data['FinalVelocity'], data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("RocketControl", pulp.LpMinimize)

# Define the decision variables
x = [pulp.LpVariable(f"x_{t}", cat="Continuous") for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat="Continuous") for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat="Continuous") for t in range(T)]

abs_a = [pulp.LpVariable(f"abs_a_{t}", lowBound=0, cat="Continuous") for t in range(T)]

# Set the objective function: Minimize total absolute fuel consumption
problem += pulp.lpSum(abs_a)

# Add constraints
# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Dynamic model constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])
    problem += abs_a[t] >= a[t]
    problem += abs_a[t] >= -a[t]

# Solve the LP problem
problem.solve()

# Retrieve the results
positions = [pulp.value(x_i) for x_i in x]
velocities = [pulp.value(v_i) for v_i in v]
accelerations = [pulp.value(a_i) for a_i in a]
fuel_spent = sum(abs(pulp.value(a_i)) for a_i in a)

# Print results in the required output format
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')