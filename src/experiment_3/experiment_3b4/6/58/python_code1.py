import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]   
}

# Sets and indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Parameters
time_required = data['time_required']
cost = data['machine_costs']
available = data['availability']
price = data['prices']
setup_time = data['setup_time']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat=pulp.LpContinuous)
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat=pulp.LpBinary)

# Objective Function
profit = pulp.lpSum([price[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([(pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + 
                      (setup_time[p] * setup_flag[p] if m == 0 else 0)) * cost[m] for m in range(M)])

problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + \
               (pulp.lpSum([setup_time[p] * setup_flag[p] for p in range(P)]) if m == 0 else 0) <= available[m]

for p in range(P):
    problem += setup_flag[p] <= batches[p]
    problem += batches[p] >= 0

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')