import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Extracting parameters from data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("Regular_Production", range(N), lowBound=0, upBound=max_regular_amount, cat='Continuous')
over_quant = pulp.LpVariable.dicts("Overtime_Production", range(N), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(N + 1), lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum(cost_regular * reg_quant[n] for n in range(N)) + \
           pulp.lpSum(cost_overtime * over_quant[n] for n in range(N)) + \
           pulp.lpSum(store_cost * inventory[n] for n in range(N + 1))

# Constraints
for n in range(N):
    if n == 0:
        problem += inventory[0] + reg_quant[n] + over_quant[n] >= demand[n], f"Demand_{n}"
    else:
        problem += inventory[n - 1] + reg_quant[n] + over_quant[n] >= demand[n], f"Demand_{n}"
    
    if n < N - 1:
        problem += inventory[n] <= pulp.lpSum(reg_quant[n]) + pulp.lpSum(over_quant[n]), f"Inventory_Limit_{n}"

# Solve the problem
problem.solve()

# Extracting results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

# Output
output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')