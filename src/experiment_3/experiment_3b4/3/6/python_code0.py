import pulp

# Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Extract data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("RocketPathControl", pulp.LpMinimize)

# Decision variables
x_t = pulp.LpVariable.dicts("x", range(T+1))
v_t = pulp.LpVariable.dicts("v", range(T+1))
a_t = pulp.LpVariable.dicts("a", range(T))
u_t = pulp.LpVariable.dicts("u", range(T), lowBound=0)

# Objective function
problem += pulp.lpSum(u_t[t] for t in range(T)), "TotalFuelConsumption"

# Constraints
problem += (x_t[0] == x_0), "InitialPosition"
problem += (v_t[0] == v_0), "InitialVelocity"
problem += (x_t[T] == x_T), "FinalPosition"
problem += (v_t[T] == v_T), "FinalVelocity"

for t in range(T):
    problem += (x_t[t+1] == x_t[t] + v_t[t]), f"PositionUpdate_{t}"
    problem += (v_t[t+1] == v_t[t] + a_t[t]), f"VelocityUpdate_{t}"
    problem += (u_t[t] >= a_t[t]), f"Auxiliary_1_{t}"
    problem += (u_t[t] >= -a_t[t]), f"Auxiliary_2_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')