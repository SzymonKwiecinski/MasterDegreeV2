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

#### Problem data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

#### Extract data
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  #### number of alloys
S = len(steel_prices)  #### number of steel types

#### Initialize problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision variables
alloy_amount = pulp.LpVariable.dicts("AlloyAmount", [(a, s) for a in range(A) for s in range(S)], lowBound=0)

#### Objective function
profit = pulp.lpSum(
    (steel_prices[s] * pulp.lpSum(alloy_amount[a, s] for a in range(A)) 
     - pulp.lpSum(alloy_prices[a] * alloy_amount[a, s] for a in range(A)))
    for s in range(S)
)
problem += profit, "Total Profit"

#### Constraints

#### Alloy usage restriction
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= available[a], f"AlloyAvailability_{a}"

#### Carbon content requirement
for s in range(S):
    problem += (pulp.lpSum(carbon[a] * alloy_amount[a, s] for a in range(A))
                >= carbon_min[s] * pulp.lpSum(alloy_amount[a, s] for a in range(A))), f"CarbonContent_{s}"

#### Nickel content restriction
for s in range(S):
    problem += (pulp.lpSum(nickel[a] * alloy_amount[a, s] for a in range(A))
                <= nickel_max[s] * pulp.lpSum(alloy_amount[a, s] for a in range(A))), f"NickelContent_{s}"

#### Alloy 1 limitation
for s in range(S):
    problem += alloy_amount[0, s] <= 0.4 * pulp.lpSum(alloy_amount[a, s] for a in range(A)), f"Alloy1_Limit_{s}"

#### Solve the problem
problem.solve()

#### Prepare the output
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel = [sum(alloy_use[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

