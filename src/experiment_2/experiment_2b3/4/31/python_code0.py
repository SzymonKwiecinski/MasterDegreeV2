import pulp

# Data input
data = {'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}

demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)  # Number of time periods
K = len(num)     # Number of generator types

# Define the problem
problem = pulp.LpProblem("Power_Station_Commitment", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
gen_output = pulp.LpVariable.dicts("gen_output", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective function: Minimize total cost (running, extra, and startup costs)
total_cost = (
    pulp.lpSum(
        numon[k, t] * runcost[k] +
        (gen_output[k, t] - numon[k, t] * minlevel[k]) * extracost[k] +
        startup[k, t] * startcost[k]
        for k in range(K) for t in range(T)
    )
)
problem += total_cost

# Constraints
for t in range(T):
    # Demand satisfaction
    problem += pulp.lpSum(gen_output[k, t] for k in range(K)) >= demand[t]

    for k in range(K):
        # Generating limits for type k generators
        problem += minlevel[k] * numon[k, t] <= gen_output[k, t]
        problem += gen_output[k, t] <= maxlevel[k] * numon[k, t]
        problem += numon[k, t] <= num[k]  # Limit on number of generators that can be turned on

        if t > 0:
            # Startup cost condition
            problem += numon[k, t] - numon[k, t-1] <= startup[k, t]
        else:
            # On first time step, startup cost is straightforward
            problem += numon[k, t] <= startup[k, t]

# Solve the problem
problem.solve()

# Prepare the output
result = {
    "numon": [
        [pulp.value(numon[k, t]) for t in range(T)]
        for k in range(K)
    ]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')