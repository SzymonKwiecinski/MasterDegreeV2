import pulp
import json

# Data
data_json = "{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}"
data = json.loads(data_json.replace("'", '"'))

# Problem variables
demand = data['demand']
N = len(demand)
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, upBound=max_regular_amount, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
storage = [pulp.LpVariable(f'storage_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * storage[n] for n in range(N))

# Constraints
for n in range(N):
    production = reg_quant[n] + over_quant[n] + (storage[n-1] if n > 0 else 0)
    problem += production - demand[n] + (storage[n] if n < N-1 else 0) == 0

# Solve the problem
problem.solve()

# Output results
reg_quant_result = [reg_quant[n].varValue for n in range(N)]
over_quant_result = [over_quant[n].varValue for n in range(N)]

output = {
    "reg_quant": reg_quant_result,
    "over_quant": over_quant_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')