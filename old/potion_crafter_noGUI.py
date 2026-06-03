import pandas as pd
import numpy as np
from collections import Counter
import jmespath
import time
import duckdb

def calculate_ingredients(ins, pots):

    # Clean inputs: remove empty/default selections
    ins_list = [x for x in ins if isinstance(x, str) and x.strip() and x != 'Select an Ingredient']
    if len(ins_list) != 3:
        return "Please provide 3 ingredients"

    mask = (
    pots[['i1_name', 'i2_name', 'i3_name']]
        .apply(set, axis=1)
        .eq({ins[0], ins[1], ins[2]})
    )

    res = pots.loc[mask, 'list_of_potions']
    if res.empty:
        return "No potion found"
    else:
        return res.iloc[0]

if __name__ == "__main__":
    # opt = StringVar(value="Amber")
    pots = pd.read_json('potions.json')
    p2 = pd.read_csv('potions.csv')
    ins = ['Boom Beri', 'Brush Reed', 'Starstone']
    ingredients = pd.read_json('ingredients.json')
    
    l = ingredients['ingredient'].unique().tolist()
    # # pot = calc_csv(ins, p2)
    # print(pot)
    pot = calculate_ingredients(ins, pots)
    print(pot)