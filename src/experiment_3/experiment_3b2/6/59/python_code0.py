import pulp
import json

# Read data
data = json.loads('{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}')

# Extract translators and required languages
translators = data['translators']
required_languages = data['required_languages']

# Sets and parameters
N = list(range(len(translators)))  # Translators indexed by i
M = required_languages  # Required languages indexed by m

# Create model
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", N, cat='Binary')

# Objective function
problem += pulp.lpSum(translators[i]['cost'] * x[i] for i in N), "Total_Cost"

# Constraints
for m in M:
    problem += (pulp.lpSum(x[i] for i in N if m in translators[i]['languages']) >= 1, f"Lang_Coverage_{m}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')