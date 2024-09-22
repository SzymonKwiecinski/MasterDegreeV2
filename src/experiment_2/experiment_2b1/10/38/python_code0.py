import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Problem initialization
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Parameters
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Decision variables
reg_quant = pulp.LpVariable.dicts("Regular_Production", range(N), lowBound=0, cat='Continuous')
over_quant = pulp.LpVariable.dicts("Overtime_Production", range(N), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
for n in range(N):
    # Inventory balance for each month
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - inventory[n] == demand[n]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] - inventory[n] == demand[n]
        
    # Regular production limit
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Output results
reg_quant_output = [pulp.value(reg_quant[n]) for n in range(N)]
over_quant_output = [pulp.value(over_quant[n]) for n in range(N)]

output = {
    "reg_quant": reg_quant_output,
    "over_quant": over_quant_output
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')