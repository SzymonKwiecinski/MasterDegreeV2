# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A manufacturer wishes to produce \var{alloy_quant} lb of an alloy that consists of several kinds of metals.
- And by weight, the alloy we want contains a target quantity\var{target_{m}} of metal \var{metal_{m}}.
- Several other kinds of alloys are available at various prices. 
- These alloys can be melted to get the alloy we want.
- Alloy \var{k} has \var{ratio_{k, m}} ratio of \var{metal_{m}} and is sold at price of \var{price_k}.
- Ratio \var{ratio_{k, m}} ranges between 0 and 1.0 and should be properly treated in optimization

INPUT FORMAT:

{
	"alloy_quant": alloy_quant,
	"target": [target_{m} for m in 1,...,M],
	"ratio": [[ratio_{k, m} for m in 1,...,M] for k = 1,...,K],
	"price": [price_{k} for k in 1,...,K]
}

OBJECTIVE: The manufacturer wishes to find the amounts of the various alloys needed and to determine the cheapest combination.

OUTPUT INFO:

- \var{amount} represents the quantity of each alloy we buy

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To create a mathematical model for this linear programming problem, we need to focus on minimizing the cost of purchasing various available alloys to produce the desired alloy composition. We will consider the constraints regarding the amount of each metal in the final alloy.

Let's define the variables and translate the problem into a linear programming model:

**Variables:**
- Let \( x_k \) be the amount of alloy \( k \) we purchase, for \( k = 1, \dots, K \).

**Objective Function:**
- We aim to minimize the total cost of purchasing the alloys. Therefore, the objective function is:
  \[
  \text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \cdot x_k
  \]

**Constraints:**
1. The total weight of the purchased alloys must equal the desired alloy quantity:
   \[
   \sum_{k=1}^{K} x_k = \text{alloy\_quant}
   \]

2. For each metal \( m \), the alloy composition must meet the target weight:
   \[
   \sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m, \quad \text{for each } m = 1, \dots, M
   \]

3. Non-negativity constraint for the purchase amounts:
   \[
   x_k \geq 0, \quad \text{for each } k = 1, \dots, K
   \]

Here's the corresponding LaTeX representation of the linear programming model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Subject to:}

1. Total weight constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal composition constraints:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m, \quad \text{for each } m = 1, \dots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0, \quad \text{for each } k = 1, \dots, K
\]

\end{document}
```

This model will guide you in determining the amounts of each alloy to purchase to minimize cost while meeting the metal composition requirements of the desired alloy.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Subject to:}

1. Total weight constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal composition constraints:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m, \quad \text{for each } m = 1, \dots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0, \quad \text{for each } k = 1, \dots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data parsed from JSON
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [
        [0.1, 0.9],
        [0.25, 0.75],
        [0.5, 0.5],
        [0.75, 0.25],
        [0.95, 0.05]
    ],
    'price': [5, 4, 3, 2, 1.5]
}

#### Problem setup
problem = pulp.LpProblem("Metal_Alloy_Problem", pulp.LpMinimize)

#### Decision variables
K = len(data['price'])
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)])

#### Total weight constraint
problem += pulp.lpSum([x[k] for k in range(K)]) == data['alloy_quant']

#### Metal composition constraints
M = len(data['target'])
for m in range(M):
    problem += pulp.lpSum([data['ratio'][k][m] * x[k] for k in range(K)]) == data['target'][m]

#### Solve the problem
problem.solve()

#### Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

