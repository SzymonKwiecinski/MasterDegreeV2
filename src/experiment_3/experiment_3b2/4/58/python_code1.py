import pulp

# Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Define the sets and indices
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + 
         (1 if m == 0 else 0) * pulp.lpSum(data['setup_time'][p] * setup_flag[p] for p in range(P))) 
         for m in range(M))

problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + 
                (1 if m == 0 else 0) * pulp.lpSum(data['setup_time'][p] * setup_flag[p] for p in range(P)) <= data['availability'][m]), f"Machine_Availability_{m}")

U = 1000  # A large constant for upper bound
for p in range(P):
    problem += (setup_flag[p] >= batches[p] / U, f"Setup_Requirement_{p}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')