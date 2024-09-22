import pulp
import json

# Data provided in JSON format
data = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10]
}'''

# Load data
data = json.loads(data)

# Extract data from loaded JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Setting up the problem
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines
problem = pulp.LpProblem("Auto_Parts_Manufacturing_Problem", pulp.LpMaximize)

# Variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += profit, "Total_Profit"

# Constraints
# Machine availability constraint
problem += \
    pulp.lpSum([pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]) <= \
    pulp.lpSum(availability), "Machine_Availability_Constraint"

# Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_for_Part_{p+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')