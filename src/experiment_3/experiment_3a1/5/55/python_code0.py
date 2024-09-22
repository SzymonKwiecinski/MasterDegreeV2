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

# Constants
P = len(data['prices'])  # Number of parts
M = len(data['availability'])  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  # Number of batches for each part

# Objective function: 
# Maximize Z = sum(price_p * b_p) - sum(cost_m * sum(time_{m,p} * b_p)) - Labor Cost for Machine 1

# Labor cost for Machine 1
t = pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P))  # Total time on Machine 1
labor_cost = pulp.LpVariable("labor_cost")
problem += (pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) -
             pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(1, M)) -
             pulp.ifThen(t <= data['overtime_hour'],
                         labor_cost == data['standard_cost'] * t,
                         labor_cost == data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (t - data['overtime_hour'])))

# Constraints
# Machine Availability Constraints
for m in range(1, M):
    problem += pulp.lpSum(data['time_required[m][p]'] * b[p] for p in range(P)) <= data['availability'][m], f"Availability_constraint_machine_{m+1}"

# Minimum batches for each part
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_batches_constraint_part_{p+1}"

# Minimum profit constraint
problem += (pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) -
             pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(1, M)) -
             labor_cost >= data['min_profit'], "Min_profit_constraint")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')