import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 
        'max_regular_amount': 5.0, 
        'cost_regular': 10.0, 
        'cost_overtime': 12.0, 
        'store_cost': 1.0}

# Extracting values from data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Problem Definition
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Variables
reg_quant = pulp.LpVariable.dicts("RegularProduction", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("OvertimeProduction", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0)

# Objective Function
total_cost = pulp.lpSum(cost_regular * reg_quant[n] for n in range(N)) + \
             pulp.lpSum(cost_overtime * over_quant[n] for n in range(N)) + \
             pulp.lpSum(store_cost * inventory[n] for n in range(N))

problem += total_cost

# Constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= demand[n], f"Demand_Constraint_{n}"
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] >= demand[n], f"Demand_Constraint_{n}"

    problem += reg_quant[n] <= max_regular_amount, f"Max_Regular_Production_{n}"

    if n < N - 1:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_{n}"
    else:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_Last_{n}"

# Solve the problem
problem.solve()

# Get the results
reg_quant_result = [reg_quant[n].varValue for n in range(N)]
over_quant_result = [over_quant[n].varValue for n in range(N)]

# Print the results
print(json.dumps({"reg_quant": reg_quant_result, "over_quant": over_quant_result}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')