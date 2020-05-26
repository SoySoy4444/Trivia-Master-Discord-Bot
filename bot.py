#Started 26/05/20

import csv
import random

questions = []
with open("questions.csv", "r") as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for line in csv_reader:
		questions.append(line)
random.shuffle(questions)

for questionDict in questions:
	question = questionDict["Question"]
	choicesList = questionDict["Choices"].split(" - ")
	correctAnswerIndex = questionDict["Correct Answer Index"]
	correctAnswer = choicesList[int(correctAnswerIndex)]

	print(question, choicesList, correctAnswer)