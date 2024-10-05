# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A company produces \var{S} different types of steel using \var{A} different alloys.
- The company has \var{available_{a}} tons of alloy \var{a} available.
- Steel \var{s} requires a certain percentage of carbon \var{carbon_min_{s}}.
- Steel \var{s} has a maximum allowable percentage for nickel \var{nickel_max_{s}}.
- Alloy \var{a} contains \var{carbon_{a}} percent of carbon and \var{nickel_{a}} percent of nickel.
- Alloy \var{a} has a purchase price of \var{alloy_price_{a}} per ton.
- Steel \var{s} has a selling price of \var{steel_price_{s}} per ton.
- All steel must have at most 40% of alloy 1.

INPUT FORMAT: 

{
"available": [available_{a} for a in 1, ..., A],
"carbon": [carbon_{a} for a in 1, ..., A],
"nickel": [nickel_{a} for a in 1, ..., A],
"alloy_prices": [alloy_price_{a} for a in 1, ..., A],
"steel_prices": [steel_price_{s} for s in 1, ..., S],
"carbon_min": [carbon_min_{s} for s in 1, ..., S],
"nickel_max": [nickel_min_{s} for s in 1, ..., S]
}

OBJECTIVE: How much of each alloy should the company use in each type of steel, and how much of each steel type should be produced to maximize profit?

OUTPUT INFO:

- The amount of each alloy used in each type of steel \var{alloy_amount_{a,s}}.
- \var{total_steel_{s}} shows the total amount of steel type \var{s} produced.
- \var{total_profit} represents the total profit.

OUTPUT FORMAT:

{
    "alloy_use": [[alloy_amount_{a,s} for a in 1, ..., A] for s in 1, ..., S],
    "total_steel": [total_steel_{s} for s in 1, ..., S],
    "total_profit": total_profit
}
</DESCRIPTION>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {
    "available": [40, 50, 80],
    "carbon": [3, 4, 3.5],
    "nickel": [1, 1.5, 1.8],
    "alloy_prices": [380, 400, 440],
    "steel_prices": [650, 600],
    "carbon_min": [3.6, 3.4],
    "nickel_max": [1.5, 1.7]
}

available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)
S = len(steel_prices)

#### Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
alloy_use = pulp.LpVariable.dicts("AlloyUse", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("TotalSteel", (s for s in range(S)), lowBound=0)

#### Objective function
profit = pulp.lpSum(
    steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_prices[a] * alloy_use[a, s] for a in range(A))
    for s in range(S)
)
problem += profit

#### Constraints
#### 1. Availability of each alloy
for a in range(A):
    problem += pulp.lpSum(alloy_use[a, s] for s in range(S)) <= available[a]

#### 2. Carbon and Nickel requirements for each steel type
for s in range(S):
    #### Carbon constraints
    problem += pulp.lpSum(carbon[a] * alloy_use[a, s] for a in range(A)) >= carbon_min[s] * total_steel[s]
    #### Nickel constraints
    problem += pulp.lpSum(nickel[a] * alloy_use[a, s] for a in range(A)) <= nickel_max[s] * total_steel[s]

#### 3. Alloy 1 usage constraint
for s in range(S):
    problem += alloy_use[0, s] <= 0.4 * total_steel[s]

#### 4. Total steel production is the sum of alloys used
for s in range(S):
    problem += total_steel[s] == pulp.lpSum(alloy_use[a, s] for a in range(A))

#### Solve the problem
problem.solve()

#### Collect results
alloy_use_result = [[pulp.value(alloy_use[a, s]) for a in range(A)] for s in range(S)]
total_steel_result = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use_result,
    "total_steel": total_steel_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

