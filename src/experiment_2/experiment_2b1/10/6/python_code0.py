import pulp
import json

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Parameters
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("Rocket_trajectory", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: Minimize total fuel consumption
problem += pulp.lpSum(pulp.lpAbs(a[t]) for t in range(T)), "TotalFuel"

# Constraints
problem += x[0] == x_0, "InitialPosition"
problem += v[0] == v_0, "InitialVelocity"

for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionUpdate_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityUpdate_{t}"

problem += x[T] == x_T, "FinalPosition"
problem += v[T] == v_T, "FinalVelocity"

# Solve the problem
problem.solve()

# Collect results
result = {
    "x": [x[t].varValue for t in range(T + 1)],
    "v": [v[t].varValue for t in range(T + 1)],
    "a": [a[t].varValue for t in range(T)],
    "fuel_spend": pulp.value(problem.objective),
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')