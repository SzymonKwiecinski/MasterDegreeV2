import pulp

# Load the data
data = {'demand': [10.0, 20.0, 10.0], 
        'max_regular_amount': 5.0, 
        'cost_regular': 10.0, 
        'cost_overtime': 12.0, 
        'store_cost': 1.0}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create LP problem
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

# Variables
reg_quant = pulp.LpVariable.dicts("Regular_Production", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("Overtime_Production", range(N), lowBound=0)
store = pulp.LpVariable.dicts("Storage", range(N+1), lowBound=0)

# Objective Function
problem += pulp.lpSum([cost_regular * reg_quant[i] + 
                       cost_overtime * over_quant[i] + 
                       store_cost * store[i+1] for i in range(N)])

# Constraints
for i in range(N):
    # Satisfy demand
    problem += reg_quant[i] + over_quant[i] + store[i] == demand[i] + store[i+1]
    # Regular production limit
    problem += reg_quant[i] <= max_regular_amount

# Set initial storage to 0
problem += store[0] == 0

# Solve problem
problem.solve()

# Prepare the result
result = {
    "reg_quant": [pulp.value(reg_quant[i]) for i in range(N)],
    "over_quant": [pulp.value(over_quant[i]) for i in range(N)]
}

# Print the result
import json
print(json.dumps(result, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')