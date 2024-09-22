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

\section*{Linear Programming Model for Steel Production}

\textbf{Variables:}
\begin{itemize}
    \item Let \( alloy\_amount_{a,s} \) be the amount of alloy \( a \) used in steel type \( s \).
    \item Let \( total\_steel_{s} \) be the total amount of steel type \( s \) produced.
    \item Let \( total\_profit \) be the total profit from the sale of all types of steel.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( available_{a} \): available tons of alloy \( a \).
    \item \( carbon_{a} \): percentage of carbon in alloy \( a \).
    \item \( nickel_{a} \): percentage of nickel in alloy \( a \).
    \item \( alloy\_price_{a} \): purchase price of alloy \( a \) per ton.
    \item \( steel\_price_{s} \): selling price of steel type \( s \) per ton.
    \item \( carbon\_min_{s} \): minimum allowable percentage of carbon in steel type \( s \).
    \item \( nickel\_max_{s} \): maximum allowable percentage of nickel in steel type \( s \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } total\_profit = \sum_{s=1}^{S} (steel\_price_{s} \cdot total\_steel_{s}) - \sum_{a=1}^{A} (alloy\_price_{a} \cdot \sum_{s=1}^{S} alloy\_amount_{a,s})
\]

\textbf{Constraints:}
\begin{enumerate}
    \item Alloy availability constraints:
    \[
    \sum_{s=1}^{S} alloy\_amount_{a,s} \leq available_{a} \quad \forall a \in \{1,\ldots,A\}
    \]
    
    \item Carbon content constraints for steel types:
    \[
    \frac{\sum_{a=1}^{A} (carbon_{a} \cdot alloy\_amount_{a,s})}{total\_steel_{s}} \geq carbon\_min_{s} \quad \forall s \in \{1,\ldots,S\}
    \]

    \item Nickel content constraints for steel types:
    \[
    \frac{\sum_{a=1}^{A} (nickel_{a} \cdot alloy\_amount_{a,s})}{total\_steel_{s}} \leq nickel\_max_{s} \quad \forall s \in \{1,\ldots,S\}
    \]

    \item Alloy 1 usage constraint:
    \[
    \sum_{s=1}^{S} alloy\_amount_{1,s} \leq 0.4 \cdot total\_steel_{s} \quad \forall s \in \{1,\ldots,S\}
    \]

    \item Non-negativity constraints:
    \[
    alloy\_amount_{a,s} \geq 0 \quad \forall a \in \{1,\ldots,A\}, \forall s \in \{1,\ldots,S\}
    \]
    \[
    total\_steel_{s} \geq 0 \quad \forall s \in \{1,\ldots,S\}
    \]
\end{enumerate}

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

\section*{Linear Programming Model for Steel Production}

\textbf{Variables:}
\begin{itemize}
    \item Let \( alloy\_amount_{a,s} \) be the amount of alloy \( a \) used in steel type \( s \).
    \item Let \( total\_steel_{s} \) be the total amount of steel type \( s \) produced.
    \item Let \( total\_profit \) be the total profit from the sale of all types of steel.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( available_{a} \): available tons of alloy \( a \).
    \item \( carbon_{a} \): percentage of carbon in alloy \( a \).
    \item \( nickel_{a} \): percentage of nickel in alloy \( a \).
    \item \( alloy\_price_{a} \): purchase price of alloy \( a \) per ton.
    \item \( steel\_price_{s} \): selling price of steel type \( s \) per ton.
    \item \( carbon\_min_{s} \): minimum allowable percentage of carbon in steel type \( s \).
    \item \( nickel\_max_{s} \): maximum allowable percentage of nickel in steel type \( s \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } total\_profit = \sum_{s=1}^{S} (steel\_price_{s} \cdot total\_steel_{s}) - \sum_{a=1}^{A} (alloy\_price_{a} \cdot \sum_{s=1}^{S} alloy\_amount_{a,s})
\]

\textbf{Constraints:}
\begin{enumerate}
    \item Alloy availability constraints:
    \[
    \sum_{s=1}^{S} alloy\_amount_{a,s} \leq available_{a} \quad \forall a \in \{1,\ldots,A\}
    \]
    
    \item Carbon content constraints for steel types:
    \[
    \frac{\sum_{a=1}^{A} (carbon_{a} \cdot alloy\_amount_{a,s})}{total\_steel_{s}} \geq carbon\_min_{s} \quad \forall s \in \{1,\ldots,S\}
    \]

    \item Nickel content constraints for steel types:
    \[
    \frac{\sum_{a=1}^{A} (nickel_{a} \cdot alloy\_amount_{a,s})}{total\_steel_{s}} \leq nickel\_max_{s} \quad \forall s \in \{1,\ldots,S\}
    \]

    \item Alloy 1 usage constraint:
    \[
    \sum_{s=1}^{S} alloy\_amount_{1,s} \leq 0.4 \cdot total\_steel_{s} \quad \forall s \in \{1,\ldots,S\}
    \]

    \item Non-negativity constraints:
    \[
    alloy\_amount_{a,s} \geq 0 \quad \forall a \in \{1,\ldots,A\}, \forall s \in \{1,\ldots,S\}
    \]
    \[
    total\_steel_{s} \geq 0 \quad \forall s \in \{1,\ldots,S\}
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

#### Parameters
available = data['available']  #### available tons of alloy
carbon = data['carbon']        #### percentage of carbon in alloy
nickel = data['nickel']        #### percentage of nickel in alloy
alloy_prices = data['alloy_prices']  #### purchase price of alloy per ton
steel_prices = data['steel_prices']  #### selling price of steel type per ton
carbon_min = data['carbon_min']      #### minimum allowable percentage of carbon
nickel_max = data['nickel_max']      #### maximum allowable percentage of nickel

A = len(available)  #### number of alloys
S = len(steel_prices)  #### number of steel types

#### Define the Linear Programming problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

#### Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

#### Objective function
problem += pulp.lpSum(steel_prices[s] * total_steel[s] for s in range(S)) - \
           pulp.lpSum(alloy_prices[a] * pulp.lpSum(alloy_amount[a][s] for s in range(S)) for a in range(A))

#### Constraints
#### Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= available[a]

#### Carbon content constraints
for s in range(S):
    problem += (pulp.lpSum(carbon[a] * alloy_amount[a][s] for a in range(A)) / total_steel[s]) >= carbon_min[s]

#### Nickel content constraints
for s in range(S):
    problem += (pulp.lpSum(nickel[a] * alloy_amount[a][s] for a in range(A)) / total_steel[s]) <= nickel_max[s]

#### Alloy 1 usage constraint
for s in range(S):
    problem += pulp.lpSum(alloy_amount[0][s] for _ in range(S)) <= 0.4 * total_steel[s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

