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

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_{a,s} \) be the amount of alloy \( a \) used in steel type \( s \) (in tons).
    \item \( y_s \) be the total amount of steel type \( s \) produced (in tons).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( A \): Number of alloys
    \item \( S \): Number of steel types
    \item \( \text{available}_a \): Available tons of alloy \( a \)
    \item \( \text{carbon}_{a} \): Percentage of carbon in alloy \( a \)
    \item \( \text{nickel}_{a} \): Percentage of nickel in alloy \( a \)
    \item \( \text{alloy\_price}_{a} \): Purchase price of alloy \( a \)
    \item \( \text{steel\_price}_{s} \): Selling price of steel type \( s \)
    \item \( \text{carbon\_min}_{s} \): Minimum carbon percentage required for steel type \( s \)
    \item \( \text{nickel\_max}_{s} \): Maximum nickel percentage allowed for steel type \( s \)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{total\_profit} = \sum_{s=1}^{S} \text{steel\_price}_s \cdot y_s - \sum_{a=1}^{A} \text{alloy\_price}_a \cdot \sum_{s=1}^{S} x_{a,s}
\]

\subsection*{Constraints}
1. Alloy availability constraint:
\[
\sum_{s=1}^{S} x_{a,s} \leq \text{available}_a \quad \forall a \in \{1, \ldots, A\}
\]

2. Carbon percentage constraint for each steel type \( s \):
\[
\frac{\sum_{a=1}^{A} x_{a,s} \cdot \text{carbon}_a}{y_s} \geq \text{carbon\_min}_s \quad \forall s \in \{1, \ldots, S\}
\]

3. Nickel percentage constraint for each steel type \( s \):
\[
\frac{\sum_{a=1}^{A} x_{a,s} \cdot \text{nickel}_a}{y_s} \leq \text{nickel\_max}_s \quad \forall s \in \{1, \ldots, S\}
\]

4. Maximum usage of alloy 1:
\[
\sum_{s=1}^{S} x_{1,s} \leq 0.4 \cdot \sum_{s=1}^{S} y_s
\]

5. Non-negativity constraints:
\[
x_{a,s} \geq 0 \quad \forall a \in \{1, \ldots, A\}, s \in \{1, \ldots, S\}
\]
\[
y_s \geq 0 \quad \forall s \in \{1, \ldots, S\}
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

\section*{Linear Programming Model for Steel Production}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_{a,s} \) be the amount of alloy \( a \) used in steel type \( s \) (in tons).
    \item \( y_s \) be the total amount of steel type \( s \) produced (in tons).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( A \): Number of alloys
    \item \( S \): Number of steel types
    \item \( \text{available}_a \): Available tons of alloy \( a \)
    \item \( \text{carbon}_{a} \): Percentage of carbon in alloy \( a \)
    \item \( \text{nickel}_{a} \): Percentage of nickel in alloy \( a \)
    \item \( \text{alloy\_price}_{a} \): Purchase price of alloy \( a \)
    \item \( \text{steel\_price}_{s} \): Selling price of steel type \( s \)
    \item \( \text{carbon\_min}_{s} \): Minimum carbon percentage required for steel type \( s \)
    \item \( \text{nickel\_max}_{s} \): Maximum nickel percentage allowed for steel type \( s \)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{total\_profit} = \sum_{s=1}^{S} \text{steel\_price}_s \cdot y_s - \sum_{a=1}^{A} \text{alloy\_price}_a \cdot \sum_{s=1}^{S} x_{a,s}
\]

\subsection*{Constraints}
1. Alloy availability constraint:
\[
\sum_{s=1}^{S} x_{a,s} \leq \text{available}_a \quad \forall a \in \{1, \ldots, A\}
\]

2. Carbon percentage constraint for each steel type \( s \):
\[
\frac{\sum_{a=1}^{A} x_{a,s} \cdot \text{carbon}_a}{y_s} \geq \text{carbon\_min}_s \quad \forall s \in \{1, \ldots, S\}
\]

3. Nickel percentage constraint for each steel type \( s \):
\[
\frac{\sum_{a=1}^{A} x_{a,s} \cdot \text{nickel}_a}{y_s} \leq \text{nickel\_max}_s \quad \forall s \in \{1, \ldots, S\}
\]

4. Maximum usage of alloy 1:
\[
\sum_{s=1}^{S} x_{1,s} \leq 0.4 \cdot \sum_{s=1}^{S} y_s
\]

5. Non-negativity constraints:
\[
x_{a,s} \geq 0 \quad \forall a \in \{1, \ldots, A\}, s \in \{1, \ldots, S\}
\]
\[
y_s \geq 0 \quad \forall s \in \{1, \ldots, S\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

#### Define the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Define sets
A = range(len(data['available']))  #### Alloys
S = range(len(data['steel_prices']))  #### Steel types

#### Decision Variables
x = pulp.LpVariable.dicts("x", (A, S), lowBound=0)  #### Amount of alloy a used for steel type s
y = pulp.LpVariable.dicts("y", S, lowBound=0)        #### Total amount of steel type s produced

#### Objective Function
profit = pulp.lpSum(data['steel_prices'][s] * y[s] for s in S) - pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(x[a][s] for s in S) for a in A)
problem += profit

#### Constraints
#### Alloy availability constraint
for a in A:
    problem += pulp.lpSum(x[a][s] for s in S) <= data['available'][a]

#### Carbon percentage constraints
for s in S:
    problem += (pulp.lpSum(x[a][s] * data['carbon'][a] for a in A) >= data['carbon_min'][s] * y[s])

#### Nickel percentage constraints
for s in S:
    problem += (pulp.lpSum(x[a][s] * data['nickel'][a] for a in A) <= data['nickel_max'][s] * y[s])

#### Maximum usage of alloy 1
problem += (pulp.lpSum(x[0][s] for s in S) <= 0.4 * pulp.lpSum(y[s] for s in S))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

