import pulp

# Data from the provided JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Parameters
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N)), "Total_Cost"

# Constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= demand[n], f"Demand_Constraint_{n+1}"
    else:
        problem += inventory[n-1] + reg_quant[n] + over_quant[n] >= demand[n], f"Demand_Constraint_{n+1}"
    
    problem += reg_quant[n] <= max_regular_amount, f"Regular_Production_Limit_{n+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')