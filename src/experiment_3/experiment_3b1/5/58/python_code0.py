import pulp
import json

# Data in JSON format
data = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}'''

# Load the data
data = json.loads(data)

# Parameters
P = len(data['prices'])  # Number of different parts
M = len(data['machine_costs'])  # Number of different machines
time_required = data['time_required']  # time_required[m][p]
machine_costs = data['machine_costs']  # cost_m
availability = data['availability']  # available_m
prices = data['prices']  # price_p
setup_time = data['setup_time']  # setup_time_p

# Create the problem
problem = pulp.LpProblem("Production_Problem", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
         pulp.lpSum(setup_flag[p] * setup_time[p] * (1 if m != 0 else 0) for p in range(P))) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + \
               pulp.lpSum(setup_flag[p] * setup_time[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m+1}"

# Non-negativity and integer constraints are already set by variable definitions
# The setup_flag binary constraints are already set by variable definitions

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')