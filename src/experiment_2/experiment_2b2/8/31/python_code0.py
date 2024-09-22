import pulp

# Data from the input
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Extracting values for easier access
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)  # Number of periods
K = len(num)     # Number of generator types

# Initialize problem
problem = pulp.LpProblem("Electricity_Cost_Minimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 0, None, cat='Integer')
output = pulp.LpVariable.dicts("output", ((k, t) for k in range(K) for t in range(T)), 0, None, cat='Continuous')
start_up = pulp.LpVariable.dicts("start_up", ((k, t) for k in range(K) for t in range(T)), 0, 1, cat='Binary')

# Objective function
costs = []
for k in range(K):
    for t in range(T):
        generators_run_cost = numon[(k, t)] * runcost[k]
        extra_generation_cost = output[(k, t)] * extracost[k]
        start_up_cost = start_up[(k, t)] * startcost[k]
        costs.append(generators_run_cost + extra_generation_cost + start_up_cost)

problem += pulp.lpSum(costs)

# Constraints
for t in range(T):
    # Demand constraint
    problem += pulp.lpSum(output[(k, t)] for k in range(K)) >= demand[t]
    for k in range(K):
        # Min level constraints
        problem += output[(k, t)] >= numon[(k, t)] * minlevel[k]
        # Max level constraints
        problem += output[(k, t)] <= numon[(k, t)] * maxlevel[k]
        # Number of generators constraints
        problem += numon[(k, t)] <= num[k]

        # Start-up decision (ensuring accurate start-up cost accounting)
        if t == 0:
            problem += numon[(k, t)] <= start_up[(k, t)] * num[k]
        else:
            problem += numon[(k, t)] - numon[(k, t-1)] <= start_up[(k, t)] * num[k]

# Solve the problem
problem.solve()

# Extract solution
solution_numon = [[int(numon[(k, t)].varValue) for t in range(T)] for k in range(K)]

# Print objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the solution
output_data = {"numon": solution_numon}
print(output_data)