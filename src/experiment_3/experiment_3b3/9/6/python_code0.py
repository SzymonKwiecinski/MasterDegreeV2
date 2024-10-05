import pulp

# Problem setup
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Input data
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(data['TotalTime'] + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(data['TotalTime'] + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(data['TotalTime'])]

# Objective Function
problem += pulp.lpSum(pulp.lpSum([pulp.lpSum([a[t] for t in range(data['TotalTime'])])] for t in range(data['TotalTime']))), "TotalFuelSpend"

# Constraints
problem += (x[0] == data['InitialPosition'], "InitialPosition")
problem += (v[0] == data['InitialVelocity'], "InitialVelocity")
problem += (x[data['TotalTime']] == data['FinalPosition'], "FinalPosition")
problem += (v[data['TotalTime']] == data['FinalVelocity'], "FinalVelocity")

for t in range(data['TotalTime']):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

# Solve the problem
problem.solve()

# Output results
result = {
    "x": [pulp.value(x[i]) for i in range(1, data['TotalTime'] + 1)],
    "v": [pulp.value(v[i]) for i in range(1, data['TotalTime'] + 1)],
    "a": [pulp.value(a[i]) for i in range(data['TotalTime'])],
    "fuel_spend": pulp.value(problem.objective),
}

print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')