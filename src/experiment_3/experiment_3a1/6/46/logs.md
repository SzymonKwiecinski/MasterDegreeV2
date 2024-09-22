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

\textbf{Sets:}
\begin{itemize}
    \item Let \( S \) be the set of steel types.
    \item Let \( A \) be the set of alloys.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{available}_{a} \): available tons of alloy \( a \) for \( a \in A \)
    \item \( \text{carbon}_{a} \): percent of carbon in alloy \( a \) for \( a \in A \)
    \item \( \text{nickel}_{a} \): percent of nickel in alloy \( a \) for \( a \in A \)
    \item \( \text{alloy\_price}_{a} \): purchase price of alloy \( a \) per ton for \( a \in A \)
    \item \( \text{steel\_price}_{s} \): selling price of steel \( s \) per ton for \( s \in S \)
    \item \( \text{carbon\_min}_{s} \): minimum carbon percentage required for steel \( s \) for \( s \in S \)
    \item \( \text{nickel\_max}_{s} \): maximum nickel percentage allowed for steel \( s \) for \( s \in S \)
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item \( x_{a,s} \): amount of alloy \( a \) used in steel type \( s \) 
    \item \( \text{total\_steel}_{s} \): total amount of steel type \( s \) produced
    \item \( \text{total\_profit} \): total profit
\end{itemize}

\textbf{Objective function:}
\[
\text{Maximize } Z = \sum_{s \in S} (\text{steel\_price}_{s} \cdot \text{total\_steel}_{s}) - \sum_{a \in A} (\text{alloy\_price}_{a} \cdot \sum_{s \in S} x_{a,s})
\]

\textbf{Subject to:}

\textbf{Material Constraints:}
\[
\sum_{s \in S} x_{a,s} \leq \text{available}_{a}, \quad \forall a \in A
\]

\textbf{Carbon Constraints:}
\[
\frac{\sum_{a \in A} (x_{a,s} \cdot \text{carbon}_{a})}{\text{total\_steel}_{s}} \geq \text{carbon\_min}_{s}, \quad \forall s \in S
\]

\textbf{Nickel Constraints:}
\[
\frac{\sum_{a \in A} (x_{a,s} \cdot \text{nickel}_{a})}{\text{total\_steel}_{s}} \leq \text{nickel\_max}_{s}, \quad \forall s \in S
\]

\textbf{Alloy 1 Constraint:}
\[
\sum_{s \in S} x_{1,s} \leq 0.4 \cdot \text{total\_steel}_{s}, \quad \forall s \in S
\]

\textbf{Non-negativity Constraints:}
\[
x_{a,s} \geq 0, \quad \forall a \in A, \; s \in S
\]
\[
\text{total\_steel}_{s} \geq 0, \quad \forall s \in S
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

\textbf{Sets:}
\begin{itemize}
    \item Let \( S \) be the set of steel types.
    \item Let \( A \) be the set of alloys.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{available}_{a} \): available tons of alloy \( a \) for \( a \in A \)
    \item \( \text{carbon}_{a} \): percent of carbon in alloy \( a \) for \( a \in A \)
    \item \( \text{nickel}_{a} \): percent of nickel in alloy \( a \) for \( a \in A \)
    \item \( \text{alloy\_price}_{a} \): purchase price of alloy \( a \) per ton for \( a \in A \)
    \item \( \text{steel\_price}_{s} \): selling price of steel \( s \) per ton for \( s \in S \)
    \item \( \text{carbon\_min}_{s} \): minimum carbon percentage required for steel \( s \) for \( s \in S \)
    \item \( \text{nickel\_max}_{s} \): maximum nickel percentage allowed for steel \( s \) for \( s \in S \)
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item \( x_{a,s} \): amount of alloy \( a \) used in steel type \( s \) 
    \item \( \text{total\_steel}_{s} \): total amount of steel type \( s \) produced
    \item \( \text{total\_profit} \): total profit
\end{itemize}

\textbf{Objective function:}
\[
\text{Maximize } Z = \sum_{s \in S} (\text{steel\_price}_{s} \cdot \text{total\_steel}_{s}) - \sum_{a \in A} (\text{alloy\_price}_{a} \cdot \sum_{s \in S} x_{a,s})
\]

\textbf{Subject to:}

\textbf{Material Constraints:}
\[
\sum_{s \in S} x_{a,s} \leq \text{available}_{a}, \quad \forall a \in A
\]

\textbf{Carbon Constraints:}
\[
\frac{\sum_{a \in A} (x_{a,s} \cdot \text{carbon}_{a})}{\text{total\_steel}_{s}} \geq \text{carbon\_min}_{s}, \quad \forall s \in S
\]

\textbf{Nickel Constraints:}
\[
\frac{\sum_{a \in A} (x_{a,s} \cdot \text{nickel}_{a})}{\text{total\_steel}_{s}} \leq \text{nickel\_max}_{s}, \quad \forall s \in S
\]

\textbf{Alloy 1 Constraint:}
\[
\sum_{s \in S} x_{1,s} \leq 0.4 \cdot \text{total\_steel}_{s}, \quad \forall s \in S
\]

\textbf{Non-negativity Constraints:}
\[
x_{a,s} \geq 0, \quad \forall a \in A, \; s \in S
\]
\[
\text{total\_steel}_{s} \geq 0, \quad \forall s \in S
\]

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

#### Sets
alloys = range(len(data['available']))  #### A
steels = range(len(data['steel_prices']))  #### S

#### Parameters
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

#### Variables
x = pulp.LpVariable.dicts("x", (alloys, steels), 0)  #### Amount of alloy a used in steel type s
total_steel = pulp.LpVariable.dicts("total_steel", steels, 0)  #### Total amount of steel produced
total_profit = pulp.LpVariable("total_profit")  #### Total profit

#### Problem Definition
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Objective Function
problem += pulp.lpSum(steel_prices[s] * total_steel[s] for s in steels) - \
           pulp.lpSum(alloy_prices[a] * pulp.lpSum(x[a][s] for s in steels) for a in alloys)

#### Material Constraints
for a in alloys:
    problem += pulp.lpSum(x[a][s] for s in steels) <= available[a]

#### Carbon Constraints
for s in steels:
    problem += pulp.lpSum(x[a][s] * carbon[a] for a in alloys) >= carbon_min[s] * total_steel[s]

#### Nickel Constraints
for s in steels:
    problem += pulp.lpSum(x[a][s] * nickel[a] for a in alloys) <= nickel_max[s] * total_steel[s]

#### Alloy 1 Constraint
for s in steels:
    problem += pulp.lpSum(x[0][s] for a in alloys) <= 0.4 * total_steel[s]

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

