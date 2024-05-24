import re
pattern = re.compile('[\W_]+')
with open('./input.txt', 'r', encoding='utf-8') as f:
  input = f.readlines()
counter = 0
for line in input:
  line = re.sub(pattern, '', line).lower().strip()
  unique_chars = len(set(line))
  p1 = 0
  p2 = len(line) - 1
  is_palindrome = True
  while p1 <= p2:
    if line[p1] != line[p2]:
      is_palindrome = False
      unique_chars = -1
      break
    p1 += 1
    p2 -= 1
  counter += 1
  print(f"{counter}. {is_palindrome and 'YES' or 'NO'}, {unique_chars}")
