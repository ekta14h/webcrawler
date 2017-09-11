import requests
from bs4 import BeautifulSoup
import time

start_page = "https://en.wikipedia.org/wiki/Python_(programming_language)"
max_steps = 25

def continue_crawl(search_history, target_url, max_steps):
  """Checks for stopping criteria for target_url"""
  if search_history == []:
    return True
  if search_history[-1] == target_url:
    print("We've found the target article!")
    return False
  elif len(search_history) > max_steps:
    print("The search has gone on suspiciously long, aborting search!")
    return False
  elif len(set(search_history)) < len(search_history):
    print("We've arrived at an article we've already seen, aborting search!")
    return False
  else:
    return True

def fetch_next_url(url, search_history, all_text):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, "html5lib")
  all_text.append(soup.p)
  target_url = soup.p.a.get('href')
  print("target_url", target_url)
  return complete_url(target_url)

def complete_url(url):
  return "https://en.wikipedia.org" + url

if __name__ == '__main__':
  search_history = []
  all_text = []
  response = requests.get(start_page)
  # Now response.text has the html content of page, lets parse html by BeautifulSoup
  soup = BeautifulSoup(response.text, "html5lib")
  target_url = soup.p.a.get('href')
  target_url = complete_url(target_url)
  print("target_url", target_url)
  all_text.append(soup.p)

  while True:
    if continue_crawl(search_history, target_url, max_steps):
      print("sleeping for feq secs to not overload the server")
      time.sleep(2)
      target_url = fetch_next_url(target_url, search_history, all_text)
      search_history.append(target_url)

  # once crawler has stopped, lets save the text to file.
  with open("python_data.txt", "w") as fp:
    for line in all_text:
      fp.write(line + "\n")
  print("DONE Crawling!!")
