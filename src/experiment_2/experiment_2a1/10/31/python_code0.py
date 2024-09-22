import pulp
import json

# Input data in JSON format
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Problem definition
T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of generator types

# Create the model
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", 
                               ((k, t) for k in range(K) for t in range(T)),
                               lowBound=0, 
                               upBound=data['num'][k], 
                               cat='Integer')

# Additional variables for generation levels
genlevel = pulp.LpVariable.dicts("genlevel", 
                                   ((k, t) for k in range(K) for t in range(T)), 
                                   lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(
    (data['startcost'][k] * pulp.lpIndicator(numon[k, t] > 0) + 
     data['runcost'][k] + 
     data['extracost'][k] * (genlevel[k, t] - data['minlevel'][k]) 
    ) 
    for k in range(K) for t in range(T)), "Total_Cost"

# Constraints
for t in range(T):
    # Demand satisfaction
    problem += (pulp.lpSum(genlevel[k, t] for k in range(K)) == data['demand'][t]), f"Demand_Constraint_{t}"
    
    for k in range(K):
        # Min and max generation constraints
        problem += (genlevel[k, t] >= data['minlevel'][k] * numon[k, t]), f"Min_Generation_{k}_{t}"
        problem += (genlevel[k, t] <= data['maxlevel'][k] * numon[k, t]), f"Max_Generation_{k}_{t}"

# Solve the problem
problem.solve()

# Prepare the output
result = {'numon': [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]}

# Output the result and the objective value
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')