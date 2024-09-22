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
    \item Let \( x_{a,s} \) be the amount of alloy \( a \) used in steel type \( s \) (in tons).
    \item Let \( y_s \) be the total amount of steel type \( s \) produced (in tons).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{available}_{a} \): Available tons of alloy \( a \).
    \item \( \text{carbon}_{a} \): Percentage of carbon in alloy \( a \).
    \item \( \text{nickel}_{a} \): Percentage of nickel in alloy \( a \).
    \item \( \text{alloy\_price}_{a} \): Purchase price per ton of alloy \( a \).
    \item \( \text{steel\_price}_{s} \): Selling price per ton of steel type \( s \).
    \item \( \text{carbon\_min}_{s} \): Minimum percentage of carbon required for steel type \( s \).
    \item \( \text{nickel\_max}_{s} \): Maximum allowable percentage of nickel for steel type \( s \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{s=1}^{S} \left( y_s \cdot \text{steel\_price}_{s} \right) - \sum_{a=1}^{A} \left( \sum_{s=1}^{S} x_{a,s} \cdot \text{alloy\_price}_{a} \right)
\]

\textbf{Subject to:}
\begin{align*}
1. & \quad \sum_{s=1}^{S} x_{a,s} \leq \text{available}_{a}, \quad \forall a \in \{1, \ldots, A\} \\
2. & \quad \sum_{a=1}^{A} x_{a,s} \cdot \text{carbon}_{a} \geq \text{carbon\_min}_{s} \cdot y_s, \quad \forall s \in \{1, \ldots, S\} \\
3. & \quad \sum_{a=1}^{A} x_{a,s} \cdot \text{nickel}_{a} \leq \text{nickel\_max}_{s} \cdot y_s, \quad \forall s \in \{1, \ldots, S\} \\
4. & \quad x_{1,s} \leq 0.4 \cdot y_s, \quad \forall s \in \{1, \ldots, S\} \\
5. & \quad x_{a,s} \geq 0, \quad \forall a \in \{1, \ldots, A\}, s \in \{1, \ldots, S\} \\
6. & \quad y_s \geq 0, \quad \forall s \in \{1, \ldots, S\}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item \( x_{a,s} \): Amount of alloy \( a \) used in steel type \( s \)
    \item \( y_s \): Total amount of steel type \( s \) produced
    \item \( Z \): Total profit
\end{itemize}

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
    \item Let \( x_{a,s} \) be the amount of alloy \( a \) used in steel type \( s \) (in tons).
    \item Let \( y_s \) be the total amount of steel type \( s \) produced (in tons).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{available}_{a} \): Available tons of alloy \( a \).
    \item \( \text{carbon}_{a} \): Percentage of carbon in alloy \( a \).
    \item \( \text{nickel}_{a} \): Percentage of nickel in alloy \( a \).
    \item \( \text{alloy\_price}_{a} \): Purchase price per ton of alloy \( a \).
    \item \( \text{steel\_price}_{s} \): Selling price per ton of steel type \( s \).
    \item \( \text{carbon\_min}_{s} \): Minimum percentage of carbon required for steel type \( s \).
    \item \( \text{nickel\_max}_{s} \): Maximum allowable percentage of nickel for steel type \( s \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{s=1}^{S} \left( y_s \cdot \text{steel\_price}_{s} \right) - \sum_{a=1}^{A} \left( \sum_{s=1}^{S} x_{a,s} \cdot \text{alloy\_price}_{a} \right)
\]

\textbf{Subject to:}
\begin{align*}
1. & \quad \sum_{s=1}^{S} x_{a,s} \leq \text{available}_{a}, \quad \forall a \in \{1, \ldots, A\} \\
2. & \quad \sum_{a=1}^{A} x_{a,s} \cdot \text{carbon}_{a} \geq \text{carbon\_min}_{s} \cdot y_s, \quad \forall s \in \{1, \ldots, S\} \\
3. & \quad \sum_{a=1}^{A} x_{a,s} \cdot \text{nickel}_{a} \leq \text{nickel\_max}_{s} \cdot y_s, \quad \forall s \in \{1, \ldots, S\} \\
4. & \quad x_{1,s} \leq 0.4 \cdot y_s, \quad \forall s \in \{1, \ldots, S\} \\
5. & \quad x_{a,s} \geq 0, \quad \forall a \in \{1, \ldots, A\}, s \in \{1, \ldots, S\} \\
6. & \quad y_s \geq 0, \quad \forall s \in \{1, \ldots, S\}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item \( x_{a,s} \): Amount of alloy \( a \) used in steel type \( s \)
    \item \( y_s \): Total amount of steel type \( s \) produced
    \item \( Z \): Total profit
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from the provided JSON format
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

#### Parameters
A = len(data['available'])  #### Number of alloys
S = len(data['steel_prices'])  #### Number of steel types

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Steel_Production", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  #### Alloy usage in steel production
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)  #### Amount of steel produced

#### Objective Function
profit = pulp.lpSum([y[s] * data['steel_prices'][s] for s in range(S)]) - \
         pulp.lpSum([pulp.lpSum([x[a][s] * data['alloy_prices'][a] for s in range(S)]) for a in range(A)])

problem += profit, "Total_Profit"

#### Constraints
#### 1. Alloy availability
for a in range(A):
    problem += pulp.lpSum([x[a][s] for s in range(S)]) <= data['available'][a], f"Available_Alloy_{a}"

#### 2. Carbon requirement
for s in range(S):
    problem += pulp.lpSum([x[a][s] * data['carbon'][a] for a in range(A)]) >= data['carbon_min'][s] * y[s], f"Carbon_Min_{s}"

#### 3. Nickel limit
for s in range(S):
    problem += pulp.lpSum([x[a][s] * data['nickel'][a] for a in range(A)]) <= data['nickel_max'][s] * y[s], f"Nickel_Max_{s}"

#### 4. Alloy 1 usage limit for all steel types
for s in range(S):
    problem += x[0][s] <= 0.4 * y[s], f"Alloy_1_Usage_Limit_{s}"

#### Solve the problem
problem.solve()

#### Output results
for a in range(A):
    for s in range(S):
        print(f"x[{a},{s}] = {x[a][s].varValue}")

for s in range(S):
    print(f"y[{s}] = {y[s].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

