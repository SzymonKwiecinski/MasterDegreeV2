import pulp
import json

# Data
data = json.loads("{'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}")

# Parameters
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Creating the problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Decision Variables: amount[i][j] for shipping from terminal i to destination j
amount = pulp.LpVariable.dicts("amount", 
                                 ((i, j) for i in range(num_terminals) for j in range(num_destinations)),
                                 lowBound=0)

# Objective Function
problem += pulp.lpSum(cost[i][j] * amount[(i, j)] for i in range(num_terminals) for j in range(num_destinations)), "Total Transportation Cost"

# Supply Constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[(i, j)] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[(i, j)] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output results
distribution = [{ 'from': i, 'to': j, 'amount': pulp.value(amount[(i, j)]) }
                for i in range(num_terminals) for j in range(num_destinations) 
                if pulp.value(amount[(i, j)]) > 0]

# Total transportation cost
total_cost = pulp.value(problem.objective)

# Print output
print(f'Distribution: {distribution}')
print(f'Total Transportation Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')