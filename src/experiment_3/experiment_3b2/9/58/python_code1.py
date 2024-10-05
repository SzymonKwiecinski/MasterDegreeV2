import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Parameters
M = len(data['machine_costs'])  # Number of machines
P = len(data['prices'])          # Number of parts
time = data['time_required']     # time[m][p]
cost = data['machine_costs']     # cost[m]
available = data['availability']  # available[m]
price = data['prices']            # price[p]
setup_time = data['setup_time']   # setup_time[p]
max_p = 1000  # A large number to ensure y_p is set to 1 if x_p > 0

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)  # Batches of parts produced
y = pulp.LpVariable.dicts("y", range(P), cat='Binary')  # Binary variable for setup

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(price[p] * x[p] for p in range(P)) - \
           pulp.lpSum(cost[m] * pulp.lpSum(time[m][p] * x[p] for p in range(P)) for m in range(M)) - \
           pulp.lpSum(setup_time[p] * cost[0] * y[p] for p in range(P))

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time[m][p] * x[p] for p in range(P)) <= available[m]

# Time constraints for machine 1 with setup
for p in range(P):
    problem += time[0][p] * x[p] + setup_time[p] * y[p] <= available[0]

# Linking x and y
for p in range(P):
    problem += y[p] >= (x[p] / max_p)  # Fixing the division syntax error

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')