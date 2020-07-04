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

    def __init__(self, field_type: typing.Type[typing.Any]):
        pass


class Article:
	"""The `Article` class you need to write for the qualifier."""

	def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
		self.title = title
		self.author = author
		self.publication_date = publication_date
		self.content = content

	def __repr__(self):
		return f"<Article title=\"{self.title}\" " + f"author='{self.author}' " + f"publication_date='{self.publication_date.isoformat()}'>"

	def __len__(self):
		return len(self.content)	

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

# For debug
# if __name__ == "__main__":
# 	title = 'THIS IS TITLE'
# 	author = 'IQRAR'
# 	publication_date = datetime.datetime(1837, 4, 7, 12, 15, 0)
# 	content = "The requirements listed in this section only apply to the Article class. Please make sure the changes you make for the requirements this section don't break any of the requirements listed in the previous section."

# 	article = Article(title, author, publication_date, content)
# 	print(repr(article))
# 	print(article.content)
# 	print(len(article))
# 	print(article.short_introduction(n_characters=8))
# 	print(len(article.short_introduction(n_characters=8)))
# 	print(article.most_common_words(6))

