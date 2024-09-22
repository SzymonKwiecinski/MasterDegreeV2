import pulp
import json

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Variables
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # No acceleration at time T

# Objective function
problem += pulp.lpSum([pulp.lpSum(a[t] for t in range(T))]), "TotalFuelSpent"

# Constraints
problem += (x[0] == x_0, "InitialPosition")  # Initial position
problem += (v[0] == v_0, "InitialVelocity")  # Initial velocity

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionAtTime{t+1}")  # Position update
    problem += (v[t + 1] == v[t] + a[t], f"VelocityAtTime{t+1}")  # Velocity update

# Final conditions
problem += (x[T] == x_T, "FinalPosition")  # Final position
problem += (v[T] == v_T, "FinalVelocity")  # Final velocity

# Solve the problem
problem.solve()

# Collect results
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]

fuel_spent = pulp.value(problem.objective)

# Prepare output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Print results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')