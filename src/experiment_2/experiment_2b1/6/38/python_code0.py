import pulp
import json

data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Extracting data from JSON
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create a linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("Regular", range(N), lowBound=0, cat='Continuous')
over_quant = pulp.LpVariable.dicts("Overtime", range(N), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - inventory[n] == demand[n], f"Demand_Fulfillment_{n}"
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] - inventory[n] == demand[n], f"Demand_Fulfillment_{n}"

    problem += reg_quant[n] <= max_regular_amount, f"Max_Regular_Production_{n}"

# Solve the problem
problem.solve()

# Prepare the output
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')