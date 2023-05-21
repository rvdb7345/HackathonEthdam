"""
File to turn the output from the article selection to nice markdown.
"""

import json
import re

pattern = r"[^\w\s]"  # Matches any non-alphanumeric and non-whitespace character


def article_json_to_markdown(all_articles):
    # Clear output text file
    with open("final_article.txt", "w") as file:
        pass

    for article in all_articles:
        # Open a file in write mode
        with open("final_article.txt", "a") as file:
            # Clean out stupid characters
            article_title = re.sub(pattern, "", article["title"])
            title_string = "##### {}[".format(article_title)
            for id, link in enumerate(article["hyperlink"]):
                title_string += "[{}]({}),".format(id, link)

            article_keywords = re.sub(pattern, "", str(article["keywords"]))

            # Write content to the file
            file.write(title_string[:-1] + "]\n")
            file.write("* " + article_keywords + "* \n")
            file.write(article["content"] + "\n")
