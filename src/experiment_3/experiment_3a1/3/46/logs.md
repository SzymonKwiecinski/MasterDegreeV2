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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $x_{a,s}$ be the amount of alloy $a$ used in producing steel type $s$.
    \item Let $y_s$ be the total amount of steel type $s$ produced.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize } Z &= \sum_{s=1}^{S} (steel\_price_s \cdot y_s) - \sum_{a=1}^{A} (alloy\_price_a \cdot \sum_{s=1}^{S} x_{a,s}) \\
&= \sum_{s=1}^{S} (steel\_price_s \cdot y_s) - \sum_{a=1}^{A} alloy\_price_a \cdot \sum_{s=1}^{S} x_{a,s}
\end{align*}

\textbf{Subject to:}

\textbf{1. Alloy Availability Constraints:}
\begin{align*}
\sum_{s=1}^{S} x_{a,s} &\leq available_a \quad \forall a = 1, \ldots, A
\end{align*}

\textbf{2. Carbon Content Constraints:}
\begin{align*}
\frac{\sum_{a=1}^{A} (carbon_a \cdot x_{a,s})}{y_s} &\geq carbon\_min_s \quad \forall s = 1, \ldots, S
\end{align*}

\textbf{3. Nickel Content Constraints:}
\begin{align*}
\frac{\sum_{a=1}^{A} (nickel_a \cdot x_{a,s})}{y_s} &\leq nickel\_max_s \quad \forall s = 1, \ldots, S
\end{align*}

\textbf{4. Alloy 1 Constraint:}
\begin{align*}
\sum_{s=1}^{S} x_{1,s} &\leq 0.4 \cdot \sum_{s=1}^{S} y_s
\end{align*}

\textbf{5. Non-negativity Constraints:}
\begin{align*}
x_{a,s} &\geq 0 \quad \forall a = 1, \ldots, A, \; s = 1, \ldots, S \\
y_s &\geq 0 \quad \forall s = 1, \ldots, S
\end{align*}

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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $x_{a,s}$ be the amount of alloy $a$ used in producing steel type $s$.
    \item Let $y_s$ be the total amount of steel type $s$ produced.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize } Z &= \sum_{s=1}^{S} (steel\_price_s \cdot y_s) - \sum_{a=1}^{A} (alloy\_price_a \cdot \sum_{s=1}^{S} x_{a,s}) \\
&= \sum_{s=1}^{S} (steel\_price_s \cdot y_s) - \sum_{a=1}^{A} alloy\_price_a \cdot \sum_{s=1}^{S} x_{a,s}
\end{align*}

\textbf{Subject to:}

\textbf{1. Alloy Availability Constraints:}
\begin{align*}
\sum_{s=1}^{S} x_{a,s} &\leq available_a \quad \forall a = 1, \ldots, A
\end{align*}

\textbf{2. Carbon Content Constraints:}
\begin{align*}
\frac{\sum_{a=1}^{A} (carbon_a \cdot x_{a,s})}{y_s} &\geq carbon\_min_s \quad \forall s = 1, \ldots, S
\end{align*}

\textbf{3. Nickel Content Constraints:}
\begin{align*}
\frac{\sum_{a=1}^{A} (nickel_a \cdot x_{a,s})}{y_s} &\leq nickel\_max_s \quad \forall s = 1, \ldots, S
\end{align*}

\textbf{4. Alloy 1 Constraint:}
\begin{align*}
\sum_{s=1}^{S} x_{1,s} &\leq 0.4 \cdot \sum_{s=1}^{S} y_s
\end{align*}

\textbf{5. Non-negativity Constraints:}
\begin{align*}
x_{a,s} &\geq 0 \quad \forall a = 1, \ldots, A, \; s = 1, \ldots, S \\
y_s &\geq 0 \quad \forall s = 1, \ldots, S
\end{align*}

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

#### Constants
A = len(data['available'])  #### Number of alloys
S = len(data['steel_prices'])  #### Number of steel types

#### Create a linear programming problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  #### amount of alloy a in steel s
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)  #### amount of steel s produced

#### Objective Function
problem += pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - \
           pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(x[a][s] for s in range(S)) for a in range(A))

#### Constraints

#### Alloy Availability Constraints
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= data['available'][a]

#### Carbon Content Constraints
for s in range(S):
    problem += (pulp.lpSum(data['carbon'][a] * x[a][s] for a in range(A)) >= data['carbon_min'][s] * y[s]) 

#### Nickel Content Constraints
for s in range(S):
    problem += (pulp.lpSum(data['nickel'][a] * x[a][s] for a in range(A)) <= data['nickel_max'][s] * y[s])

#### Alloy 1 Constraint
problem += pulp.lpSum(x[0][s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

