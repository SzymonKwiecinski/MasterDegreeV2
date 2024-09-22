import pulp

# Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

# Parameters
P = len(data['prices'])  # Number of different parts
M = len(data['time_required'])  # Number of different machines
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Create the LP problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
labor_cost_expr = pulp.lpSum(
    (standard_cost * pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) 
     if pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) <= overtime_hour
     else standard_cost * overtime_hour + overtime_cost * (pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) - overtime_hour))
)

profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
               pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)) - labor_cost_expr

problem += profit_expr, "TotalProfit"

# Constraints
# Time constraints for each machine
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"MachineAvailability_{m}"

# Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Minimum profit requirement
problem += profit_expr >= min_profit, "MinProfit"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')