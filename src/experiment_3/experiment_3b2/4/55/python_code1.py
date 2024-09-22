import pulp
import json

# Load data from JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Define number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Integer')

# Calculate H1
H1 = pulp.lpSum(time_required[0][p] * x[p] for p in range(P))

# Objective function
problem += (
    pulp.lpSum(prices[p] * x[p] for p in range(P)) 
    - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M)) 
    - (standard_cost * pulp.lpSum(pulp.lpMin(H1, overtime_hour)) + overtime_cost * pulp.lpSum(pulp.lpMax(0, H1 - overtime_hour)))
)

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Minimum batches constraints
for p in range(P):
    problem += x[p] >= min_batches[p]

# Minimum profit constraint
problem += (pulp.lpSum(prices[p] * x[p] for p in range(P)) 
            - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M)) 
            - (standard_cost * pulp.lpSum(pulp.lpMin(H1, overtime_hour)) + overtime_cost * pulp.lpSum(pulp.lpMax(0, H1 - overtime_hour))) >= min_profit)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')