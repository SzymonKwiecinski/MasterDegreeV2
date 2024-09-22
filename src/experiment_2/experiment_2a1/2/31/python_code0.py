import pulp
import json

# Input data
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Parameters
T = len(data['demand'])  # number of time periods
K = len(data['num'])  # number of generator types

# Create the optimization problem
problem = pulp.LpProblem("Power_Generation_Cost_Minimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 
                                     lowBound=0, upBound=data['num'][k], cat='Integer')

# Start variables
start = pulp.LpVariable.dicts("start", (k for k in range(K)), cat='Binary')

# Objective function
total_cost = pulp.lpSum(start[k] * data['startcost'][k] for k in range(K)) + \
    pulp.lpSum(data['runcost'][k] * pulp.lpSum(numon[k, t] for k in range(K)) for t in range(T)) + \
    pulp.lpSum(data['extracost'][k] * pulp.lpSum((numon[k, t] - data['minlevel'][k]) for k in range(K) if numon[k, t] > data['minlevel'][k]) for t in range(T))
problem += total_cost, "Total_Cost"

# Constraints
for t in range(T):
    problem += pulp.lpSum(numon[k, t] for k in range(K)) >= data['demand'][t], f"Demand_Constraint_{t}"

for k in range(K):
    for t in range(T):
        problem += numon[k, t] >= data['minlevel'][k] * start[k], f"Min_Level_Constraint_{k}_{t}"
        problem += numon[k, t] <= data['maxlevel'][k], f"Max_Level_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Prepare output
numon_output = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
result = {"numon": numon_output}
print(result)