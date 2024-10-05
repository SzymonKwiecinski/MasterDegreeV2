import pulp

# Input data received in JSON format
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

# Extracting data
requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
max_recruit = data["recruit"]
costredundancy = data["costredundancy"]
num_overman = data["num_overman"]
costoverman = data["costoverman"]
num_shortwork = data["num_shortwork"]
costshort = data["costshort"]

K = len(strength)  # Number of manpower categories
I = len(requirement[0])  # Number of years

# Define problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy_vars = pulp.LpVariable.dicts("Redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function: Minimize redundancy costs
problem += pulp.lpSum([
    redundancy_vars[k, i] * costredundancy[k]
    for k in range(K) for i in range(I)
])

# Constraints
for k in range(K):
    for i in range(I):
        # Initial workers strength
        if i == 0:
            workers_available = strength[k]
        else:
            # Workers available for this year considering last year's recruit, redundancy, wastage and moreonewaste
            workers_available = (
                recruit_vars[k, i - 1]
                + (strength[k] if i == 1 else sum([recruit_vars[k, j] for j in range(i)]))
                - redundancy_vars[k, i - 1]
            )

            workers_available *= (1 - moreonewaste[k])

        # Total manpower should meet the requirement (considering short-time work and overmanning)
        problem += (
            workers_available 
            + recruit_vars[k, i]
            + overmanning_vars[k, i]
            + 0.5 * short_vars[k, i]
            - redundancy_vars[k, i]
            >= requirement[k][i]
        )

        # Limit the recruits per year
        problem += recruit_vars[k, i] <= max_recruit[k]

        # Limit overmanning
        problem += overmanning_vars[k, i] <= num_overman

        # Limit short-time work
        problem += short_vars[k, i] <= num_shortwork

# Solving the problem
problem.solve()

# Output preparation
output = {
    "recruit": [[pulp.value(recruit_vars[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')