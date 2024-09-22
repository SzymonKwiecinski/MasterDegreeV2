import pulp
import json

# Input data
data = json.loads('{ "demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0 }')

# Problem details
demand = data['demand']
N = len(demand)
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("RegularProduction", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("OvertimeProduction", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
for n in range(N):
    # Inventory flow balance
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - demand[n] + inventory[n] == 0
    else:
        problem += inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n] + inventory[n] == 0
    
    # Regular production limit
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "reg_quant": [reg_quant[n].varValue for n in range(N)],
    "over_quant": [over_quant[n].varValue for n in range(N)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(output))