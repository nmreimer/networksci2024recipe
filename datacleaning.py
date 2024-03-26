import re
import pandas as pd

# ar_data = pd.read_json("recipes_raw_nosource_ar.json")
# ar_data = ar_data.T
# ar_data.dropna(inplace=True)
# ar_data['ingredients'] = ar_data['ingredients'].apply(lambda L: " ".join(L))

# ar_data['clean_ingredients'] = ar_data['ingredients'].replace(r'[^a-zA-Z\s]', '', regex=True)
# ar_data['clean_ingredients'] = ar_data['clean_ingredients'].replace('ADVERTISEMENT', '', regex=True)
# ar_data['clean_ingredients'] = ar_data['clean_ingredients'].str.lower()

# ar_data['clean_instructions'] = ar_data['instructions'].replace(r'[^a-zA-Z\s]', '', regex=True)
# ar_data['clean_instructions'] = ar_data['clean_instructions'].replace(r'\n', ' ', regex=True)
# ar_data['clean_instructions'] = ar_data['clean_instructions'].str.lower()

# def masktext(text, mask):
#     mask_list = mask.split()
#     masked_words = [word for word in text.split() if word not in mask_list]
#     return " ".join(masked_words)

# ar_data['clean_instructions_masked'] = ar_data.apply(lambda l: masktext(l['clean_instructions'], l['clean_ingredients']), axis=1)



def clean_recipedata(filename: str): 
    data = pd.read_json(filename)
    data = data.T
    data.dropna(inplace=True)
    data['ingredients'] = data['ingredients'].apply(lambda L: " ".join(L))

    data['clean_ingredients'] = data['ingredients'].replace(r'[^a-zA-Z\s]', '', regex=True)
    data['clean_ingredients'] = data['clean_ingredients'].replace('ADVERTISEMENT', '', regex=True)
    data['clean_ingredients'] = data['clean_ingredients'].str.lower()

    data['clean_instructions'] = data['instructions'].replace(r'[^a-zA-Z\s]', '', regex=True)
    data['clean_instructions'] = data['clean_instructions'].replace(r'\n', ' ', regex=True)
    data['clean_instructions'] = data['clean_instructions'].str.lower()

    data['clean_instructions_masked'] = data.apply(lambda l: masktext(l['clean_instructions'], l['clean_ingredients']), axis=1)

    return data
