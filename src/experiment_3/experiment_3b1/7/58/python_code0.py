import pulp

# Data initialization from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Extracting parameters
P = len(data['prices'])  # Number of different parts
M = len(data['time_required'])  # Number of different machines
time_required = data['time_required']  # time_{m,p}
machine_costs = data['machine_costs']  # cost_{m}
availability = data['availability']  # available_{m}
prices = data['prices']  # price_{p}
setup_time = data['setup_time']  # setup_time_{p}

# Problem definition
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (time_required[m][p] * batches[p] + 
         setup_flag[p] * setup_time[p]) for m in range(M) for p in range(P))

problem += profit

# Constraints for machine time availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Setup time constraint for machine 1
problem += pulp.lpSum(setup_flag[p] * setup_time[p] for p in range(P)) <= availability[0]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')