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
To solve this problem, we need to create a linear programming model that maximizes the company's profit by deciding how much of each alloy should be used to produce different types of steel while considering the constraints regarding availability, carbon and nickel content, and maximum usage of alloy 1.

Here is the mathematical model for this problem in \(\LaTeX\):

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the total profit

\[
\text{Maximize } \quad Z = \sum_{s=1}^{S} \left( \text{steel\_price}_{s} \cdot \text{total\_steel}_{s} \right) - \sum_{a=1}^{A} \sum_{s=1}^{S} \left( \text{alloy\_price}_{a} \cdot \text{alloy\_amount}_{a,s} \right)
\]

\textbf{Subject to:}

\[
\sum_{s=1}^{S} \text{alloy\_amount}_{a,s} \leq \text{available}_{a}, \quad \forall a = 1, \ldots, A
\]

\[
\sum_{a=1}^{A} \text{alloy\_amount}_{a,s} = \text{total\_steel}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\sum_{a=1}^{A} \left( \frac{\text{carbon}_{a}}{100} \cdot \text{alloy\_amount}_{a,s} \right) \geq \frac{\text{carbon\_min}_{s}}{100} \cdot \text{total\_steel}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\sum_{a=1}^{A} \left( \frac{\text{nickel}_{a}}{100} \cdot \text{alloy\_amount}_{a,s} \right) \leq \frac{\text{nickel\_max}_{s}}{100} \cdot \text{total\_steel}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\text{alloy\_amount}_{1,s} \leq 0.4 \cdot \text{total\_steel}_{s}, \quad \forall s = 1, \ldots, S
\]

\textbf{Variables:}
- \(\text{alloy\_amount}_{a,s} \geq 0\), the amount of alloy \(a\) used in steel type \(s\).
- \(\text{total\_steel}_{s} \geq 0\), the total amount of steel type \(s\) produced.

\end{document}
```

This formulation includes:
- The objective function to maximize profit, defined as the total revenue from selling steel minus the cost of purchasing alloys.
- Constraints to ensure that:
  - Total use of each alloy does not exceed available stock.
  - The sum of alloys used equals the total steel produced for each type.
  - Minimum carbon content and maximum nickel content requirements for each type of steel.
  - No more than 40% of each steel type can be composed of alloy 1 due to its usage restriction.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the total profit

\[
\text{Maximize } \quad Z = \sum_{s=1}^{S} \left( \text{steel\_price}_{s} \cdot \text{total\_steel}_{s} \right) - \sum_{a=1}^{A} \sum_{s=1}^{S} \left( \text{alloy\_price}_{a} \cdot \text{alloy\_amount}_{a,s} \right)
\]

\textbf{Subject to:}

\[
\sum_{s=1}^{S} \text{alloy\_amount}_{a,s} \leq \text{available}_{a}, \quad \forall a = 1, \ldots, A
\]

\[
\sum_{a=1}^{A} \text{alloy\_amount}_{a,s} = \text{total\_steel}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\sum_{a=1}^{A} \left( \frac{\text{carbon}_{a}}{100} \cdot \text{alloy\_amount}_{a,s} \right) \geq \frac{\text{carbon\_min}_{s}}{100} \cdot \text{total\_steel}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\sum_{a=1}^{A} \left( \frac{\text{nickel}_{a}}{100} \cdot \text{alloy\_amount}_{a,s} \right) \leq \frac{\text{nickel\_max}_{s}}{100} \cdot \text{total\_steel}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\text{alloy\_amount}_{1,s} \leq 0.4 \cdot \text{total\_steel}_{s}, \quad \forall s = 1, \ldots, S
\]

\textbf{Variables:}
- \(\text{alloy\_amount}_{a,s} \geq 0\), the amount of alloy \(a\) used in steel type \(s\).
- \(\text{total\_steel}_{s} \geq 0\), the total amount of steel type \(s\) produced.

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

A = len(data['available'])
S = len(data['steel_prices'])

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0)

#### Objective Function
problem += (
    pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) -
    pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a, s] for a in range(A) for s in range(S))
)

#### Constraints
#### Alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= data['available'][a]

#### Steel composition
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a, s] for a in range(A)) == total_steel[s]

#### Carbon constraints
for s in range(S):
    problem += (
        pulp.lpSum(data['carbon'][a] / 100 * alloy_amount[a, s] for a in range(A)) >=
        data['carbon_min'][s] / 100 * total_steel[s]
    )

#### Nickel constraints
for s in range(S):
    problem += (
        pulp.lpSum(data['nickel'][a] / 100 * alloy_amount[a, s] for a in range(A)) <=
        data['nickel_max'][s] / 100 * total_steel[s]
    )

#### Special alloy constraint
for s in range(S):
    problem += alloy_amount[0, s] <= 0.4 * total_steel[s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

