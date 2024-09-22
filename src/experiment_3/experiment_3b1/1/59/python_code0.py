import pulp
import json

# Data in JSON format
data = json.loads('{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}')

# Extracting translators and required languages
translators = data['translators']
required_languages = data['required_languages']

# Number of translators
N = len(translators)

# Create the linear programming problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision variables
S = pulp.LpVariable.dicts("Translator", range(N), cat='Binary')

# Objective function
problem += pulp.lpSum([translators[i]['cost'] * S[i] for i in range(N)]), "Total_Cost"

# Constraints
for language in required_languages:
    problem += pulp.lpSum([S[i] for i in range(N) if language in translators[i]['languages']]) >= 1, f"Language_{language}_Requirement"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')