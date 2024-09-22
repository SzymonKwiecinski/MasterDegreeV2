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

# Parse data
T = len(data['demand'])  # Number of time periods
K = len(data['num'])  # Number of generator types

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=None, cat='Integer')
power = pulp.LpVariable.dicts("power", (range(K), range(T)), lowBound=0, upBound=None)

# Objective function
startup_cost = pulp.lpSum(data['startcost'][k] * (numon[k][t] > 0) for k in range(K) for t in range(T))
run_cost = pulp.lpSum(data['runcost'][k] * numon[k][t] for k in range(K) for t in range(T))
extra_cost = pulp.lpSum(data['extracost'][k] * (power[k][t] - data['minlevel'][k]) * numon[k][t] for k in range(K) for t in range(T))

total_cost = startup_cost + run_cost + extra_cost
problem += total_cost

# Constraints
for t in range(T):
    # Demand constraint for each time period
    problem += pulp.lpSum(power[k][t] for k in range(K)) >= data['demand'][t]
    
    # Generator output level constraints
    for k in range(K):
        problem += power[k][t] >= data['minlevel'][k] * numon[k][t]
        problem += power[k][t] <= data['maxlevel'][k] * numon[k][t]
        
        # Number of generators constraint
        problem += numon[k][t] <= data['num'][k]

# Solve the problem
problem.solve()

# Prepare output
numon_output = [[int(numon[k][t].varValue) for t in range(T)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the number of generators on
output = {"numon": numon_output}
print(json.dumps(output))