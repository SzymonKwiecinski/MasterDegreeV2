import pulp
import json

# Input data
data = json.loads("{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}")
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

N = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N + 1)]

# Objective function
problem += pulp.lpSum([cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N)])

# Constraints
for n in range(N):
    if n == 0:
        problem += inventory[0] == 0  # Initial inventory
    if n > 0:
        problem += inventory[n] == inventory[n - 1] + reg_quant[n - 1] + over_quant[n - 1] - demand[n - 1]
    
    problem += reg_quant[n] <= max_regular_amount  # Regular production limit

# Last month's inventory constraint
problem += inventory[N] == inventory[N - 1] + reg_quant[N - 1] + over_quant[N - 1] - demand[N - 1]

# Solve the problem
problem.solve()

# Output the results
result = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(result)