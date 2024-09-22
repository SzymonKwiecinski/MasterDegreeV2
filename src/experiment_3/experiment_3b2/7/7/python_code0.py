import pulp
import json

# Input data
data = '{"X0": 0, "V0": 0, "XT": 1, "VT": 0, "T": 20}'
params = json.loads(data)

# Parameters
X0 = params['X0']
V0 = params['V0']
XT = params['XT']
VT = params['VT']
T = params['T']

# Create the LP problem
problem = pulp.LpProblem("Rocket_LP_Model", pulp.LpMinimize)

# Decision Variables
a_plus = pulp.LpVariable.dicts("a_plus", range(T), lowBound=0)
a_minus = pulp.LpVariable.dicts("a_minus", range(T), lowBound=0)
z = pulp.LpVariable("z", lowBound=0)

# State variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=0)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=0)

# Objective Function
problem += z

# Constraints
# Initial conditions
problem += x[0] == X0
problem += v[0] == V0

# Dynamic constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + (a_plus[t] - a_minus[t])

# Final conditions
problem += x[T] == XT
problem += v[T] == VT

# Thrust constraints
for t in range(T):
    problem += a_plus[t] >= 0
    problem += a_minus[t] >= 0
    problem += z >= a_plus[t] + a_minus[t]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')