import pulp

# Load data
data = {
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    "strength": [2000, 1500, 1000],
    "lessonewaste": [0.25, 0.2, 0.1],
    "moreonewaste": [0.1, 0.05, 0.05],
    "recruit": [500, 800, 500],
    "costredundancy": [200, 500, 500],
    "num_overman": 150,
    "costoverman": [1500, 2000, 3000],
    "num_shortwork": 50,
    "costshort": [500, 400, 400]
}

requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
recruit_limit = data["recruit"]
costredundancy = data["costredundancy"]
num_overman = data["num_overman"]
costoverman = data["costoverman"]
num_shortwork = data["num_shortwork"]
costshort = data["costshort"]

K = len(strength)
I = len(requirement[0])

# Initialize the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
manpower = pulp.LpVariable.dicts("manpower", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function
objective = pulp.lpSum(
    recruit[k, i] * 0 +  # Recruitment cost is neutral in this problem
    overmanning[k, i] * costoverman[k] +
    short[k, i] * costshort[k] +
    redundancy[k, i] * costredundancy[k]
    for k in range(K) for i in range(I)
)

problem += objective

# Constraints

# Manpower balance constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            manpower_previous_year = strength[k]
        else:
            manpower_previous_year = manpower[k, i-1]

        # Calculate available manpower before considering wastage
        available_manpower = manpower_previous_year * (1 - moreonewaste[k]) + recruit[k, i] * (1 - lessonewaste[k])

        # Constraint for overall balance
        problem += (
            manpower[k, i] == available_manpower + overmanning[k, i] + short[k, i] * (1 / 2) - redundancy[k, i]
        )

# Redundancy cannot exceed manpower
for k in range(K):
    for i in range(I):
        problem += redundancy[k, i] <= manpower[k, i]

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += recruit[k, i] <= recruit_limit[k]

# Overmanning limit
for i in range(I):
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= num_overman

# Short work limit
for k in range(K):
    for i in range(I):
        problem += short[k, i] <= num_shortwork

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "recruit": [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')