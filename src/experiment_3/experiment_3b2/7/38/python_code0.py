import pulp
import json

# Load data from the provided JSON format
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

# Extract data from the dictionary
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', range(N), lowBound=0)  # Regular production
y = pulp.LpVariable.dicts('y', range(N), lowBound=0)  # Overtime production
s = pulp.LpVariable.dicts('s', range(N), lowBound=0)  # Storage

# Objective function
problem += pulp.lpSum(cost_regular * x[n] + cost_overtime * y[n] + store_cost * s[n] for n in range(N)), "Total_Cost"

# Constraints
# Storage initialization
problem += s[0] == 0, "Initial_Storage"

# Demand and production constraints
for n in range(N):
    if n == 0:
        problem += x[n] + y[n] == demand[n] + s[n], f"Demand_Constraint_{n+1}"
    else:
        problem += x[n] + y[n] + s[n-1] == demand[n] + s[n], f"Demand_Constraint_{n+1}"
        
    # Max regular production constraint
    problem += x[n] <= max_regular_amount, f"Max_Regular_Amount_{n+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')