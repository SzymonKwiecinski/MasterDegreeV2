import pulp

# Data input
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f"reg_quant_{n}", 0) for n in range(N)]
over_quant = [pulp.LpVariable(f"over_quant_{n}", 0) for n in range(N)]
store_amount = [pulp.LpVariable(f"store_amount_{n}", 0) for n in range(N+1)]

# Objective function
problem += (
    pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * store_amount[n+1] for n in range(N))
)

# Constraints
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount, f"Max_Regular_Prod_{n}"
    problem += reg_quant[n] + over_quant[n] + store_amount[n] == demand[n] + store_amount[n+1], f"Demand_Satisfaction_{n}"

# Initial storage is zero
problem += store_amount[0] == 0, "Initial_Storage"

# Solve the problem
problem.solve()

# Output results
output = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')