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
```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}

\begin{document}

% Define the parameters and decision variables
\newcommand{\nmines}{n_{\text{mines}}}
\newcommand{\nmaxwork}{n_{\text{maxwork}}}
\newcommand{\royalty}{\text{royalty}}
\newcommand{\limit}{\text{limit}}
\newcommand{\quality}{\text{quality}}
\newcommand{\requiredquality}{\text{requiredquality}}
\newcommand{\price}{\text{price}}
\newcommand{\discount}{\text{discount}}
\newcommand{\isoperated}{\text{isoperated}}
\newcommand{\amount}{\text{amount}}

% Objective function: Maximize the total discounted profit
\begin{align*}
\text{Maximize:} \quad & \sum_{i=1}^{I} \left( \frac{\price}{(1 + \discount)^i} \sum_{k=1}^{K} \amount_{k,i} \right) - \sum_{i=1}^{I} \sum_{k=1}^{K} \frac{\royalty_k \cdot (1 - \isoperated_{k,i})}{(1 + \discount)^i}
\end{align*}

% Constraints
\text{Subject to:}
\begin{align*}
& \sum_{k=1}^{K} \isoperated_{k,i} \leq \nmaxwork, \quad \forall i = 1,\ldots,I \\
& \amount_{k,i} \leq \limit_k \cdot \isoperated_{k,i}, \quad \forall k = 1,\ldots,K, \forall i = 1,\ldots,I \\
& \sum_{k=1}^{K} \left( \amount_{k,i} \cdot \quality_k \right) = \requiredquality_i \sum_{k=1}^{K} \amount_{k,i}, \quad \forall i = 1,\ldots,I \\
& \isoperated_{k,i} \in \{0, 1\}, \quad \forall k = 1,\ldots,K, \forall i = 1,\ldots,I \\
& \amount_{k,i} \geq 0, \quad \forall k = 1,\ldots,K, \forall i = 1,\ldots,I
\end{align*}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}

\begin{document}

% Define the parameters and decision variables
\newcommand{\nmines}{n_{\text{mines}}}
\newcommand{\nmaxwork}{n_{\text{maxwork}}}
\newcommand{\royalty}{\text{royalty}}
\newcommand{\limit}{\text{limit}}
\newcommand{\quality}{\text{quality}}
\newcommand{\requiredquality}{\text{requiredquality}}
\newcommand{\price}{\text{price}}
\newcommand{\discount}{\text{discount}}
\newcommand{\isoperated}{\text{isoperated}}
\newcommand{\amount}{\text{amount}}

% Objective function: Maximize the total discounted profit
\begin{align*}
\text{Maximize:} \quad & \sum_{i=1}^{I} \left( \frac{\price}{(1 + \discount)^i} \sum_{k=1}^{K} \amount_{k,i} \right) - \sum_{i=1}^{I} \sum_{k=1}^{K} \frac{\royalty_k \cdot (1 - \isoperated_{k,i})}{(1 + \discount)^i}
\end{align*}

% Constraints
\text{Subject to:}
\begin{align*}
& \sum_{k=1}^{K} \isoperated_{k,i} \leq \nmaxwork, \quad \forall i = 1,\ldots,I \\
& \amount_{k,i} \leq \limit_k \cdot \isoperated_{k,i}, \quad \forall k = 1,\ldots,K, \forall i = 1,\ldots,I \\
& \sum_{k=1}^{K} \left( \amount_{k,i} \cdot \quality_k \right) = \requiredquality_i \sum_{k=1}^{K} \amount_{k,i}, \quad \forall i = 1,\ldots,I \\
& \isoperated_{k,i} \in \{0, 1\}, \quad \forall k = 1,\ldots,K, \forall i = 1,\ldots,I \\
& \amount_{k,i} \geq 0, \quad \forall k = 1,\ldots,K, \forall i = 1,\ldots,I
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

#### Indices
K = data['n_mines']
I = len(data['requiredquality'])

#### Create the LP problem
problem = pulp.LpProblem("Mining_Optimization", pulp.LpMaximize)

#### Decision variables
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(K) for i in range(I)), cat='Binary')

#### Objective function: Maximize the total discounted profit
objective = pulp.lpSum(
    (data['price'] / (1 + data['discount'])**i) * pulp.lpSum(amount[k, i] for k in range(K))
    - pulp.lpSum(data['royalty'][k] * (1 - isoperated[k, i]) / (1 + data['discount'])**i for k in range(K))
    for i in range(I)
)
problem += objective

#### Constraints

#### Maximum number of mines operated at the same time
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(K)) <= data['n_maxwork']

#### Amount extracted cannot exceed limit if not operated
for k in range(K):
    for i in range(I):
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i]

#### Blend quality requirement
for i in range(I):
    total_amount = pulp.lpSum(amount[k, i] for k in range(K))
    problem += pulp.lpSum(amount[k, i] * data['quality'][k] for k in range(K)) == data['requiredquality'][i] * total_amount

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


