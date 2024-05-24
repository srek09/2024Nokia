import re

matrices = {}
operations = []
operators = {"+": 1, "-": 1, "*": 2, "/": 2, "%":2, "^": 3}  #order of operations

def add(A, B):
	return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

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

			while line != 'operations':
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


def shunting_yard(expression: str):
	output_queue = []
	operator_stack = [] 

	for token in expression.replace(" ", ""):

		if token in operators:
			while (operator_stack and operators[token] <= operators[operator_stack[-1]]):
				output_queue.append(operator_stack.pop())
			operator_stack.append(token)

		else:
			output_queue.append(token)

	output_queue += operator_stack[::-1]

	return output_queue


def evaluate_postfix(expression):
	stack = []
	for token in expression:
		if token in operators:
			operand2 = stack.pop()
			operand1 = stack.pop()
			result = token == "+" and add(operand1, operand2) or multiply(operand1, operand2)
			stack.append(result)
		else:
			stack.append(matrices[token])

	return stack and stack.pop() or ''


for operation in operations:
	result = evaluate_postfix(shunting_yard(operation))
	print(operation)
	for i in result:
		print(' '.join(map(str, i)))
	print()