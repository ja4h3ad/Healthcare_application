from bs4 import BeautifulSoup
import requests

url = 'https://mdbarrows.com/procedures/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the relevant content
faqs = soup.find_all('div', class_='faq-question-answer')
for faq in faqs:
    question = faq.find('p', class_='question').text
    answer = faq.find('p', class_='answer').text
    print(question, answer)


if __name__ == "__main__":
    main()
