# Started 26/05/20
# https://discord.com/api/oauth2/authorize?client_id=714829362570068068&permissions=76800&scope=bot

import csv
import random
import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def read_questions():
	questions_list = []
	with open("questions.csv", "r") as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for line in csv_reader:
			questions_list.append(line)
	random.shuffle(questions_list)
	return questions_list


def get_question(question_number, questions_list):
	question_dict = questions_list[question_number]
	question = question_dict["Question"]
	choices_list = question_dict["Choices"].split(";;;")
	correct_answer_index = question_dict["Correct Answer Index"]
	correct_answer = choices_list[int(correct_answer_index)]

	return question, choices_list, correct_answer


client = discord.Client()
quizNumber = 0
current_answer = None
questions = read_questions()


async def finish_quiz(channel):
	await channel.send("Thanks for playing!")


async def start_game(channel):
	global quizNumber
	global current_answer
	quizNumber, current_answer = 0, None

	await channel.send("Starting quiz!")


async def load_question(channel):
	global quizNumber
	global current_answer

	try:
		question_tuple = get_question(quizNumber, questions)
	except IndexError:  # no more questions
		await finish_quiz(channel)  # end game
	else:
		await channel.send(question_tuple[0])  # send the question
		choices = ""
		for answer_choice in question_tuple[1]:
			choices += answer_choice + "\n"
			#  await channel.send(answer_choice) #send answer choice one by ne
		await channel.send(choices)
		current_answer = question_tuple[2]  # set the current answer the bot is waiting for


@client.event
async def on_message(message):
	global quizNumber
	global current_answer
	if message.author == client.user:
		return

	if message.content.startswith("!quiz"):
		await start_game(message.channel)
		await load_question(message.channel)

	elif message.content.startswith(current_answer[:2]):  # user does not have to enter full answer, only A), B), etc.
		await message.channel.send("Correct!")
		quizNumber += 1
		await load_question(message.channel)

	elif len(message.content) == 2 and message.content[1] == ")":
		await message.channel.send("Incorrect!")

	elif message.content.startswith("!quit"):
		await finish_quiz(message.channel)

client.run(TOKEN)

# TODO Add a scoring system, deduct points for each wrong attempt
