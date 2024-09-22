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
To create a linear programming model for this problem, we aim to minimize the total cost of purchasing foods while satisfying the nutritional requirements. The decision variable is the quantity of each food type to purchase. Here's the mathematical formulation of the problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Problem Formulation}

\subsection*{Decision Variables}
Let \( \text{quantity}_k \) be the quantity of food \( k \) to purchase (for \( k = 1, \ldots, K \)).

\subsection*{Objective Function}
Minimize the total cost of purchasing foods:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
To satisfy the nutritional requirements, the following constraints must hold for each nutrient \( m \) (for \( m = 1, \ldots, M \)):

\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m
\]

\subsection*{Non-negativity Constraints}

\[
\text{quantity}_k \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

\end{document}
```

In this model:
- The objective function represents the total cost, which we want to minimize.
- The constraints ensure that the total nutrition from the purchased foods meets or exceeds the daily nutritional requirements.
- Non-negativity constraints are added to ensure that the quantity of foods purchased is non-negative.

This mathematical model can be solved using linear programming solvers to determine the optimal quantity of each food to purchase so that the total cost is minimized while meeting all the nutritional demands.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Problem Formulation}

\subsection*{Decision Variables}
Let \( \text{quantity}_k \) be the quantity of food \( k \) to purchase (for \( k = 1, \ldots, K \)).

\subsection*{Objective Function}
Minimize the total cost of purchasing foods:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
To satisfy the nutritional requirements, the following constraints must hold for each nutrient \( m \) (for \( m = 1, \ldots, M \)):

\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m
\]

\subsection*{Non-negativity Constraints}

\[
\text{quantity}_k \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

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

#### Define problem
problem = pulp.LpProblem("Food_Optimization", pulp.LpMinimize)

#### Decision variables
K = len(data['price'])  #### Number of food items
quantity = [pulp.LpVariable(f'quantity_{k+1}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

#### Constraints
M = len(data['demand'])  #### Number of nutrients
for m in range(M):
    problem += (
        pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m],
        f"Nutrient_Requirement_{m+1}"
    )

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

