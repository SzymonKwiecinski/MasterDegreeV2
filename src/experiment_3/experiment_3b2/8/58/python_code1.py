import pulp
import json

# Data from the provided JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')  # Number of batches for parts
y = pulp.LpVariable.dicts("y", range(P), cat='Binary')  # Setup variables

# Objective Function
problem += pulp.lpSum(prices[p] * x[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) + (1 if m == 0 else 0) * pulp.lpSum(setup_time[p] * y[p] for p in range(P))) for m in range(M)))

# Constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) + (1 if m == 0 else 0) * pulp.lpSum(setup_time[p] * y[p] for p in range(P))) <= availability[m]

# Constraints for binary variables and non-negativity
for p in range(P):
    problem += y[p] <= 1  # y_p ∈ {0, 1}
    problem += x[p] >= 0  # x_p >= 0
    problem += y[p] == 0 or (x[p] >= 0.01)  # y_p = 0 or x_p >= 0.01

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')