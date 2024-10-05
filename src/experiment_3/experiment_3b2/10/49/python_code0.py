import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Problem setup
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Creating the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * 
                     pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) 
                     for m in range(M))

problem += profit, "Total_Profit"

# Constraints for machines 1 to M-2
for m in range(M-2):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) 
                 <= data['availability'][m]), f"Machine_Availability_{m+1}"

# Combined machine availability for machines M and M-1
problem += (pulp.lpSum(data['time_required'][M-1][p] * batches[p] for p in range(P)) + 
             pulp.lpSum(data['time_required'][M-2][p] * batches[p] for p in range(P)) 
             <= data['availability'][M-1] + data['availability'][M-2]), "Combined_Machine_Availability"

# Minimum production requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Production_Requirement_{p+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')