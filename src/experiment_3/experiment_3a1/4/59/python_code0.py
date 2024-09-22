import pulp
import json

# Load data from JSON format
data = json.loads('{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}')

# Problem definition
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(len(data['translators'])), cat='Binary')

# Objective Function
problem += pulp.lpSum(translator['cost'] * x[i] for i, translator in enumerate(data['translators'])), "Total_Cost"

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum(x[i] for i, translator in enumerate(data['translators']) if language in translator['languages']) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Output
selected_translators = [i + 1 for i in range(len(data['translators'])) if pulp.value(x[i]) == 1]
total_cost = pulp.value(problem.objective)
print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')