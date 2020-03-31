import json
import re
import os
import numpy as np
import sys
                                                                          
def transform(direc,spl):
	names = ['train','dev']
	questions_list = ['q1', 'q2', 'q3', 'q4', 'q5']
	answer_list = [{'answer_start': 0, 'text': 'UNLABELEDDDD'}]
	total_data_train = []
	total_data_dev = []
	train_length = 0
	dev_length = 0

	# Loop through every file
	for filename in os.listdir(direc):
		with open(os.path.join(direc, filename), 'r') as f:
			src_dict = json.load(f)
			section_to_text_dict = {}

			# Get text for each section
			for paragraph in src_dict['body_text']:
				sectname = paragraph['section']
				graph = paragraph['text']

				# Process the text
				while graph[0] == " ":
					graph = graph[1:]

				# create spaces btwn words and punctuation
				graph = re.sub('([.,!?()])', r' \1 ', graph)
				graph = re.sub('\s{2,}', ' ', graph)

				# filter out citations
				# graph.split()
  
				if sectname not in section_to_text_dict:
					section_to_text_dict[sectname] = graph
				else:
					section_to_text_dict[sectname] += graph

			# Fir each question and section, create a data entry
			for sectname in section_to_text_dict:
				for qind in range(len(questions_list)):
					question = questions_list[qind]
					id = filename.split('.')[0] + '_' + sectname + '_' + str(qind)

					answer_object = {'answers': answer_list, 'question': question, 'id': id}
					paragraph_object = {'context': section_to_text_dict[sectname], 'qas': [answer_object]}

					if np.random.random() < spl:
						current = 'train'
						train_length += 1
						total_data_train.append({"title":"COVID","paragraphs":[paragraph_object]})
					else:
						current = 'dev'
						dev_length += 1
						total_data_dev.append({"title":"COVID","paragraphs":[paragraph_object]})

	# Save train and dev files
	total_data_train = {'data': total_data_train, 'version': '1.0', 'len': train_length}
	total_data_dev = {'data': total_data_dev, 'version': '1.0', 'len': dev_length}
	file_name_train = 'COVID_train.json'
	file_name_dev = 'COVID_dev.json'

	with open(os.path.join(direc, file_name_train), 'w') as f:
		json.dump(total_data_train, f)

	print(file_name_train + ' has been saved!')

	with open(os.path.join(direc, file_name_dev), 'w') as f:
		json.dump(total_data_dev, f)

	print(file_name_dev + ' has been saved!')

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Expected usage: python transformer.py <data repo>")
		sys.exit()
	data_repo = sys.argv[1]
	transform(data_repo, .5) 
