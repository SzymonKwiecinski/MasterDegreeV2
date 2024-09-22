import pulp
import json

# Data provided in JSON format
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}'''

data = json.loads(data_json)

# Parameters
time_required = data['time_required']  # M x P matrix
machine_costs = data['machine_costs']   # M costs
availability = data['availability']       # M availability
prices = data['prices']                   # P prices
setup_time = data['setup_time']           # P setup time

M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
               pulp.lpSum(machine_costs[m] * (
                   pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                   pulp.lpSum(setup_flag[p] * setup_time[p] for p in range(P)) if m == 0) ) for m in range(M))

problem += total_profit, "Total Profit"

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                 pulp.lpSum(setup_flag[p] * setup_time[p] for p in range(P)) if m == 0) <= availability[m], 
                 f"Machine_Availability_Constraint_{m}")

# Setup requirement for machine 1
for p in range(P):
    problem += (setup_flag[p] >= batches[p] / (1 + max(batches[p] for p in range(P))), 
                 f"Setup_Requirement_{p}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')