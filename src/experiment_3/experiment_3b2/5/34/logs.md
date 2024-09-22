# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We assume that there are available at the market different foods and that the food \var{k} sells at a price \var{price_{k}} per unit. 
- In addition there are several basic nutritional ingredients and, to achieve a balanced diet, each individual must receive at least \var{demand_{m}} units of nutrient \var{m} per day. 
- Finally, we assume that each unit of food \var{k} contains \var{nutri_{k, m}} units of nutrition \var{m}

INPUT FORMAT:

{
	"price": [price_{k} for k in 1,...,K],
	"demand": [demand_{m} for m in 1,...,M],
	"nutrition": [[nutri_{k, m} for m in 1,...,M] for k in 1,...,K]
}


OBJECTIVE: We want to minimize the total prices of the foods to purchase.

OUTPUT INFO:

- \var{quantity} represents the quantity of each food to purchase

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this problem as a linear programming problem, we need to establish decision variables, an objective function, and a set of constraints.

**Decision Variables:**
- Let \( x_k \) represent the amount of food \( k \) to purchase, where \( k \) ranges from 1 to \( K \).

**Objective Function:**
- We want to minimize the total cost of purchasing the foods:
  \[
  \text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \times x_k
  \]

**Constraints:**
- For each nutrient \( m \), ensure that the total nutrition provided by the purchased foods meets or exceeds the required demand:
  \[
  \sum_{k=1}^{K} \text{nutri}_{k,m} \times x_k \geq \text{demand}_m \quad \text{for each } m = 1, \ldots, M
  \]

- Non-negativity constraints:
  \[
  x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
  \]

Now, let's write this LP model in LaTeX using the appropriate formatting:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Nutritional Diet Problem}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity of food \( k \) to purchase for \( k = 1, \ldots, K \).

\subsection*{Objective}
Minimize the total cost of purchasing foods:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\subsection*{Subject to Constraints}
\begin{align*}
\sum_{k=1}^{K} \text{nutri}_{k,m} \times x_k & \geq \text{demand}_m, \quad \text{for each } m = 1, \ldots, M \\
x_k & \geq 0, \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}
```

This model can now be solved using any linear programming solver to determine the values of \( x_k \) that minimize the cost while satisfying all nutritional constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Nutritional Diet Problem}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity of food \( k \) to purchase for \( k = 1, \ldots, K \).

\subsection*{Objective}
Minimize the total cost of purchasing foods:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\subsection*{Subject to Constraints}
\begin{align*}
\sum_{k=1}^{K} \text{nutri}_{k,m} \times x_k & \geq \text{demand}_m, \quad \text{for each } m = 1, \ldots, M \\
x_k & \geq 0, \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Define the problem
problem = pulp.LpProblem("Nutritional_Diet_Problem", pulp.LpMinimize)

#### Decision variables
K = len(data['price'])  #### Number of food items
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Quantity of each food item

#### Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
M = len(data['demand'])  #### Number of nutritional demands
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Demand_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

