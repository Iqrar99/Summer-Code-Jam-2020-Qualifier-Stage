"""
Solution by iqrar99#1556

Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import re
import typing


class ArticleField:
	"""The `ArticleField` class for the Advanced Requirements."""

	field_type: typing.Type[typing.Any] 

	def __init__(self, field_type: typing.Type[typing.Any]):
		self.field_type = field_type

	def __set_name__(self, owner, name):
		self.name = name

	def __set__(self, instance, value):
		if isinstance(value, self.field_type):
			instance.__dict__[self.name] = value
		
		else:
			err_msg1 = self.field_type.__name__
			err_msg2 = value.__class__.__name__
			raise TypeError(
				f"""expected an instance of type '{err_msg1}' for attribute '{self.name}', got '{err_msg2}' instead""")

	def __get__(self, instance, owner):
		return instance.__dict__.get(self.name)

	def __str__(self):
		return self.__data

class Article:
	"""The `Article` class you need to write for the qualifier."""
	
	id_now = 0
	last_edited = None
	
	title = ArticleField(field_type=str)
	author = ArticleField(field_type=str)
	publication_date = ArticleField(field_type=datetime.datetime)
	my_content = ArticleField(field_type=str)

	def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
		self.title = title
		self.author = author
		self.publication_date = publication_date
		self.my_content = content
		self.id = Article.id_now
		Article.id_now += 1

	def __repr__(self):
		return f"<Article title=\"{self.title}\" " + f"author='{self.author}' " + f"publication_date='{self.publication_date.isoformat()}'>"

	def __len__(self):
		return len(self.my_content)

	def __lt__(self, other: object):
		return self.publication_date < other.publication_date

	def __gt__(self, other: object):
		return self.publication_date > other.publication_date

	def __eq__(self, other: object):
		return self.publication_date == other.publication_date

	@property
	def content(self):
		return self.my_content

	@content.setter
	def content(self, new_content: str):
		self.my_content = new_content
		self.last_edited = datetime.datetime.now()

	def short_introduction(self, n_characters: int) -> str:
		if n_characters >= len(self.content):
			return self.content

		sliced_content = self.content[:n_characters]
		SEPARATOR = (' ', '\n')
		
		if not ((sliced_content[-1] not in SEPARATOR) and (self.content[n_characters] in SEPARATOR)):
			idx = 0

			# Find first newline or whitespace
			for i in range(len(sliced_content) - 1, -1, -1):
				if sliced_content[i] in SEPARATOR:
					idx = i
					break

			while (idx > 0) and (sliced_content[idx - 1] in SEPARATOR):
				idx -= 1

			sliced_content = sliced_content[:idx]

		return sliced_content

	def most_common_words(self, n: int) -> dict:
		if n <= 0:
			return {}

		text = re.split('[^a-zA-Z]', self.content.lower())

		word_counter = {}
		for word in text:
			if word == '':
				continue

			if word not in word_counter:
				word_counter[word] = 1
			else:
				word_counter[word] += 1

		# Sort word_counter descending
		words = list(word_counter.keys())
		value = list(word_counter.values())
		length = len(word_counter)

		for a in range(length - 1):
			for b in range(a + 1, length):
				if value[a] < value[b]:
					value[a], value[b] = value[b], value[a]
					words[a], words[b] = words[b], words[a]

				elif value[a] == value[b]:
					# Check for the first appearance
					for word in text:
						if word == words[b]:
							value[a], value[b] = value[b], value[a]
							words[a], words[b] = words[b], words[a]
							break
							
						elif word == words[a]:
							break

		if n <= len(words):
			words_target = words[:n]
			value_target = value[:n]

		else:
			words_target = words
			value_target = value

		return dict(zip(words_target, value_target))

