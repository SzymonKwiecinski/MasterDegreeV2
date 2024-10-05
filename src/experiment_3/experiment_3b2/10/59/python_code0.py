import pulp
import json

# Data provided in JSON format
data = '''{
    "translators": [
        {"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]},
        {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]},
        {"id": 3, "cost": 13000, "languages": ["AR", "CH"]},
        {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]},
        {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]},
        {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}
    ],
    "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]
}'''

# Load data
data_dict = json.loads(data)
translators = data_dict['translators']
required_languages = data_dict['required_languages']

# Create the linear programming problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [t['id'] for t in translators], cat=pulp.LpBinary)

# Objective function
problem += pulp.lpSum([t['cost'] * x[t['id']] for t in translators]), "Total_Cost"

# Constraints
for language in required_languages:
    problem += (
        pulp.lpSum([x[t['id']] for t in translators if language in t['languages']]) >= 1,
        f"Coverage_of_{language}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')