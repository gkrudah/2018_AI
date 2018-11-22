from konlpy.tag import Okt
import math
from collections import Counter
import time

list_pos = Counter()
list_neg = Counter()
num_pos = 0
num_neg = 0
total_word = 0
test = []
result = []


#training by test data
def train():
	global list_pos, list_neg, num_pos, num_neg, total_word
	okt = Okt()

	f = open("ratings_train.txt", 'r', encoding="utf8")
	#f = open("ratings_train1.txt", 'r')
	line = f.readline()

	for line in f:
		line = line.rstrip('\n')
		split_line = line.split('\t')

		if split_line[2] == '1':
			for word in okt.pos(split_line[1]):
				list_pos[word[0]] += 1
				num_pos += 1
		elif split_line[2] == '0':
			for word in okt.pos(split_line[1]):
				list_neg[word[0]] += 1
				num_neg += 1

	total_word = len(list_pos) + len(list_neg)

	f.close()


#classify test data's label by training data
def classify():
	global test, result

	f = open("ratings_test.txt", 'r', encoding="utf8")
	#f = open("ratings_valid1.txt", 'r')
	line = f.readline()

	for line in f:
		line = line.rstrip('\n')
		line = line.split('\t')
		test.append(line)

	for line in test:
		feel = NB_classifier(line[1])
		result.append(line[0] + '\t' + line[1] + '\t' + str(feel) + '\n')

	f.close()


#naive bayes model
def NB_classifier(string):
	global list_pos, list_neg, num_pos, num_neg, total_word
	pos_prob = 0
	neg_prob = 0
	okt = Okt()

	for word in okt.pos(string):
		pos_cnt = list_pos[word[0]]
		neg_cnt = list_neg[word[0]]

		pos_prob += math.log((pos_cnt + 1)/(num_pos + total_word))
		neg_prob += math.log((neg_cnt + 1)/(num_neg + total_word))

	#2 sentences below are option
	pos_prob += math.log(num_pos/(num_pos + num_neg))
	neg_prob += math.log(num_neg/(num_pos + num_neg))

	if pos_prob > neg_prob:
		return 1
	else:
		return 0


#file write the result of classified test data
def write_result():
	global result

	f = open("ratings_result.txt", 'w')
	f.write("id\tdocument\tlabel\n")

	for line in result:
		f.write(line)

	f.close()


#this function is made for test accuracy
#checking accuracy by test valid data
def accuracy():
	global test, result
	tmp = []
	accurate = 0

	for i in range(len(test)):
		tmp = result[i].rstrip('\n').split('\t')
		test_var = int(tmp[2])

		if int(test[i][2]) == test_var:
			accurate += 1

	return (accurate / len(test)) * 100


def main():
	duration = time.time()
	train()
	print(("finish train %s") % (time.time() - duration))
	classify()
	print(("finish classify %s") % (time.time() - duration))
	write_result()
	print(("finish write_result %s") % (time.time() - duration))
	#accr = accuracy() # for valid text
	#print("accuracy %f percent" % accr)
	#print(("finish accuracy %s") % (time.time() - duration))


if __name__ == "__main__":
	main()
