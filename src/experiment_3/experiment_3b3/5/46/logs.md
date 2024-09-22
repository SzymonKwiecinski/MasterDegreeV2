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

\subsection*{Sets}
\begin{itemize}
    \item Let $A$ be the set of alloys, where $a \in \{1, 2, \ldots, A\}$.
    \item Let $S$ be the set of steel types, where $s \in \{1, 2, \ldots, S\}$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $available_a$: Available tons of alloy $a$.
    \item $carbon_{a}$: Percentage of carbon in alloy $a$.
    \item $nickel_{a}$: Percentage of nickel in alloy $a$.
    \item $alloy\_price_{a}$: Price per ton of alloy $a$.
    \item $steel\_price_{s}$: Selling price per ton of steel type $s$.
    \item $carbon\_min_{s}$: Minimum percentage of carbon required for steel type $s$.
    \item $nickel\_max_{s}$: Maximum allowable percentage of nickel for steel type $s$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $alloy\_amount_{a,s}$: Amount of alloy $a$ used in steel type $s$ (in tons).
    \item $total\_steel_{s}$: Total amount of steel type $s$ produced (in tons).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize } Z = \sum_{s=1}^{S} (steel\_price_{s} \cdot total\_steel_{s}) - \sum_{a=1}^{A} (alloy\_price_{a} \cdot \sum_{s=1}^{S} alloy\_amount_{a,s})
\]

\subsection*{Constraints}

1. **Alloy availability**:
\[
\sum_{s=1}^{S} alloy\_amount_{a,s} \leq available_a, \quad \forall a \in A
\]

2. **Carbon requirement**:
\[
\sum_{a=1}^{A} \left( carbon_{a} \cdot alloy\_amount_{a,s} \right) \geq carbon\_min_{s} \cdot total\_steel_{s}, \quad \forall s \in S
\]

3. **Nickel limitation**:
\[
\sum_{a=1}^{A} \left( nickel_{a} \cdot alloy\_amount_{a,s} \right) \leq nickel\_max_{s} \cdot total\_steel_{s}, \quad \forall s \in S
\]

4. **Proportion of alloy 1**:
\[
\sum_{s=1}^{S} alloy\_amount_{1,s} \leq 0.4 \cdot \sum_{s=1}^{S} total\_steel_{s}
\]

5. **Total steel production**:
\[
total\_steel_{s} = \sum_{a=1}^{A} alloy\_amount_{a,s}, \quad \forall s \in S
\]

\subsection*{Non-negativity Constraints}
\[
alloy\_amount_{a,s} \geq 0, \quad \forall a \in A, \forall s \in S
\]
\[
total\_steel_{s} \geq 0, \quad \forall s \in S
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

\subsection*{Sets}
\begin{itemize}
    \item Let $A$ be the set of alloys, where $a \in \{1, 2, \ldots, A\}$.
    \item Let $S$ be the set of steel types, where $s \in \{1, 2, \ldots, S\}$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $available_a$: Available tons of alloy $a$.
    \item $carbon_{a}$: Percentage of carbon in alloy $a$.
    \item $nickel_{a}$: Percentage of nickel in alloy $a$.
    \item $alloy\_price_{a}$: Price per ton of alloy $a$.
    \item $steel\_price_{s}$: Selling price per ton of steel type $s$.
    \item $carbon\_min_{s}$: Minimum percentage of carbon required for steel type $s$.
    \item $nickel\_max_{s}$: Maximum allowable percentage of nickel for steel type $s$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $alloy\_amount_{a,s}$: Amount of alloy $a$ used in steel type $s$ (in tons).
    \item $total\_steel_{s}$: Total amount of steel type $s$ produced (in tons).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize } Z = \sum_{s=1}^{S} (steel\_price_{s} \cdot total\_steel_{s}) - \sum_{a=1}^{A} (alloy\_price_{a} \cdot \sum_{s=1}^{S} alloy\_amount_{a,s})
\]

\subsection*{Constraints}

1. **Alloy availability**:
\[
\sum_{s=1}^{S} alloy\_amount_{a,s} \leq available_a, \quad \forall a \in A
\]

2. **Carbon requirement**:
\[
\sum_{a=1}^{A} \left( carbon_{a} \cdot alloy\_amount_{a,s} \right) \geq carbon\_min_{s} \cdot total\_steel_{s}, \quad \forall s \in S
\]

3. **Nickel limitation**:
\[
\sum_{a=1}^{A} \left( nickel_{a} \cdot alloy\_amount_{a,s} \right) \leq nickel\_max_{s} \cdot total\_steel_{s}, \quad \forall s \in S
\]

4. **Proportion of alloy 1**:
\[
\sum_{s=1}^{S} alloy\_amount_{1,s} \leq 0.4 \cdot \sum_{s=1}^{S} total\_steel_{s}
\]

5. **Total steel production**:
\[
total\_steel_{s} = \sum_{a=1}^{A} alloy\_amount_{a,s}, \quad \forall s \in S
\]

\subsection*{Non-negativity Constraints}
\[
alloy\_amount_{a,s} \geq 0, \quad \forall a \in A, \forall s \in S
\]
\[
total\_steel_{s} \geq 0, \quad \forall s \in S
\]

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

#### Parameters
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

#### Sets
A = range(len(available))  #### Alloys
S = range(len(steel_prices))  #### Steel types

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", [(a, s) for a in A for s in S], lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", S, lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum([steel_prices[s] * total_steel[s] for s in S]) - pulp.lpSum([alloy_prices[a] * alloy_amount[a, s] for a in A for s in S])
problem += profit

#### Constraints
#### Alloy availability
for a in A:
    problem += pulp.lpSum(alloy_amount[a, s] for s in S) <= available[a], f"Alloy_Availability_{a}"

#### Carbon requirement
for s in S:
    problem += pulp.lpSum(carbon[a] * alloy_amount[a, s] for a in A) >= carbon_min[s] * total_steel[s], f"Carbon_Requirement_{s}"

#### Nickel limitation
for s in S:
    problem += pulp.lpSum(nickel[a] * alloy_amount[a, s] for a in A) <= nickel_max[s] * total_steel[s], f"Nickel_Limitation_{s}"

#### Proportion of alloy 1
problem += pulp.lpSum(alloy_amount[0, s] for s in S) <= 0.4 * pulp.lpSum(total_steel[s] for s in S), "Proportion_Alloy_1"

#### Total steel production
for s in S:
    problem += total_steel[s] == pulp.lpSum(alloy_amount[a, s] for a in A), f"Total_Steel_Production_{s}"

#### Solve
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

