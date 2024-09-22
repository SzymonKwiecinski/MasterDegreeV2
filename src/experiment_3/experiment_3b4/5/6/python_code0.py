import pulp

# Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Model setup
problem = pulp.LpProblem("Rocket_Path_Optimization", pulp.LpMinimize)

# Parameters
T = data['TotalTime']

# Variables
x = pulp.LpVariable.dicts('x', range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts('v', range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts('a', range(T), cat='Continuous')
abs_a = pulp.LpVariable.dicts('abs_a', range(T), lowBound=0, cat='Continuous')

# Objective: Minimize the total fuel spent (sum of absolute accelerations)
problem += pulp.lpSum(abs_a[t] for t in range(T))

# Constraints

# Dynamics of the rocket
for t in range(T):
    problem += x[t+1] == x[t] + v[t], f"Dynamics_position_{t}"
    problem += v[t+1] == v[t] + a[t], f"Dynamics_velocity_{t}"

# Initial conditions
problem += x[0] == data['InitialPosition'], "Initial_position"
problem += v[0] == data['InitialVelocity'], "Initial_velocity"

# Final conditions
problem += x[T] == data['FinalPosition'], "Final_position"
problem += v[T] == data['FinalVelocity'], "Final_velocity"

# Absolute value constraints for acceleration
for t in range(T):
    problem += abs_a[t] >= a[t], f"Abs_acceleration_pos_{t}"
    problem += abs_a[t] >= -a[t], f"Abs_acceleration_neg_{t}"

# Solve the problem
problem.solve()

# Print the objective value
objective_value = pulp.value(problem.objective)
print(f'<OBJ>{objective_value}</OBJ>')