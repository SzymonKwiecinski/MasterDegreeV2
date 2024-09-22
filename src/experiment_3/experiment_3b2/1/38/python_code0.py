import pulp

# Data from JSON format
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Problem definition
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
N = len(data['demand'])
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, upBound=data['max_regular_amount'])
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
store = pulp.LpVariable.dicts("store", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(data['cost_regular'] * reg_quant[n] + data['cost_overtime'] * over_quant[n] + 
                       data['store_cost'] * store[n] for n in range(N)), "Total_Cost"

# Constraints
for n in range(N):
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] == data['demand'][n] + store[n]), f"Demand_Constraint_{n}"
    else:
        problem += (reg_quant[n] + over_quant[n] + store[n-1] == data['demand'][n] + store[n]), f"Demand_Constraint_{n}"
        
# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')