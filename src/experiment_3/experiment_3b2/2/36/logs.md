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
To formulate this linear programming problem, let's define the following:

- Let \( x_k \) be the amount (in lbs) of alloy \( k \) that needs to be purchased.
- The objective is to minimize the total cost of purchasing these alloys.
- The constraint is to meet the target quantity of each metal \( m \) in the final alloy.

The linear programming model can be defined as follows:

######### Objective Function
Minimize the total cost:

\[
\text{Minimize } \sum_{k=1}^{K} \text{price}_k \times x_k
\]

######### Constraints
1. Total weight constraint: Sum of all alloys must equal the required alloy quantity.

\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal composition constraints for each metal \( m \):

\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \times x_k = \text{target}_m \times \text{alloy\_quant} \quad \text{for each } m = 1, \ldots, M
\]

3. Non-negativity constraints:

\[
x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
\]

Here is the complete model in \(\LaTeX\):

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective Function}

Minimize the total cost:
\[
\text{Minimize } \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\subsection*{Constraints}

1. Total weight constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal composition constraints for each metal \( m \):
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \times x_k = \text{target}_m \times \text{alloy\_quant} \quad \text{for each } m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
\]

\end{document}
```

This model aims to determine the optimal quantity of each alloy \( x_k \) to purchase such that the total cost is minimized while satisfying the alloy composition and weight requirements.

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

\subsection*{Objective Function}

Minimize the total cost:
\[
\text{Minimize } \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\subsection*{Constraints}

1. Total weight constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal composition constraints for each metal \( m \):
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \times x_k = \text{target}_m \times \text{alloy\_quant} \quad \text{for each } m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

#### Extracting data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

#### Number of metals and products
M = len(target)
K = len(price)

#### Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum([price[k] * x[k] for k in range(K)]), "Total_Cost"

#### Total weight constraint
problem += pulp.lpSum([x[k] for k in range(K)]) == alloy_quant, "Total_Weight"

#### Metal composition constraints
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * x[k] for k in range(K)]) == target[m] * alloy_quant, f"Metal_Composition_Constraint_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

