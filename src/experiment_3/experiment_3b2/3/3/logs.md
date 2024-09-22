# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A state wants to plan its electricity capacity for the next \var{T} years. 
- The state has a forecast of \var{demand_t} megawatts, presumed accurate, of the demand for electricity during year \var{t}.
- The existing capacity, which is in oil-fired plants, that will not be retired and will be available during year \var{t}, is \var{oil_t}.
- There are two alternatives for expanding electric capacity: coal­ fired or nuclear power plants.
- There is a capital cost of \var{coal_cost} per megawatt of coal-fired capacity that becomes operational at the beginning of year \var{t}.
- There is a capital cost of \var{nuke_cost} per megawatt of nuclear power capacity that becomes operational at the beginning of year \var{t}.
- For various political and safety reasons, it has been decided that no more than \var{max_nuke}% of the total capacity should ever be nuclear (\var{max_nuke} is a number between 0 and 100).
- Coal plants last for \var{coal_life} years, while nuclear plants last for \var{nuke_life} years.

INPUT FORMAT: 

{
    "demand": [demand_t for t in 1, ..., T],
    "oil_cap": [oil_t for t in 1, ..., T],
    "coal_cost": coal_cost,
    "nuke_cost": nuke_cost,
    "max_nuke": max_nuke,
    "coal_life": coal_life,
    "nuke_life": nuke_life,
}


OBJECTIVE: What is the capacity expansion plan that results in the minimum cost?


OUTPUT INFO:

- the output should represent how much coal and nuclear capacity should be added in each year, and how much the total cost is.
- the output should be a dictionary with three keys: "coal_cap_added", "nuke_cap_added", and "total_cost".
- the value of "coal_cap_added" should be a list of the coal capacity added in each year.
- the value of "nuke_cap_added" should be a list of the nuclear capacity added in each year.
- the value of "total_cost" should be a single floating point number showing the total cost of the system.


OUTPUT FORMAT:

{
    "coal_cap_added": [coal_t for t in 1, ..., T],
    "nuke_cap_added": [nuke_t for t in 1, ..., T],
    "total_cost": total_cost,
}


</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate the linear programming model for this problem, we need to define the decision variables, objective function, and constraints.

######### Decision Variables:
- \( \text{coal\_add}_t \): Megawatts of coal-fired capacity added in year \( t \).
- \( \text{nuke\_add}_t \): Megawatts of nuclear power capacity added in year \( t \).

######### Objective Function:
The objective is to minimize the total cost of adding capacity, which consists of the costs of coal and nuclear capacity additions.

######### Constraints:
1. **Demand Satisfaction**:
   - For each year \( t \), the total available capacity (existing oil capacity plus coal and nuclear capacity added over time) should meet or exceed the demand.
2. **Nuclear Capacity Limit**:
   - Total nuclear capacity should not exceed the specified percentage of the total capacity.
3. **Capacity Lifespan**:
   - Coal-fired capacity lasts for `coal_life` years and nuclear capacity lasts for `nuke_life` years.

Now we'll write the linear programming model in LaTeX.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Minimize} \quad Z = \sum_{t=1}^{T} (\text{coal\_cost} \times \text{coal\_add}_t + \text{nuke\_cost} \times \text{nuke\_add}_t)
\]

\textbf{Subject to:}

\begin{align*}
& \text{Demand Satisfaction:} \\
& \sum_{j=\max(1, t-\text{coal\_life}+1)}^t \text{coal\_add}_j + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^t \text{nuke\_add}_j + \text{oil}_t \geq \text{demand}_t, \quad \forall t = 1, \ldots, T \\

& \text{Nuclear Capacity Limit:} \\
& \sum_{j=\max(1, t-\text{nuke\_life}+1)}^t \text{nuke\_add}_j \leq \frac{\text{max\_nuke}}{100} \times \left( \text{oil}_t + \sum_{j=\max(1, t-\text{coal\_life}+1)}^t \text{coal\_add}_j + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^t \text{nuke\_add}_j \right), \quad \forall t = 1, \ldots, T \\

& \text{Non-negativity:} \\
& \text{coal\_add}_t \geq 0, \quad \text{nuke\_add}_t \geq 0, \quad \forall t = 1, \ldots, T
\end{align*}

\end{document}
```

This model seeks to minimize the cost of capacity additions while ensuring demand is met and nuclear capacity limits are respected in every year. The constraints take into account the lifespans of the power plants, so added capacity persists for the appropriate number of years.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Minimize} \quad Z = \sum_{t=1}^{T} (\text{coal\_cost} \times \text{coal\_add}_t + \text{nuke\_cost} \times \text{nuke\_add}_t)
\]

\textbf{Subject to:}

\begin{align*}
& \text{Demand Satisfaction:} \\
& \sum_{j=\max(1, t-\text{coal\_life}+1)}^t \text{coal\_add}_j + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^t \text{nuke\_add}_j + \text{oil}_t \geq \text{demand}_t, \quad \forall t = 1, \ldots, T \\

& \text{Nuclear Capacity Limit:} \\
& \sum_{j=\max(1, t-\text{nuke\_life}+1)}^t \text{nuke\_add}_j \leq \frac{\text{max\_nuke}}{100} \times \left( \text{oil}_t + \sum_{j=\max(1, t-\text{coal\_life}+1)}^t \text{coal\_add}_j + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^t \text{nuke\_add}_j \right), \quad \forall t = 1, \ldots, T \\

& \text{Non-negativity:} \\
& \text{coal\_add}_t \geq 0, \quad \text{nuke\_add}_t \geq 0, \quad \forall t = 1, \ldots, T
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

#### Constants
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

#### Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision variables
coal_add = pulp.LpVariable.dicts("coal_add", range(1, T + 1), lowBound=0)
nuke_add = pulp.LpVariable.dicts("nuke_add", range(1, T + 1), lowBound=0)

#### Objective function
problem += pulp.lpSum(coal_cost * coal_add[t] + nuke_cost * nuke_add[t] for t in range(1, T + 1))

#### Constraints
for t in range(1, T + 1):
    #### Demand Satisfaction
    problem += (pulp.lpSum(coal_add[j] for j in range(max(1, t - coal_life + 1), t + 1)) +
                 pulp.lpSum(nuke_add[j] for j in range(max(1, t - nuke_life + 1), t + 1)) +
                 oil_cap[t - 1] >= demand[t - 1], f"Demand_Satisfaction_{t}")

    #### Nuclear Capacity Limit
    problem += (pulp.lpSum(nuke_add[j] for j in range(max(1, t - nuke_life + 1), t + 1)) <=
                 (max_nuke / 100) * (oil_cap[t - 1] + 
                 pulp.lpSum(coal_add[j] for j in range(max(1, t - coal_life + 1), t + 1)) +
                 pulp.lpSum(nuke_add[j] for j in range(max(1, t - nuke_life + 1), t + 1))), 
                 f"Nuclear_Capacity_Limit_{t}")

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

