import random
import string

def inputChar():
	random_string = string.punctuation + string.ascii_lowercase + ' '
	random_char = list(random_string)
	return random.choice(random_char)

def inputString():
	random_num = random.choice((1,2))

	if (random_num == 1):
		return ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
	else:
		return ''.join(random.choice(string.ascii_lowercase) for _ in range(9))

def testme():
	tcCount = 0
	state = 0

	while(1):
		tcCount += 1
		c = inputChar()
		s = inputString()
		print("Iteration " + str(tcCount) + ": c = " + c + ", s = " + s + ", state = " + str(state))

		if (c == '[' and state == 0):
			state =1
		if (c == '(' and state == 1):
			state = 2
		if (c == '{' and state == 2):
			state = 3
		if (c == ' ' and state == 3):
			state = 4
		if (c == 'a' and state == 4):
			state = 5
		if (c == 'x' and state == 5):
			state = 6
		if (c == '}' and state == 6):
			state = 7
		if (c == ')' and state == 7):
			state = 8
		if (c == ']' and state == 8):
			state = 9

		if (s[0] == 'r' and s[1] == 'e' and s[2] == 's' and s[3] == 'e' and s[4] == 't' and state == 9):
			print("error ")
			break

def main():
	testme()





if __name__ == '__main__':
	main()