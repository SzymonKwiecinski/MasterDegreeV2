import pulp

# Data from the JSON input
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Indices
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flag = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
               pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += total_profit

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_{m}_Availability"

# Setup Time Constraints for machine 1
for p in range(P):
    problem += batches[p] <= (availability[0] - setup_time[p] * setup_flag[p]) / time_required[0][p], f"Setup_Time_Part_{p}"

# Only one part can be set up on Machine 1
problem += pulp.lpSum(setup_flag[p] for p in range(P)) <= 1, "One_Setup_Flag_Machine_1"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')