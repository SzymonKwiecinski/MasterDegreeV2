import pulp

# Define the problem
problem = pulp.LpProblem("Power_Generation_Scheduling", pulp.LpMinimize)

# Extract data from JSON
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Define parameters
T = len(data['demand'])
K = len(data['num'])

# Define decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
output = pulp.LpVariable.dicts("output", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Define objective function
problem += pulp.lpSum(
    data['runcost'][k] * numon[k, t] +
    data['startcost'][k] * start[k, t] +
    data['extracost'][k] * pulp.lpSum(pulp.lpMax(0, output[k, t] - data['minlevel'][k]))
    for k in range(K) for t in range(T)
)

# Add constraints

# Power Balance Constraint
for t in range(T):
    problem += pulp.lpSum(output[k, t] for k in range(K)) == data['demand'][t], f"Power_Balance_Constraint_{t}"

# Output Level Constraints
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k, t] <= output[k, t], f"Min_Output_Level_Constraint_{k}_{t}"
        problem += output[k, t] <= data['maxlevel'][k] * numon[k, t], f"Max_Output_Level_Constraint_{k}_{t}"

# Generator Activation Constraint
for k in range(K):
    for t in range(T):
        problem += output[k, t] <= data['maxlevel'][k] * numon[k, t], f"Generator_Activation_Constraint_{k}_{t}"

# Startup Decision
for k in range(K):
    for t in range(T):
        problem += output[k, t] >= data['minlevel'][k] * start[k, t], f"Startup_Decision_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')