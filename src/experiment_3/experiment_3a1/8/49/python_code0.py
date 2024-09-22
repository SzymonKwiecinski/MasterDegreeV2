import pulp

# Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Extracting parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define parameters
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Define the objective function
total_profit = pulp.lpSum([prices[p] * x[p] - 
                            pulp.lpSum([machine_costs[m] * (time_required[m][p] * x[p] / 100) 
                                         for m in range(M)]) 
                            for p in range(P)])

problem += total_profit, "Total_Profit"

# Constraints
# Minimum production requirement
for p in range(P):
    problem += x[p] >= min_batches[p], f"MinProductionRequirement_part_{p}"

# Machine availability constraint
problem += (pulp.lpSum([pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) 
                                 for m in range(M)]) <= 
                     pulp.lpSum(availability), "Machine_Availability")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')