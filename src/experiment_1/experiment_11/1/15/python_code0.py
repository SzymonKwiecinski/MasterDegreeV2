import pulp
import json

# Data provided in the problem
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10]
}'''

data = json.loads(data_json)

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines
TimeRequired = data['time_required']  # Time required matrix
MachineCosts = data['machine_costs']  # Costs of machines
Availability = data['availability']  # Availability of machines
Prices = data['prices']  # Prices of parts
MinBatches = data['min_batches']  # Minimum batches

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum(Prices[p] * x[p] for p in range(P)) - \
         pulp.lpSum(MachineCosts[m] * pulp.lpSum(TimeRequired[m][p] * x[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(TimeRequired[m][p] * x[p] for p in range(P)) <= Availability[m], f"Machine_Availability_{m}"

# Minimum production requirement
for p in range(P):
    problem += x[p] >= MinBatches[p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')