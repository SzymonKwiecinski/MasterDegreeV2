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
To formulate this problem as a linear programming model, we need to determine the amount of each type of alloy to purchase such that the desired final alloy composition is achieved at the minimum cost.

Let's denote:
- \( x_k \) as the amount of alloy \( k \) to purchase, for \( k = 1, \ldots, K \).

The objective is to minimize the cost of purchasing the alloys. Thus, the objective function is:

\[
\text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

Subject to the constraints ensuring that the final alloy contains the exact quantity of each metal:

1. For each metal \( m \), ensure that the total amount of metal \( m \) in the mixture matches the target. This can be expressed as:

\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m \quad \text{for} \quad m = 1, \ldots, M
\]

2. The total weight of all alloys used should equal the desired quantity:

\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

3. Non-negativity constraints for all \( x_k \):

\[
x_k \geq 0 \quad \text{for} \quad k = 1, \ldots, K
\]

Now, let’s write the above formulation in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} \text{price}_k \cdot x_k \\
\text{subject to} \quad & \sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m, \quad \text{for} \quad m = 1, \ldots, M \\
& \sum_{k=1}^{K} x_k = \text{alloy\_quant} \\
& x_k \geq 0, \quad \text{for} \quad k = 1, \ldots, K
\end{align*}

\end{document}
``` 

This model will help the manufacturer determine the quantities of each alloy to purchase at the minimum cost while satisfying the metal composition requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} \text{price}_k \cdot x_k \\
\text{subject to} \quad & \sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m, \quad \text{for} \quad m = 1, \ldots, M \\
& \sum_{k=1}^{K} x_k = \text{alloy\_quant} \\
& x_k \geq 0, \quad \text{for} \quad k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

#### Extracting data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  #### Number of different materials
M = len(target)  #### Number of targets

#### Create the linear programming problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"Target_Constraint_{m+1}"

problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

