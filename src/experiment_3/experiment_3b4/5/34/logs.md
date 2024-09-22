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
To solve this problem, we need to create a linear programming model that minimizes the total cost of purchasing foods while meeting the nutritional requirements. Let's denote:

- \( K \): Number of different foods available
- \( M \): Number of different nutrients

Given:
- \( \text{price}_k \): Price per unit of food \( k \)
- \( \text{demand}_m \): Minimum required units of nutrient \( m \) per day
- \( \text{nutri}_{k, m} \): Units of nutrient \( m \) present in one unit of food \( k \)

Our objective is to determine the quantity \( \text{quantity}_k \) of each food \( k \) to purchase, such that the cost is minimized and the nutritional demands are satisfied.

Below is the mathematical model in \(\LaTeX\) format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total cost of purchasing foods:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\textbf{Subject to:}

- Nutritional requirements for each nutrient \( m \):

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m, \quad \forall m = 1, \ldots, M
\]

- Non-negativity constraint:

\[
\text{quantity}_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}
```

In this model:
- The objective function \( Z \) is the total cost that we aim to minimize.
- The constraints ensure that the total nutrition from all foods meets or exceeds the daily demand for each nutrient.
- The non-negativity constraints ensure that the food quantities are non-negative.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total cost of purchasing foods:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\textbf{Subject to:}

- Nutritional requirements for each nutrient \( m \):

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m, \quad \forall m = 1, \ldots, M
\]

- Non-negativity constraint:

\[
\text{quantity}_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

#### Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

#### Initialize the problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

#### Decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

#### Objective function: Minimize the total cost
problem += pulp.lpSum(data['price'][k] * quantities[k] for k in range(K)), "Total Cost"

#### Nutritional constraints
for m in range(M):
    problem += (pulp.lpSum(data['nutrition'][k][m] * quantities[k] for k in range(K)) 
                >= data['demand'][m], f'Nutrient_{m}_Requirement')

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

