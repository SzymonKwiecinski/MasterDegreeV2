import pulp

# Data from JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the problem
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
inventory[0] = 0  # Initial inventory

for n in range(N):
    if n > 0:
        problem += inventory[n] == inventory[n - 1] + reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_{n}"
    problem += reg_quant[n] <= max_regular_amount, f"Max_Regular_Production_{n}"
    problem += inventory[n] >= 0, f"Non_Negative_Inventory_{n}"
    problem += reg_quant[n] >= 0, f"Non_Negative_Regular_Production_{n}"
    problem += over_quant[n] >= 0, f"Non_Negative_Overtime_Production_{n}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')