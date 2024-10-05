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
To formulate the given problem as a linear programming model, we need to define the decision variables, objective function, and constraints based on the input format.

Let's define:

- Decision Variables: 
  - \( x_k \): the amount (in lb) of alloy \( k \) to purchase, where \( k = 1, \ldots, K \).

- Objective Function:
  - Minimize the total cost of purchasing the alloys.

- Constraints:
  - Ensure that the total weight of the purchased alloys equals the required weight of the alloy (\(\text{alloy\_quant}\)).
  - Ensure that for each metal \( m \), the proportion of that metal in the combination is exactly as required (\(\text{target}_{m}\)).

The linear programming model can be written as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model}

\textbf{Decision Variables:}  
Let \( x_k \) be the amount of alloy \( k \) to purchase for \( k = 1, \ldots, K \).

\textbf{Objective Function:}  
Minimize the total cost of purchasing the alloys:
\[
\min \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\textbf{Constraints:}  
1. The total amount of alloy produced must be equal to the required amount:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. For each metal \( m \), ensure the correct proportion in the final alloy:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \times x_k = \text{target}_{m} \times \text{alloy\_quant}, \quad \forall m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}
```

The above linear programming model accurately represents the problem statement and constraints provided. The objective is to minimize the cost while ensuring the alloy contains the correct proportions of each metal. The decision variables are the amounts of each available alloy to purchase, and the constraints ensure the desired alloy weight and composition are achieved.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model}

\textbf{Decision Variables:}  
Let \( x_k \) be the amount of alloy \( k \) to purchase for \( k = 1, \ldots, K \).

\textbf{Objective Function:}  
Minimize the total cost of purchasing the alloys:
\[
\min \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\textbf{Constraints:}  
1. The total amount of alloy produced must be equal to the required amount:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. For each metal \( m \), ensure the correct proportion in the final alloy:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \times x_k = \text{target}_{m} \times \text{alloy\_quant}, \quad \forall m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
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
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

#### Extract data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

#### Number of alloys and metals
K = len(price)
M = len(target)

#### Create the problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("alloy", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(price[k] * x[k] for k in range(K))

#### Constraints
#### Total amount of alloy produced must be equal to the required amount
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant

#### Proportional constraints for each metal
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m] * alloy_quant

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

