#Started 26/05/20
#https://discord.com/api/oauth2/authorize?client_id=714829362570068068&permissions=76800&scope=bot

import csv
import random
import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

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

client.run(TOKEN)