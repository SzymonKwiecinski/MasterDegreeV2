import pulp
import json

# Data provided in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], 
              [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], 
              [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], 
              [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Extracting parameters
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])  # Assuming all limits have same length
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Create the problem
problem = pulp.LpProblem("Engineering_Factory_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(num_machines) for i in range(num_months)), cat='Binary')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k, i] - store_price * storage[k, i] 
                       for k in range(num_products) 
                       for i in range(num_months)), "Total_Profit"

# Constraints
# Production Time Constraint
for m in range(num_machines):
    for i in range(num_months):
        problem += pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(num_products)) \
                   <= n_workhours * (1 - maintain[m, i]), f"ProductionTime_Constraint_m{m}_i{i}"

# Marketing Limitation
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= limit[k][i], f"MarketingLimitation_k{k}_i{i}"

# Storage Dynamics
for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i], f"StorageDynamics_k{k}_i{i}"

# Initial storage condition
for k in range(num_products):
    problem += storage[k, 0] == 0, f"InitialStorage_k{k}"

# Final Inventory Requirement
for k in range(num_products):
    problem += storage[k, num_months-1] >= keep_quantity, f"FinalInventory_k{k}"

# Machine Maintenance Requirement
for i in range(num_months):
    problem += pulp.lpSum(maintain[m, i] for m in range(num_machines)) <= sum(down), f"MaintenanceRequirement_i{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')