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
To formulate the given problem as a Linear Programming (LP) model, we need to define decision variables, the objective function, and the constraints.

######### Decision Variables:

- Let \( x_t^{\text{coal}} \) be the coal-fired capacity added in year \( t \).
- Let \( x_t^{\text{nuke}} \) be the nuclear capacity added in year \( t \).

######### Parameters:

- `demand_t`: Demand for electricity in year \( t \).
- `oil_t`: Existing oil-fired capacity available in year \( t \).
- `coal_cost`: Cost per megawatt for coal-fired capacity.
- `nuke_cost`: Cost per megawatt for nuclear capacity.
- `max_nuke`: Maximum percentage of total capacity that can be nuclear.
- `coal_life`: Lifespan of coal plants.
- `nuke_life`: Lifespan of nuclear plants.

######### Objective Function:

Minimize the total cost of adding new capacity over the planning horizon.

\[
\text{Minimize } \sum_{t=1}^T \left( \text{coal\_cost} \cdot x_t^{\text{coal}} + \text{nuke\_cost} \cdot x_t^{\text{nuke}} \right)
\]

######### Constraints:

1. **Demand Satisfaction:**

   For each year \( t \),

   \[
   o_t + \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \geq \text{demand}_t
   \]

2. **Nuclear Capacity Limit:**

   For each year \( t \),

   \[
   \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \leq \frac{\text{max\_nuke}}{100} \times \left( o_t + \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \right)
   \]

3. **Non-negativity:**

   \[
   x_t^{\text{coal}} \geq 0, \quad x_t^{\text{nuke}} \geq 0 \quad \forall \, t = 1, \ldots, T
   \]

######### LATEX Representation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Planning}

\subsection*{Objective Function}

\[
\text{Minimize } \sum_{t=1}^T \left( \text{coal\_cost} \cdot x_t^{\text{coal}} + \text{nuke\_cost} \cdot x_t^{\text{nuke}} \right)
\]

\subsection*{Constraints}

1. \textbf{Demand Satisfaction:}
   \[
   o_t + \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \geq \text{demand}_t
   \]

2. \textbf{Nuclear Capacity Limit:}
   \[
   \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \leq \frac{\text{max\_nuke}}{100} \times \left( o_t + \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \right)
   \]

3. \textbf{Non-negativity:}
   \[
   x_t^{\text{coal}} \geq 0, \quad x_t^{\text{nuke}} \geq 0 \quad \forall \, t = 1, \ldots, T
   \]

\end{document}
```

This model captures the requirements and constraints of the electricity capacity expansion problem. You can solve it using linear programming techniques to find the optimal values for \( x_t^{\text{coal}} \) and \( x_t^{\text{nuke}} \) that minimize the total cost.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Planning}

\subsection*{Objective Function}

\[
\text{Minimize } \sum_{t=1}^T \left( \text{coal\_cost} \cdot x_t^{\text{coal}} + \text{nuke\_cost} \cdot x_t^{\text{nuke}} \right)
\]

\subsection*{Constraints}

1. \textbf{Demand Satisfaction:}
   \[
   o_t + \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \geq \text{demand}_t
   \]

2. \textbf{Nuclear Capacity Limit:}
   \[
   \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \leq \frac{\text{max\_nuke}}{100} \times \left( o_t + \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{\text{nuke}} \right)
   \]

3. \textbf{Non-negativity:}
   \[
   x_t^{\text{coal}} \geq 0, \quad x_t^{\text{nuke}} \geq 0 \quad \forall \, t = 1, \ldots, T
   \]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

#### Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

#### Decision Variables
x_coal = pulp.LpVariable.dicts("x_coal", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
x_nuke = pulp.LpVariable.dicts("x_nuke", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
o = pulp.LpVariable.dicts("o", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(data['CoalCost'] * x_coal[t] + data['NukeCost'] * x_nuke[t] for t in range(1, data['T'] + 1))

#### Constraints

#### Demand Satisfaction
for t in range(1, data['T'] + 1):
    demand_expr = o[t] + pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) + \
                 pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    problem += (demand_expr >= data['Demand'][t - 1], f"Demand_Satisfaction_{t}")

#### Nuclear Capacity Limit
for t in range(1, data['T'] + 1):
    nuke_capacity_expr = pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    problem += (nuke_capacity_expr <= (data['MaxNuke'] / 100) * \
                 (o[t] + pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) + \
                  pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))), 
                 f"Nuclear_Capacity_Limit_{t}")

#### Solve the problem
problem.solve()

#### Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

