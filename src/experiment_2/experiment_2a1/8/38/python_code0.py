import pulp
import json

# Input data in JSON format
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Extracting data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Create the problem variable
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, upBound=max_regular_amount, cat='Continuous')
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(N + 1), lowBound=0, cat='Continuous')  # Inventory for each month

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
problem += (inventory[0] == 0)  # Initial inventory is zero
for n in range(N):
    if n == 0:
        problem += (inventory[n] + reg_quant[n] + over_quant[n] - demand[n] == inventory[n+1])
    else:
        problem += (inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n] == inventory[n+1])
    problem += (reg_quant[n] <= max_regular_amount)  # Regular production limits

# Solve the problem
problem.solve()

# Collecting results
reg_quant_result = [reg_quant[n].varValue for n in range(N)]
over_quant_result = [over_quant[n].varValue for n in range(N)]

# Output format
output = {
    "reg_quant": reg_quant_result,
    "over_quant": over_quant_result
}

print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')