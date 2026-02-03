
import pandas as pd
import json
import re
from bs4 import BeautifulSoup
def convert_with_pandas(csv_file_path, json_file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    print(df)
    # Convert the DataFrame to JSON format and save to file
    # orient='records' ensures the output is a list of JSON objects (one per row)
    df.to_json(json_file_path, orient='records', indent=4)

    print(f"CSV to JSON conversion completed with pandas! Output saved to {json_file_path}")



# STAT_REGEX = re.compile(r"\[(\d+)-(\d+)-(\d+)\]")

# def extract_ingredients(html_path):
#     with open(html_path, "r", encoding="utf-8") as f:
#         soup = BeautifulSoup(f, "html.parser")

#     ingredients = []

#     # buttons = soup.find_all("button", class_="ingredient-button")
#     buttons = soup.find_all("button", class_="attribute-name")
    
#     print(buttons)
#     for button in buttons:
#         name = button.get("data-ingredient")
#         rarity = button.get("data-rarity")

#         if not name or not rarity:
#             continue

#         text = button.get_text(strip=True)
#         match = STAT_REGEX.search(text)

#         if not match:
#             continue

#         combat, utility, whimsy = map(int, match.groups())

#         ingredients.append({
#             "ingredient": name,
#             "rarity": rarity,
#             "combat": combat,
#             "utility": utility,
#             "whimsy": whimsy
#         })

#     return ingredients

STAT_REGEX = re.compile(r"\[(\d+)-(\d+)-(\d+)\]")

def extract_ingredients(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    ingredients = []

    # 1. Target the actual button class from your snippet
    buttons = soup.find_all("button", class_="ingredient-button")
    
    for button in buttons:
        # 2. Extract attributes safely
        name = button.get("data-ingredient")
        rarity = button.get("data-rarity")

        if not name or not rarity:
            continue

        # 3. Get the text. If the numbers are inside the button, .get_text() works.
        # If the numbers are just AFTER the button, we use .next_sibling
        text = button.get_text(strip=True)
        if not STAT_REGEX.search(text):
            # Check the text immediately following the button if not found inside
            next_text = button.find_next_sibling(string=True)
            text = next_text.strip() if next_text else ""

        match = STAT_REGEX.search(text)

        if match:
            combat, utility, whimsy = map(int, match.groups())
            ingredients.append({
                "ingredient": name,
                "rarity": rarity,
                "combat": combat,
                "utility": utility,
                "whimsy": whimsy
            })

    return ingredients




if __name__ == "__main__":
    html = "ingredients2.html"
    json_file = "ingredients.json"
    # with open(html, "r", encoding="utf-8") as f:
    #     soup = BeautifulSoup(f, "html.parser")
    ings = extract_ingredients(html)
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(ings, f, indent=4, ensure_ascii=False)
    # d = soup.find('string', 'Amber')
    # print(d)


    # print(soup.b)
    # for string in soup.stripped_strings:
    #     if string == 'Amber':
    #         print(string)
    # print(d)
    # content = d.get_text()
    # print(content)
    # print(soup.find_all('a', class_="attribute-value"))
    # print(soup.contents)
    
    # data = extract_ingredients(html)
    # with open(json_file, "w", encoding="utf-8") as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)
    # print(f"Extracted {len(data)} ingredients → {json_file}")
    # Call the function with your file paths
    # convert_with_pandas('potions.csv', 'potions.json')