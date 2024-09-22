# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A company is undergoing a number of changes that will affect its manpower requirements in future years. 
- Owing to the installation of new machinery, fewer unskilled but more skilled and semi-skilled workers will be required. 
- In addition to this, a downturn in trade is expected in the next year, which will reduce the need for workers in all categories.
- The estimated manpower requirements for manpower \var{k} in year \var{i} is \var{requirement_{k, i}}.
- The current strength of manpower \var{k} is \var{strength_{k}}.
- The company wishes to decide its policy with regard to recruitment, retraining, redundancy and short-time working in the next years.
- There is a natural wastage of labour. 
- A fairly large number of workers leave during their first year. After this, the rate is much smaller. 
- Taking this into account, the wastage rates of \var{k} manpower with less than one year's service is \var{lessonewaste_{k}}.
- The wastage rates of \var{k} manpower with more than one year's service is \var{moreonewaste_{k}}.
- There has been no recent recruitment and all workers in the current labour force have been employed for more than one year.
- It is possible to recruit a limited number of workers from outside. 
- In any one year, the numbers that can be recruited in manpower \var{k} is \var{recruit_{k}}.
- The redundancy payment to manpower \var{k} is \var{costredundancy_{k}}.
- It is possible to employ up to \var{num_overman} more workers over the whole company than are needed, but the extra costs per employee per year is \var{costoverman_{k}} for manpower \var{k}.
- Up to \var{num_shortwork} workers in each category of skill can be put on short-time working. 
- The cost of this (per employee per year) is \var{costshort_{k}} for manpower \var{k}.
- An employee on short-time working meets the production requirements of half a full-time employee.


INPUT FORMAT:

{
    "requirement": [[requirement_{k, i} for i in 1,...,I] for k in 1,...,K],
    "strength": [strength_{k} for k in 1,...,K],
    "lessonewaste": [lessonewaste_{k} for k in 1,...,K],
    "moreonewaste": [lessonewaste_{k} for k in 1,...,K],
    "recruit": [recruit_{k} for k in 1,...,K],
    "costredundancy": [costredundancy_{k} for k in 1,...,K],
    "num_overman": num_overman,
    "costoverman": [costoverman_{k} for k in 1,...,K],
    "num_shortwork": num_shortwork
    "costshort": [costshort_{k} for k in 1,...,K],
}


OBJECTIVE: The company’s declared objective is to minimize costs. How should they operate in order to do this?

OUTPUT INFO:

- \var{recruit} represents the number of each recruit manpower to employ each year
- \var{overmanning} represents the number of each overmanning manpower to employ each year
- \var{short} represents the number of each short-time manpower to employ each year

OUTPUT FORMAT:

{
    "recruit": [[recruit_{k, i} for i in 1,...,I] for k in 1,...,K],
    "overmanning": [[overmanning_{k, i} for i in 1,...,I] for k in 1,...,K],
    "short": [[short_{k, i} for i in 1,...,I] for k in 1,...,K]
}
</DESCRIPTION>
<DATA>
{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input Data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

K = len(data['strength'])  #### Number of manpower categories
I = len(data['requirement'][0])  #### Number of years

#### Define the problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

#### Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')

#### Objective Function
cost = pulp.lpSum(
    data['costredundancy'][k] * (data['strength'][k] + pulp.lpSum(overmanning[k][i] for i in range(I)) - data['requirement'][k][i]) 
    for k in range(K) for i in range(I)) + \
    pulp.lpSum(data['costoverman'][k] * overmanning[k][i] for k in range(K) for i in range(I)) + \
    pulp.lpSum(data['costshort'][k] * short[k][i] for k in range(K) for i in range(I))

problem += cost, "Total_Cost"

#### Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] - pulp.lpSum(recruit[k][i] for k in range(K)) +
            (1 - data['lessonewaste'][k]) * data['strength'][k] +
            (1 - data['moreonewaste'][k]) * (data['strength'][k] - pulp.lpSum(recruit[k][i-1] for i in range(1, I))) - 
            overmanning[k][i] + short[k][i] >= data['requirement'][k][i],
            f"Demand_Constraint_k{k}_i{i}"
        )
        
        problem += recruit[k][i] <= data['recruit'][k], f"Recruit_Constraint_k{k}_i{i}"
        
        if i > 0:
            problem += overmanning[k][i] <= data['num_overman'], f"Overmanning_Constraint_k{k}_i{i}"
            problem += short[k][i] <= data['num_shortwork'], f"Short_Time_Constraint_k{k}_i{i}"

#### Solve the problem
problem.solve()

#### Prepare Output
recruit_solution = [[int(recruit[k][i].varValue) for i in range(I)] for k in range(K)]
overmanning_solution = [[int(overmanning[k][i].varValue) for i in range(I)] for k in range(K)]
short_solution = [[int(short[k][i].varValue) for i in range(I)] for k in range(K)]

output = {
    "recruit": recruit_solution,
    "overmanning": overmanning_solution,
    "short": short_solution
}

#### Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

