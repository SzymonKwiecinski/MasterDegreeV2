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
To formulate this problem as a linear programming model, we need to focus on minimizing the cost while ensuring that the produced alloy has the required composition of each metal. Let's define the decision variables and then set up the objective and constraints.

**Decision Variables:**

- Let \( x_k \) be the amount (in pounds) of alloy \( k \) used in the production of the final alloy for \( k = 1, \ldots, K \).

**Objective Function:**

- Minimize the total cost of purchasing the alloys:
  \[
  \text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \cdot x_k
  \]

**Constraints:**

1. **Total Amount Constraint:**

   The total weight of alloys used should be equal to the desired weight of the final alloy:
   \[
   \sum_{k=1}^{K} x_k = \text{alloy\_quant}
   \]

2. **Metal Composition Constraint:**

   For each metal \( m = 1, \ldots, M \), the weighted sum of the metals in the alloys must match the target weight of metal \( m \) in the final alloy:
   \[
   \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \quad \text{for each } m = 1, \ldots, M
   \]

3. **Non-negativity Constraints:**

   The amount of each alloy used must be non-negative:
   \[
   x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
   \]

Here is the mathematical model formulated in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model for Alloy Production:}

\begin{align*}
\text{Let } & x_k \text{ be the amount of alloy } k \text{ used, for } k = 1, \ldots, K. \\
\\
\text{Objective:} \quad & \text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \cdot x_k \\
\\
\text{Subject to:} \quad & \sum_{k=1}^{K} x_k = \text{alloy\_quant} \\
& \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \quad \text{for each } m = 1, \ldots, M \\
& x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}
```

This LaTeX code specifies the linear programming model for minimizing the cost of creating a specific alloy mixture while ensuring that the final alloy meets specific composition constraints for each metal.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model for Alloy Production:}

\begin{align*}
\text{Let } & x_k \text{ be the amount of alloy } k \text{ used, for } k = 1, \ldots, K. \\
\\
\text{Objective:} \quad & \text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \cdot x_k \\
\\
\text{Subject to:} \quad & \sum_{k=1}^{K} x_k = \text{alloy\_quant} \\
& \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \quad \text{for each } m = 1, \ldots, M \\
& x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the JSON format
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

#### Parameters
K = len(data['price'])   #### Number of alloys
M = len(data['target'])  #### Number of targets

#### Create a linear programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
problem += pulp.lpSum(x[k] for k in range(K)) == data['alloy_quant'], "Total_Alloy_Quantity"

for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(K)) == data['target'][m], f"Target_Constraint_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

