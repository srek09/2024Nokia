import re
del_chars = ''.join(c for c in map(chr, range(8212)) if not c.isalnum())
del_map = str.maketrans('', '', del_chars)


with open('./input.txt', 'r', encoding='utf-8') as f:
	input = f.readlines()

for line in input:
	line = line.translate(del_map).lower().strip()
	unique_chars = len(set(line)) # Count unique characters
	# This part of the code is checking whether the given `line` is a palindrome. Here's a breakdown of
	# what each step does:
	# I use a two-pointer approach to check if the string is a palindrome. (p1 --> from the beginning of the string, p2 --> from the end of the string)
	p1 = 0
	p2 = len(line) - 1
	is_palindrome = 'YES'

	while p1 <= p2:
		# I compare the characters at the two pointers. If they are not equal, the given string is not a palindrome therefore I can stop and move on to the next one.
		if line[p1] != line[p2]:
			is_palindrome = 'NO'
			unique_chars = -1
			break

		# If the characters are equal, I increment p1 and decrement p2 to check the next pair of characters until the 2 pointers meet.
		p1 += 1
		p2 -= 1

	print(f"{is_palindrome}, {unique_chars}")
