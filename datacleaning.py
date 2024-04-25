import re
import pandas as pd
from nltk.corpus import stopwords

ingredient_units = {'inch', 'ml', 'milliliter','milliliters','liters','teaspoons', 'l','liter','teaspoon','t','tsp','tablespoon','tablespoons','tbl','tbs','tbsp','ounce','oz','fl','cup','cups','c','pint','pints','pt','p','quart','quarts','qt','gal','gals','gallon','gallons','g','mg','milligram','milligrams','gram','grams','pound','pounds','lb','lbs','c','f'}
stop_words = set(stopwords.words("english"))
stop_words = stop_words.union(ingredient_units)

def masktext(text, mask):
    mask_list = mask.split()
    masked_words = [word for word in text.split() if word not in mask_list]
    return " ".join(masked_words)

# ar_data['clean_instructions_masked'] = ar_data.apply(lambda l: masktext(l['clean_instructions'], l['clean_ingredients']), axis=1)



def clean_recipedata(filename: str, n = 5000): 
    data = pd.read_json(filename)
    data = data.T
    data.dropna(inplace=True)
    data = data.sample(n=n, random_state=2024)
    data['ingredients'] = data['ingredients'].apply(lambda L: " ".join(L))

    data['clean_ingredients'] = data['ingredients'].replace(r'[^a-zA-Z\s]', '', regex=True)
    data['clean_ingredients'] = data['clean_ingredients'].replace('ADVERTISEMENT', '', regex=True)
    data['clean_ingredients'] = data['clean_ingredients'].str.lower()

    data['clean_instructions'] = data['instructions'].replace(r'[^a-zA-Z\s]', '', regex=True)
    data['clean_instructions'] = data['clean_instructions'].replace(r'\n', ' ', regex=True)
    data['clean_instructions'] = data['clean_instructions'].str.lower()

    data['clean_instructions'] = data.apply(lambda l: masktext(l['clean_instructions'], " ".join(stop_words)), axis=1)
    data['clean_ingredients'] = data.apply(lambda l: masktext(l['clean_ingredients'], " ".join(stop_words)), axis=1)

    data['clean_instructions'] = data.apply(lambda l: masktext(l['clean_instructions'], l['title']), axis=1)
    data['clean_ingredients'] = data.apply(lambda l: masktext(l['clean_ingredients'], l['title']), axis=1)

    data['clean_instructions_masked'] = data.apply(lambda l: masktext(l['clean_instructions'], l['clean_ingredients']), axis=1)

    return data




def filter_stop_words(words):
    output = list()
    for word in words:
        if word.casefold() not in stop_words:
            output.append(word)
    return(output)

# data["instruction_words"] = data["instruction_words"].apply(filter_stop_words)
# data["ingredient_words"] = data["ingredient_words"].apply(filter_stop_words)
# data['index'] = data.index
# data.to_csv("data_small.csv")




from ast import literal_eval

def data_for_nodes(nodes: set):
    data = pd.read_csv("data_small.csv", converters={"ingredient_words": literal_eval,"instruction_words": literal_eval})
    data = data.rename(columns={"Unnamed: 0":"Id"})
    output = pd.DataFrame([rec for rec in nodes]).rename(columns={0: "Id"}).set_index('Id').join(data.set_index('Id'))
    return output