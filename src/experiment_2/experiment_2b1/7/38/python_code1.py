import pulp
import json

# Load data
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

# Parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create the problem
problem = pulp.LpProblem("Minimize_Production_Costs", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("Regular_Production", range(N), lowBound=0, upBound=max_regular_amount, cat='Continuous')
over_quant = pulp.LpVariable.dicts("Overtime_Production", range(N), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(N + 1), lowBound=0, cat='Continuous')  # for N+1 to account for end inventory

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
for n in range(N):
    # Inventory balance
    if n == 0:
        problem += inventory[0] + reg_quant[n] + over_quant[n] == demand[n]
    else:
        problem += inventory[n] + reg_quant[n] + over_quant[n] == demand[n] + inventory[n - 1]
    
    # Ensure inventory carried over
    problem += inventory[n] >= 0

# Ensure the last inventory is zero (not needed to carry over)
problem += inventory[N] == 0

# Solve the problem
problem.solve()

# Prepare output
reg_quant_output = [reg_quant[n].varValue for n in range(N)]
over_quant_output = [over_quant[n].varValue for n in range(N)]

output = {"reg_quant": reg_quant_output, "over_quant": over_quant_output}
print(output)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')