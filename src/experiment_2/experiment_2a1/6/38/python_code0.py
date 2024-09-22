import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Problem parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("Regular_Production", range(N), lowBound=0, cat='Continuous')
over_quant = pulp.LpVariable.dicts("Overtime_Production", range(N), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(N+1), lowBound=0, cat='Continuous')  # inventory at each month

# Objective function: Minimize total cost
total_cost = (
    pulp.lpSum(cost_regular * reg_quant[n] for n in range(N)) +
    pulp.lpSum(cost_overtime * over_quant[n] for n in range(N)) +
    pulp.lpSum(store_cost * inventory[n] for n in range(N + 1))
)
problem += total_cost

# Constraints
# Inventory constraints
problem += inventory[0] == 0  # starting with zero inventory
for n in range(N):
    if n < N - 1:
        problem += inventory[n + 1] == inventory[n] + reg_quant[n] + over_quant[n] - demand[n]
    else:
        problem += inventory[n + 1] == inventory[n] + reg_quant[n] + over_quant[n] - demand[n] # final inventory

# Production constraints
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount  # Regular production limit
    problem += over_quant[n] >= 0  # No negative overtime production

# Solve the problem
problem.solve()

# Prepare output
output = {
    "reg_quant": [reg_quant[n].varValue for n in range(N)],
    "over_quant": [over_quant[n].varValue for n in range(N)]
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')