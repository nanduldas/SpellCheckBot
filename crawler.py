import requests
from bs4 import BeautifulSoup
from enchant.checker import SpellChecker

# Set up the spell checker
spell_checker = SpellChecker("en_US")

# Fetch repositories using GitHub API
url = "https://api.github.com/search/repositories"
query = "language:python"
params = {
    "q": query,
    "sort": "stars",
    "order": "desc"
}
response = requests.get(url, params=params)
repositories = response.json()

for repo in repositories["items"]:
    # Get the README file
    readme_url = repo["html_url"] + "/blob/master/README.md"
    readme_response = requests.get(readme_url)
    readme_html = readme_response.text

    # Parse the HTML and extract text
    soup = BeautifulSoup(readme_html, "html.parser")
    readme_text = soup.get_text()

    # Spell-check the text
    spell_checker.set_text(readme_text)
    for error in spell_checker:
        print(f"Spelling mistake in repository: {repo['name']}")
        print(f"Error: {error.word}")
        print(f"Suggestions: {error.suggest()}")
        print()

    spell_checker.reset()