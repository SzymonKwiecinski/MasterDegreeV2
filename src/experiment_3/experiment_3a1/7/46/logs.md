# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( alloy\_amount_{a,s} \) be the amount of alloy \( a \) used in producing steel type \( s \) (in tons).
    \item Let \( total\_steel_{s} \) be the total amount of steel type \( s \) produced (in tons).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } total\_profit = \sum_{s=1}^{S} (steel\_price_{s} \cdot total\_steel_{s}) - \sum_{a=1}^{A} (alloy\_price_{a} \cdot \sum_{s=1}^{S} alloy\_amount_{a,s})
\]

\textbf{Subject to:}

\textit{Alloy Availability Constraints:}
\[
\sum_{s=1}^{S} alloy\_amount_{a,s} \leq available_{a}, \quad \forall a = 1, \ldots, A
\]

\textit{Carbon Requirement Constraints:}
\[
\sum_{a=1}^{A} (carbon_{a} \cdot alloy\_amount_{a,s}) \geq carbon\_min_{s} \cdot total\_steel_{s}, \quad \forall s = 1, \ldots, S
\]

\textit{Nickel Requirement Constraints:}
\[
\sum_{a=1}^{A} (nickel_{a} \cdot alloy\_amount_{a,s}) \leq nickel\_max_{s} \cdot total\_steel_{s}, \quad \forall s = 1, \ldots, S
\]

\textit{Alloy 1 Limitation:}
\[
\sum_{s=1}^{S} alloy\_amount_{1,s} \leq 0.4 \cdot \sum_{s=1}^{S} total\_steel_{s}
\]

\textit{Non-negativity Constraints:}
\[
alloy\_amount_{a,s} \geq 0, \quad \forall a = 1, \ldots, A, \quad s = 1, \ldots, S
\]
\[
total\_steel_{s} \geq 0, \quad \forall s = 1, \ldots, S
\]

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( alloy\_amount_{a,s} \) be the amount of alloy \( a \) used in producing steel type \( s \) (in tons).
    \item Let \( total\_steel_{s} \) be the total amount of steel type \( s \) produced (in tons).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } total\_profit = \sum_{s=1}^{S} (steel\_price_{s} \cdot total\_steel_{s}) - \sum_{a=1}^{A} (alloy\_price_{a} \cdot \sum_{s=1}^{S} alloy\_amount_{a,s})
\]

\textbf{Subject to:}

\textit{Alloy Availability Constraints:}
\[
\sum_{s=1}^{S} alloy\_amount_{a,s} \leq available_{a}, \quad \forall a = 1, \ldots, A
\]

\textit{Carbon Requirement Constraints:}
\[
\sum_{a=1}^{A} (carbon_{a} \cdot alloy\_amount_{a,s}) \geq carbon\_min_{s} \cdot total\_steel_{s}, \quad \forall s = 1, \ldots, S
\]

\textit{Nickel Requirement Constraints:}
\[
\sum_{a=1}^{A} (nickel_{a} \cdot alloy\_amount_{a,s}) \leq nickel\_max_{s} \cdot total\_steel_{s}, \quad \forall s = 1, \ldots, S
\]

\textit{Alloy 1 Limitation:}
\[
\sum_{s=1}^{S} alloy\_amount_{1,s} \leq 0.4 \cdot \sum_{s=1}^{S} total\_steel_{s}
\]

\textit{Non-negativity Constraints:}
\[
alloy\_amount_{a,s} \geq 0, \quad \forall a = 1, \ldots, A, \quad s = 1, \ldots, S
\]
\[
total\_steel_{s} \geq 0, \quad \forall s = 1, \ldots, S
\]

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input as provided
data_json = '{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}'
data = json.loads(data_json)

#### Extract data from the JSON structure
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

#### Define the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Constants
A = len(available)  #### Number of alloys
S = len(steel_prices)  #### Number of steel types

#### Decision Variables
alloy_amount = pulp.LpVariable.dicts("AlloyAmount", (range(A), range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("TotalSteel", range(S), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(steel_prices[s] * total_steel[s] for s in range(S)) - pulp.lpSum(alloy_prices[a] * pulp.lpSum(alloy_amount[a][s] for s in range(S)) for a in range(A))

#### Constraints

#### Alloy Availability Constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= available[a]

#### Carbon Requirement Constraints
for s in range(S):
    problem += pulp.lpSum(carbon[a] * alloy_amount[a][s] for a in range(A)) >= carbon_min[s] * total_steel[s]

#### Nickel Requirement Constraints
for s in range(S):
    problem += pulp.lpSum(nickel[a] * alloy_amount[a][s] for a in range(A)) <= nickel_max[s] * total_steel[s]

#### Alloy 1 Limitation
problem += pulp.lpSum(alloy_amount[0][s] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

