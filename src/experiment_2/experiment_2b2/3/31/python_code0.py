import pulp

# Parse input data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000], 
    'num': [12, 10, 5], 
    'minlevel': [850, 1250, 1500], 
    'maxlevel': [2000, 1750, 4000], 
    'runcost': [1000, 2600, 3000], 
    'extracost': [2.0, 1.3, 3.0], 
    'startcost': [2000, 1000, 500]
}

# Unpack data
demand = data["demand"]
num = data["num"]
minlevel = data["minlevel"]
maxlevel = data["maxlevel"]
runcost = data["runcost"]
extracost = data["extracost"]
startcost = data["startcost"]

T = len(demand)  # Number of periods
K = len(num)     # Number of generator types

# Create a problem instance
problem = pulp.LpProblem("Generator_Scheduling", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, cat='Integer')
gen_output = pulp.LpVariable.dicts("gen_output", ((k, t) for k in range(K) for t in range(T)), 
                                   lowBound=0, cat='Continuous')
start_up = pulp.LpVariable.dicts("start_up", ((k, t) for k in range(K) for t in range(T)), 
                                 cat='Binary')

# Objective function
# Sum over all costs: running costs at min level, extra costs above min level, and startup costs
total_cost = (
    pulp.lpSum(runcost[k] * numon[k, t] + 
               extracost[k] * (gen_output[k, t] - numon[k, t] * minlevel[k]) +
               startcost[k] * start_up[k, t]
               for k in range(K) for t in range(T))
)

problem += total_cost

# Constraints
# Meet demand for each period
for t in range(T):
    problem += pulp.lpSum(gen_output[k, t] for k in range(K)) >= demand[t], f"Demand_{t}"

# Generator operation limits and start-up constraints
for k in range(K):
    for t in range(T):
        # Generator can only operate within its minimum and maximum limits
        problem += gen_output[k, t] <= numon[k, t] * maxlevel[k], f"MaxOutput_{k}_{t}"
        problem += gen_output[k, t] >= numon[k, t] * minlevel[k], f"MinOutput_{k}_{t}"
        
        # Cannot have more generators on than available
        problem += numon[k, t] <= num[k], f"MaxNumOn_{k}_{t}"
        
        # Starting constraints: if a generator is on, it should be either starting up or was on
        if t == 0:
            problem += numon[k, t] <= start_up[k, t] * num[k]
        else:
            problem += numon[k, t] <= numon[k, t - 1] + start_up[k, t]

# Solve the problem
problem.solve()

# Extract the results
result = {
    "numon": [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')