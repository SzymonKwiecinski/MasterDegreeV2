import pulp
import json

# Data in JSON format
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

# Extracting data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Setting up the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(1, N + 1)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(1, N + 1)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(1, N + 1)]

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n - 1] + cost_overtime * over_quant[n - 1] + store_cost * inventory[n - 1] for n in range(1, N + 1)), "Total_Cost"

# Constraints
# Demand Satisfaction
for n in range(1, N + 1):
    if n == 1:
        problem += reg_quant[n - 1] + over_quant[n - 1] - inventory[n - 1] == demand[n - 1], f"Demand_Satisfaction_{n}"
    else:
        problem += reg_quant[n - 1] + over_quant[n - 1] + inventory[n - 2] - inventory[n - 1] == demand[n - 1], f"Demand_Satisfaction_{n}"

# Regular Production Capacity
for n in range(1, N + 1):
    problem += reg_quant[n - 1] <= max_regular_amount, f"Regular_Production_Capacity_{n}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')