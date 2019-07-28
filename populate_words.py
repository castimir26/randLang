import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'random_language.settings')

import django
django.setup()

from randLang.models import Dict_Words

word_file = open("1-1000.txt")

def populate():

  words = []
  word_list = []
  word_dict = {}
  x = 0
  for word in word_file:
    word_list.append(word.rstrip())
  for word in range(0, len(word_list)):
    x += 1
    word_dict = {
        "word": word_list[word]
    }
    words.append(word_dict)
  for word in words:
      c = add_word(word)

# Print out what we have added to the user.
  for c in Dict_Words.objects.all():
      print("- {0} ".format(str(c)))

def add_word(word):
  c = Dict_Words.objects.get_or_create(word = word)[0]
  print(type(c))
  c.save()
  return c

# Start execution here!
if __name__ == '__main__':
  print("Starting randLang population script...")
populate()
