import pulp
import json

# Load data from JSON format
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

# Extracting data from the loaded json
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Define the problem
problem = pulp.LpProblem("Minimize_Production_Costs", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("Regular_Production", range(N), lowBound=0)
y = pulp.LpVariable.dicts("Overtime_Production", range(N), lowBound=0)
s = pulp.LpVariable.dicts("Stored_Units", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(cost_regular * x[n] + cost_overtime * y[n] + store_cost * s[n] for n in range(N))

# Constraints
problem += s[0] == 0  # Starting inventory is 0

for n in range(N):
    problem += x[n] + y[n] + (s[n-1] if n > 0 else 0) == demand[n] + s[n]
    problem += x[n] <= max_regular_amount  # Maximum regular production constraint

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')