import pulp
import json

# Load data from the provided JSON
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}")

# Extracting data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Define the number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous') # Number of batches
y = pulp.LpVariable.dicts("y", range(P), cat='Binary') # Setup variable

# Objective function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M)) - \
         pulp.lpSum(setup_time[p] * y[p] * machine_costs[0] for p in range(P))

problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) + 
                 (m == 0) * pulp.lpSum(setup_time[p] * y[p] for p in range(P))) <= availability[m], f"Availability_Constraint_{m}")

U = 1  # Assumed upper limit for the relationship between x and y
for p in range(P):
    problem += y[p] >= x[p] / U, f"Setup_Constraint_{p}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')