import pulp

# Data
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Parameters
T = data['TotalTime'] 
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']

# Problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a_plus = [pulp.LpVariable(f"a^+_{t}", lowBound=0, cat='Continuous') for t in range(T)]
a_minus = [pulp.LpVariable(f"a^-_{t}", lowBound=0, cat='Continuous') for t in range(T)]

# Objective
problem += pulp.lpSum([a_plus[t] + a_minus[t] for t in range(T)])

# Constraints
# Initial conditions
problem += (x[0] == x0, "Initial_Position")
problem += (v[0] == v0, "Initial_Velocity")

# Equations of motion
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Motion_Equation_Position_{t}")
    problem += (v[t+1] == v[t] + a_plus[t] - a_minus[t], f"Motion_Equation_Velocity_{t}")

# Final conditions
problem += (x[T] == xT, "Final_Position")
problem += (v[T] == vT, "Final_Velocity")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')