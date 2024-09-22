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

\textbf{Objective:} Maximize total profit

\[
\text{Maximize } Z = \sum_{s=1}^S \text{steel\_price}_s \cdot y_s - \sum_{a=1}^A \text{alloy\_price}_a \cdot \sum_{s=1}^S x_{a,s}
\]

\textbf{Subject to constraints:}

1. **Alloy availability constraints:**
\[
\sum_{s=1}^S x_{a,s} \leq \text{available}_{a}, \quad \forall a \in \{1, \ldots, A\}
\]

2. **Carbon content constraints for each steel type:**
\[
\sum_{a=1}^A \frac{\text{carbon}_{a}}{100} x_{a,s} \geq \text{carbon\_min}_{s} \cdot y_s, \quad \forall s \in \{1, \ldots, S\}
\]

3. **Nickel content constraints for each steel type:**
\[
\sum_{a=1}^A \frac{\text{nickel}_{a}}{100} x_{a,s} \leq \text{nickel\_max}_{s} \cdot y_s, \quad \forall s \in \{1, \ldots, S\}
\]

4. **Maximum limit on alloy 1 usage:**
\[
\sum_{s=1}^S x_{1,s} \leq 0.4 \cdot \sum_{s=1}^S y_s
\]

5. **Non-negativity constraints:**
\[
x_{a,s} \geq 0, \quad y_s \geq 0 \quad \forall a \in \{1, \ldots, A\}, s \in \{1, \ldots, S\}
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

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_{a,s} \) be the amount of alloy \( a \) used in steel type \( s \) (in tons).
    \item Let \( y_s \) be the total amount of steel type \( s \) produced (in tons).
\end{itemize}

\textbf{Objective:} Maximize total profit

\[
\text{Maximize } Z = \sum_{s=1}^S \text{steel\_price}_s \cdot y_s - \sum_{a=1}^A \text{alloy\_price}_a \cdot \sum_{s=1}^S x_{a,s}
\]

\textbf{Subject to constraints:}

1. **Alloy availability constraints:**
\[
\sum_{s=1}^S x_{a,s} \leq \text{available}_{a}, \quad \forall a \in \{1, \ldots, A\}
\]

2. **Carbon content constraints for each steel type:**
\[
\sum_{a=1}^A \frac{\text{carbon}_{a}}{100} x_{a,s} \geq \text{carbon\_min}_{s} \cdot y_s, \quad \forall s \in \{1, \ldots, S\}
\]

3. **Nickel content constraints for each steel type:**
\[
\sum_{a=1}^A \frac{\text{nickel}_{a}}{100} x_{a,s} \leq \text{nickel\_max}_{s} \cdot y_s, \quad \forall s \in \{1, \ldots, S\}
\]

4. **Maximum limit on alloy 1 usage:**
\[
\sum_{s=1}^S x_{1,s} \leq 0.4 \cdot \sum_{s=1}^S y_s
\]

5. **Non-negativity constraints:**
\[
x_{a,s} \geq 0, \quad y_s \geq 0 \quad \forall a \in \{1, \ldots, A\}, s \in \{1, \ldots, S\}
\]

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

#### Define the LP problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (s for s in range(S)), lowBound=0, cat='Continuous')

#### Objective Function
profit = (
    pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) 
    - pulp.lpSum(data['alloy_prices'][a] * x[a, s] for a in range(A) for s in range(S))
)
problem += profit

#### Constraints

#### 1. Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(x[a, s] for s in range(S)) <= data['available'][a]

#### 2. Carbon content constraints
for s in range(S):
    problem += pulp.lpSum((data['carbon'][a] / 100) * x[a, s] for a in range(A)) >= data['carbon_min'][s] * y[s]

#### 3. Nickel content constraints
for s in range(S):
    problem += pulp.lpSum((data['nickel'][a] / 100) * x[a, s] for a in range(A)) <= data['nickel_max'][s] * y[s]

#### 4. Maximum limit on alloy 1 usage
problem += pulp.lpSum(x[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S))

#### Solve the problem
problem.solve()

#### Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

