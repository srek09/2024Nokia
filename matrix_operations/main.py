matrices = {} # read from input file
operations = [] # read from input file
operators = {'+': 1, '*': 2} #operators allowed

# matrix addition
# we go through each element of the matrix and add the corresponding elements of the two matrices
def add(A, B):
	return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


# matrix multiplication
# we go through each element of the matrix and multiply the corresponding (col = row, row = col) elements of the two matrices
def multiply(A, B):
	return [[sum (A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))] for i in range(len(A))]

with open('./input.txt', 'r') as f:
	input = f.readlines()
	current_line = 0

	while current_line < len(input):
		line = input[current_line].strip()

		if line == 'matrices':
			current_line += 2
			line = input[current_line].strip()

			while line != 'operations': # read all matrices
				id = line
				current_line += 1
				line = input[current_line].strip()
				matrix = []


				while len(line) > 0 and line[0].isdigit():
					matrix.append([int(num) for num in line.split()])
					current_line += 1
					line = input[current_line].strip()


				matrices[id] = matrix
				current_line += 1
				line = input[current_line].strip()
    
			current_line += 2

		operations.append(input[current_line].strip())
		current_line += 1


# Shunting Yard Algorithm
# we convert the infix expression to postfix
# we use a stack to store the operators and a queue to store the operands
# we go through each token in the expression and check if it is an operator or an operand
# if it is an operator we check if it has higher precedence than the operator on top of the stack
# if it has higher precedence we add it to the stack
# if it has lower precedence we pop the operator from the stack and add it to the queue
# if it is an operand we add it to the queue
# we add the remaining operators from the stack to the queue
# we evaluate the postfix expression

def shunting_yard(expression):
	output_queue = []
	operator_stack = [] 

	for token in expression.replace(' ', ''):
		if token in operators:
			while (operator_stack and operators[token] <= operators[operator_stack[-1]]):
				output_queue.append(operator_stack.pop())
			operator_stack.append(token)

		else:
			output_queue.append(token)

	output_queue += operator_stack[::-1]

	return output_queue


# here we calculate the result of the postfix expression
def evaluate_postfix(expression):
	stack = []
	for token in expression:
		if token in operators:
			operand2 = stack.pop()
			operand1 = stack.pop()
			result = token == '+' and add(operand1, operand2) or multiply(operand1, operand2)
			stack.append(result)
		else:
			stack.append(matrices[token])

	return stack and stack.pop() or ''


# evaluating and printing the results
for operation in operations:
	result = evaluate_postfix(shunting_yard(operation))
	print(operation, '\n'.join([' '.join(str(j) for j in i) for i in result]), sep='\n', end='\n\n')
