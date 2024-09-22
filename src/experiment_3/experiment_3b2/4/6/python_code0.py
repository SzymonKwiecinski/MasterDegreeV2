import pulp
import json

# Data input
data = json.loads('{"InitialPosition": 0, "InitialVelocity": 0, "FinalPosition": 1, "FinalVelocity": 0, "TotalTime": 20}')
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
u = pulp.LpVariable.dicts("u", range(T), lowBound=0)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

# Objective function
problem += pulp.lpSum(u[t] for t in range(T)), "TotalCost"

# Constraints
problem += x[0] == x_0, "InitialPosition"
problem += v[0] == v_0, "InitialVelocity"
problem += x[T] == x_T, "FinalPosition"
problem += v[T] == v_T, "FinalVelocity"

for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionUpdate_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityUpdate_{t}"
    problem += -u[t] <= a[t], f"AccelerationLowerBound_{t}"
    problem += a[t] <= u[t], f"AccelerationUpperBound_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')