# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A mining company is going to continue operating in a certain area for the next years. 
- There are \var{n_mines} mines in this area, but it can operate at most \var{n_maxwork} in any one year. 
- Although a mine may not operate in a certain year, it is still necessary to keep it ‘open’, in the sense that royalties are payable, if it be operated in a future year. 
- Clearly, if a mine is not going to be worked again, it can be permanently closed down and no more royalties need be paid. 
- The yearly royalties payable on each mine kept ‘open’ is \var{royalty_{k}} for mine \var{k}.
- There is an upper limit to the amount of ore, which can be extracted from each mine in a year. 
- The upper limit for mine \var{k} is \var{limit_{k}}.
- The ore from the different mines is of varying quality.
- This quality is measured on a scale so that blending ores together results in a linear combination of the quality measurements, for example, if equal quantities of two ores were combined, the resultant ore would have a quality measurement half way between
that of the ingredient ores. 
- The quality of ore from mine \var{k} is \var{quality_{k}}.
- In each year, it is necessary to combine the total outputs from each mine to produce a blended ore of exactly some stipulated quality.
- In year \var{i}, the required quality is \var{requiredquality_{i}}.
- The final blended ore sells for \var{price} ton each year. 
- Revenue and expenditure for future years must be discounted at a rate of \var{discount} per annum.

INPUT FORMAT:

{
    "n_mines": n_mines,
    "n_maxwork": n_maxwork,
    "royalty": [royalty_{k} for k in 1,...,K],
    "limit": [limit_{k} for k in 1,...,K],
    "quality": [quality_{k} for k in 1,...,K],
    "requiredquality": [requiredquality_{i} for i in 1,...,I],
    "price": price,
    "discount": discount
}


OBJECTIVE: To maximize profit, which mines should be operated each year and how much should they produce?

OUTPUT INFO:

- \var{isoperated} represents whether each mine is operated in each year
- \var{amount} represents the amount of ore produced by each mine in each year

OUTPUT FORMAT:

{
    "isoperated": [[isoperated_{k, i} for i in 1,...,I] for k in 1,...K]
    "amount": [[amount_{k, i} for i in 1,...,I] for k in 1,...K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate the given problem as a Mixed Integer Programming (MIP) problem, we need to define the decision variables, the objective function, and the constraints using the information provided.

Let's consider the following model:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Decision Variables:}

\begin{align*}
\text{isoperated}_{k,i} & \quad \text{Binary variable, 1 if mine } k \text{ is operated in year } i, 0 \text{ otherwise.} \\
\text{amount}_{k,i} & \quad \text{Amount of ore produced by mine } k \text{ in year } i.
\end{align*}

\textbf{Objective Function:}

The objective is to maximize the net present value of the profit over all years:

\[
\text{Maximize} \quad \sum_{i=1}^{I} \frac{1}{(1+\text{discount})^{i}} \left( \text{price} \cdot \sum_{k=1}^{K} \text{amount}_{k,i} - \sum_{k=1}^{K} \text{royalty}_k \cdot \text{isoperated}_{k,i} \right)
\]

\textbf{Constraints:}

1. **Capacity Constraints**: The amount produced by each mine cannot exceed its limit.
   \[
   \text{amount}_{k,i} \leq \text{limit}_k \cdot \text{isoperated}_{k,i} \quad \forall k = 1, \ldots, K, \, \forall i = 1, \ldots, I
   \]

2. **Quality Constraints**: The blended ore must meet the required quality each year.
   \[
   \frac{\sum_{k=1}^{K} \text{quality}_k \cdot \text{amount}_{k,i}}{\sum_{k=1}^{K} \text{amount}_{k,i}} = \text{requiredquality}_i \quad \forall i = 1, \ldots, I
   \]

3. **Maximum Mines Operated**: At most \text{n\_maxwork} mines can be operated each year.
   \[
   \sum_{k=1}^{K} \text{isoperated}_{k,i} \leq \text{n\_maxwork} \quad \forall i = 1, \ldots, I
   \]

\textbf{Variable Domains:}

\begin{align*}
\text{isoperated}_{k,i} & \in \{0, 1\} \quad \forall k = 1, \ldots, K, \, \forall i = 1, \ldots, I \\
\text{amount}_{k,i} & \geq 0 \quad \forall k = 1, \ldots, K, \, \forall i = 1, \ldots, I
\end{align*}

\end{document}
```

This model captures the key constraints and the objective to maximize the net present value of profits by determining which mines to operate and how much ore to extract from each, while considering operational constraints, quality requirements, and royalty costs.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Decision Variables:}

\begin{align*}
\text{isoperated}_{k,i} & \quad \text{Binary variable, 1 if mine } k \text{ is operated in year } i, 0 \text{ otherwise.} \\
\text{amount}_{k,i} & \quad \text{Amount of ore produced by mine } k \text{ in year } i.
\end{align*}

\textbf{Objective Function:}

The objective is to maximize the net present value of the profit over all years:

\[
\text{Maximize} \quad \sum_{i=1}^{I} \frac{1}{(1+\text{discount})^{i}} \left( \text{price} \cdot \sum_{k=1}^{K} \text{amount}_{k,i} - \sum_{k=1}^{K} \text{royalty}_k \cdot \text{isoperated}_{k,i} \right)
\]

\textbf{Constraints:}

1. **Capacity Constraints**: The amount produced by each mine cannot exceed its limit.
   \[
   \text{amount}_{k,i} \leq \text{limit}_k \cdot \text{isoperated}_{k,i} \quad \forall k = 1, \ldots, K, \, \forall i = 1, \ldots, I
   \]

2. **Quality Constraints**: The blended ore must meet the required quality each year.
   \[
   \frac{\sum_{k=1}^{K} \text{quality}_k \cdot \text{amount}_{k,i}}{\sum_{k=1}^{K} \text{amount}_{k,i}} = \text{requiredquality}_i \quad \forall i = 1, \ldots, I
   \]

3. **Maximum Mines Operated**: At most \text{n\_maxwork} mines can be operated each year.
   \[
   \sum_{k=1}^{K} \text{isoperated}_{k,i} \leq \text{n\_maxwork} \quad \forall i = 1, \ldots, I
   \]

\textbf{Variable Domains:}

\begin{align*}
\text{isoperated}_{k,i} & \in \{0, 1\} \quad \forall k = 1, \ldots, K, \, \forall i = 1, \ldots, I \\
\text{amount}_{k,i} & \geq 0 \quad \forall k = 1, \ldots, K, \, \forall i = 1, \ldots, I
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

#### Constants
K = data['n_mines']
I = len(data['requiredquality'])
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

#### Initialize the problem
problem = pulp.LpProblem("Maximize_NPV", pulp.LpMaximize)

#### Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(K) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

#### Objective Function
problem += pulp.lpSum((1/(1 + discount)**(i+1)) * (price * pulp.lpSum(amount[k, i] for k in range(K)) - pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(K))) for i in range(I))

#### Constraints
#### Capacity Constraints
for k in range(K):
    for i in range(I):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

#### Quality Constraints
for i in range(I):
    problem += pulp.lpSum(quality[k] * amount[k, i] for k in range(K)) >= requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(K)), f"QualityConstraint_{i}"

#### Maximum Mines Operated
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(K)) <= n_maxwork, f"MaxMinesOperated_{i}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

