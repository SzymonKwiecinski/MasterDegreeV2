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
To solve this problem, we will formulate it as a Linear Programming (LP) problem. The objective is to minimize the cost of purchasing the alloys while meeting the composition requirements for each metal in the final alloy.

######### Decision Variables:
- Let \( x_k \) be the amount in pounds of alloy \( k \) that we purchase for \( k = 1, \ldots, K \).

######### Objective Function:
- Minimize the total cost: 
  \[
  \min \sum_{k=1}^{K} \text{price}_k \cdot x_k
  \]

######### Constraints:
1. **Total Quantity Constraint**: The sum of all purchased alloy quantities should be equal to the desired alloy weight:
   \[
   \sum_{k=1}^{K} x_k = \text{alloy\_quant}
   \]

2. **Metal Composition Constraints**: For each metal \( m = 1, \ldots, M \), the weighted sum of metals in all purchased alloys must meet the target composition:
   \[
   \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant}
   \]

3. **Non-negativity Constraints**:
   \[
   x_k \geq 0 \quad \text{for all } k=1, \ldots, K
   \]

Below is the Linear Programming formulation in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
\[
x_k \quad \text{(amount of alloy } k \text{ purchased, for } k = 1, \ldots, K)
\]

\textbf{Objective Function:}
\[
\min \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Constraints:}

1. Total Quantity Constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal Composition Constraints:
\[
\sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant}, \quad \text{for } m = 1, \ldots, M
\]

3. Non-negativity:
\[
x_k \geq 0 \quad \text{for all } k=1, \ldots, K
\]

\end{document}
```

This model ensures that you purchase the minimum cost combination of available alloys while satisfying the alloy quantity and compositional requirements.

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

\textbf{Decision Variables:}
\[
x_k \quad \text{(amount of alloy } k \text{ purchased, for } k = 1, \ldots, K)
\]

\textbf{Objective Function:}
\[
\min \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Constraints:}

1. Total Quantity Constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal Composition Constraints:
\[
\sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant}, \quad \text{for } m = 1, \ldots, M
\]

3. Non-negativity:
\[
x_k \geq 0 \quad \text{for all } k=1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

#### Extracting data from JSON
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  #### Number of alloys
M = len(target)  #### Number of metal types

#### Create a linear programming problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

#### Total Quantity Constraint
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Quantity"

#### Metal Composition Constraints
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m] * alloy_quant, f"Metal_Composition_Constraint_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

