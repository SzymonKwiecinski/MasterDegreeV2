import pulp

# Extract data from JSON format
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

T = len(data['demand'])
K = len(data['num'])

# Initialize the LP problem
problem = pulp.LpProblem("Power_Generation_Scheduling", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(
    data['runcost'][k] * numon[k, t] + 
    data['extracost'][k] * (level[k, t] - data['minlevel'][k]) * numon[k, t] +
    data['startcost'][k] * startup[k, t]
    for k in range(K) for t in range(T) if level[k, t] >= data['minlevel'][k]
)

# Constraints

# Demand Satisfaction
for t in range(T):
    problem += (
        pulp.lpSum(level[k, t] for k in range(K)) >= data['demand'][t],
        f"Demand_Satisfaction_{t}"
    )

# Generation Levels
for k in range(K):
    for t in range(T):
        problem += (
            data['minlevel'][k] * numon[k, t] <= level[k, t],
            f"Min_Generation_Level_{k}_{t}"
        )
        problem += (
            level[k, t] <= data['maxlevel'][k] * numon[k, t],
            f"Max_Generation_Level_{k}_{t}"
        )

# Startup Cost Activation
for k in range(K):
    for t in range(T):
        problem += (
            level[k, t] >= data['minlevel'][k] * startup[k, t],
            f"Startup_Cost_Activation_{k}_{t}"
        )

# Operational Limits
for k in range(K):
    for t in range(T):
        problem += (
            numon[k, t] <= data['num'][k],
            f"Operational_Limits_{k}_{t}"
        )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the number of generators that are on during each period
output = {(k, t): pulp.value(numon[k, t]) for k in range(K) for t in range(T)}
print("Output: ", output)