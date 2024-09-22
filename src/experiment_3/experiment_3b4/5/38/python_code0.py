import pulp

# Data from the JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Number of periods
N = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, upBound=data['max_regular_amount'])
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
store_quant = pulp.LpVariable.dicts("store_quant", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * store_quant[n]
    for n in range(N)
])

# Constraints
# Initial storage constraint
prev_store_quant = 0
for n in range(N):
    # Demand Satisfaction Constraint
    problem += reg_quant[n] + over_quant[n] + prev_store_quant == data['demand'][n] + store_quant[n]
    
    # Update the previous store quantity for the next period
    prev_store_quant = store_quant[n]

# Solve the problem
problem.solve()

# Output the optimal value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')