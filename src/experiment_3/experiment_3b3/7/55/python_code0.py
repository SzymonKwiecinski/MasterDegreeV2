import pulp

# Data
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

# Indices
parts = range(4)  # There are 4 parts
machines = range(3)  # There are 3 machines

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", parts, lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in parts)
costs = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in parts) for m in machines)

# Labor Cost Calculation
total_time = pulp.lpSum(time_required[0][p] * batches[p] for p in parts)  # Considering machine 1 for labor calculation

labor_cost = pulp.LpVariable("labor_cost", lowBound=0, cat='Continuous')
problem += (labor_cost == 
            pulp.lpSum(
                [standard_cost * total_time, 
                 overtime_cost * (total_time - overtime_hour)]
            ) - overtime_cost * pulp.lpMin(0, total_time - overtime_hour))

# Objective
problem += profit - costs - labor_cost

# Constraints
# Machine availability constraints
for m in machines:
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in parts) <= availability[m]

# Minimum batches constraints
for p in parts:
    problem += batches[p] >= min_batches[p]

# Minimum profit constraint
problem += profit - costs - labor_cost >= min_profit

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')