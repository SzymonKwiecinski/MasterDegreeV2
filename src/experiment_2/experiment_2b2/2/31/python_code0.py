import pulp

# Load the data
data = {
    "demand": [15000, 30000, 25000, 40000, 27000],
    "num": [12, 10, 5],
    "minlevel": [850, 1250, 1500],
    "maxlevel": [2000, 1750, 4000],
    "runcost": [1000, 2600, 3000],
    "extracost": [2.0, 1.3, 3.0],
    "startcost": [2000, 1000, 500]
}

# Parameters
T = len(data['demand'])  # number of periods
K = len(data['num'])     # number of generator types

# Initialize the LP problem
problem = pulp.LpProblem("PowerGeneration", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, upBound=1, cat='Binary')
power_generated = pulp.LpVariable.dicts("power_generated", ((k, t) for k in range(K) for t in range(T)), 
                                        lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum(
    [
        numon[k, t] * data['runcost'][k] * data['minlevel'][k] +
        numon[k, t] * data['startcost'][k] +
        power_generated[k, t] * data['extracost'][k]
        for k in range(K) for t in range(T)
    ]
)
problem += total_cost

# Constraints
for t in range(T):
    # Demand satisfaction
    problem += pulp.lpSum(power_generated[k, t] for k in range(K)) >= data['demand'][t], f"Demand_{t}"

    for k in range(K):
        # Power generation within limits
        problem += power_generated[k, t] >= numon[k, t] * data['minlevel'][k], f"Min_Power_{k}_{t}"
        problem += power_generated[k, t] <= numon[k, t] * data['maxlevel'][k], f"Max_Power_{k}_{t}"
        # Number of generators within available units
        problem += numon[k, t] <= data['num'][k], f"Num_Generators_{k}_{t}"

# Solve the problem
problem.solve()

# Extract the results
numon_result = [[int(numon[k, t].varValue) for t in range(T)] for k in range(K)]

# Output format
output = {
    "numon": numon_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')