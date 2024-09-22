import pulp
import json

# Parse the input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Extracting parameters from the data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create the problem
problem = pulp.LpProblem("Minimize_Production_Cost", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("Regular_Prod", range(N), lowBound=0, cat='Continuous')
over_quant = pulp.LpVariable.dicts("Overtime_Prod", range(N), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(N + 1), lowBound=0, cat='Continuous')

# Objective function
problem += (
    pulp.lpSum(cost_regular * reg_quant[n] for n in range(N)) +
    pulp.lpSum(cost_overtime * over_quant[n] for n in range(N)) +
    pulp.lpSum(store_cost * inventory[n] for n in range(1, N + 1))
)

# Constraints
# First month inventory
problem += (inventory[0] == 0)

# Demand satisfaction and inventory constraints
for n in range(N):
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] >= demand[n] + inventory[n])
        problem += (inventory[n + 1] == inventory[n] + reg_quant[n] + over_quant[n] - demand[n])
    else:
        problem += (inventory[n] + reg_quant[n] + over_quant[n] >= demand[n])
        problem += (inventory[n + 1] == inventory[n] + reg_quant[n] + over_quant[n] - demand[n])

# Regular production limit constraints
for n in range(N):
    problem += (reg_quant[n] <= max_regular_amount)

# Solve the problem
problem.solve()

# Prepare the output format
output = {
    "reg_quant": [reg_quant[n].varValue for n in range(N)],
    "over_quant": [over_quant[n].varValue for n in range(N)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the output
print(json.dumps(output))