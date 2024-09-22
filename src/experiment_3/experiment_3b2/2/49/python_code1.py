import pulp
import json

# Data provided in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Extracting data from the JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Defining the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Machine availability constraints for machines 1 to M-2
for m in range(M-2):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m+1}"

# Combined availability for Machine M and M-1
problem += pulp.lpSum((time_required[M-1][p] + time_required[M-2][p]) * batches[p] for p in range(P)) <= availability[M-1] + availability[M-2], "Combined_Availability_Constraint"

# Minimum production constraints for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Minimum_Production_Constraint_{p+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')