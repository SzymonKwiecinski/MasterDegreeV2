import pulp

# Define the data from input
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Initialize the problem
problem = pulp.LpProblem("Rocket_Fuel_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T+1), cat=pulp.LpContinuous)
v = pulp.LpVariable.dicts("v", range(T+1), cat=pulp.LpContinuous)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, cat=pulp.LpContinuous)

# Additional decision variables for absolute value of a_t
abs_a = pulp.LpVariable.dicts("abs_a", range(T), lowBound=0, cat=pulp.LpContinuous)

# Objective function: Minimize total fuel spent
problem += pulp.lpSum([abs_a[t] for t in range(T)])

# Constraints
# Initial conditions
problem += x[0] == x_0, "Initial Position"
problem += v[0] == v_0, "Initial Velocity"

# Dynamics equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position Update at time {t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity Update at time {t}"
    # Constraints for absolute value
    problem += abs_a[t] >= a[t], f"Absolute Value Positive at time {t}"
    problem += abs_a[t] >= -a[t], f"Absolute Value Negative at time {t}"

# Final conditions
problem += x[T] == x_T, "Final Position"
problem += v[T] == v_T, "Final Velocity"

# Solve the problem
problem.solve()

# Extract the solution
positions = [x[t].varValue for t in range(T+1)]
velocities = [v[t].varValue for t in range(T+1)]
accelerations = [a[t].varValue for t in range(T)]
fuel_spent = sum(abs_a[t].varValue for t in range(T))

# Output the results
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')