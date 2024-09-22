import pulp
import json

# Data extraction from JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Constants
time_required = data['time_required']  # P x M matrix
machine_costs = data['machine_costs']  # M costs
availability = data['availability']  # M available time
prices = data['prices']  # P prices
setup_time = data['setup_time']  # P setup times

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines
B = float('inf')  # Assuming B is sufficiently large for this example (no limit on production if setup)

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')  # Batches of parts
y = pulp.LpVariable.dicts("y", range(P), cat='Binary')  # Setup of parts

# Objective Function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) + 
                                           pulp.lpSum(setup_time[p] * y[p] for p in range(P)) * (1 if m == 0 else 0))
                            for m in range(M)))

problem += profit

# Constraints
# Machine time availability constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * x[p] + 
                            setup_time[p] * y[p] * (1 if m == 0 else 0) for p in range(P)) <= availability[m]),
                f"availability_constraint_for_machine_{m+1}")

# Setup constraint for machine 1
for p in range(P):
    problem += (x[p] <= B * y[p], f"setup_constraint_for_part_{p+1}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')