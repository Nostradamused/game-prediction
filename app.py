import json
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from joblib import load


app = Flask(__name__)

# open the csv file
df = pd.read_csv('./data/games_full_infos.csv')
df = df.drop(columns=['release_date', 'price', 'positive', 'negative', 'app_id', 'min_owners', 'max_owners', 'hltb_single'])
rfc = load('filename.joblib')
games_pred_names = load('games_pred_names.joblib')

# The user give a category and the app return 5 random games from top 15 games of this category
@app.route("/games_proposition/<category>")
def games_proposition(category):
    sorted_df = df.sort_values(category, ascending=False)
    games = sorted_df['name'].head(15).sample(5).values.tolist()
    return games

@app.route("/category_to_games")
def game_proposition():
    # use category_to_game.html
    return render_template('category_to_games.html')


# Get all categories
@app.route("/categories")
def categories():
    return df.drop(columns=['name']).columns.tolist()


# The user give a list of 3 games and we return a list of games the user can like
# example: /games_prediction?games=game1,game2,game3
@app.route("/games_prediction_api")
def games_prediction_api():
    games_list = request.args.get('games')
    games = games_list.split('~')
    
    X = []
    for game in games:
        game_details = df[df['name'] == game].values.tolist()[0][1:]
        if len(X) == 0:
            X = game_details
        else:
            X = [(a+b)/2 for a, b in zip(X, game_details)]
    
    predictions = rfc.predict_proba([X])
    predictions = predictions[0]
    
    predicted_games = []
    indexes = []
    for i in range(10):
        max = 0
        index = 0
        for j in range(len(predictions)):
            if predictions[j] > max and j not in indexes and games_pred_names[j] not in games:
                max = predictions[j]
                index = j
        indexes.append(index)
        predicted_games.append([games_pred_names[index], max])
    
    
    total_percentage = sum([i[1] for i in predicted_games])
    
    resutlt ={
        "games": [i[0] for i in predicted_games],
        "predictions": [round(i[1]/total_percentage*100, 2) for i in predicted_games],
    }
    return json.dumps((resutlt))

@app.route("/games_prediction")
def games_prediction():
    return render_template('games_prediction.html')

@app.route("/all_games")
def all_games():
    return df['name'].values.tolist()


def get_game_categorys(game):
    categorys = df[df['name'] == game]
    # drop column name
    categorys = categorys.drop(columns=['name']).values.tolist()
    return categorys


def get_games_categorys(games):
    categorys = []
    for game in games:
        categorys.append(get_game_categorys(game))

    x = np.mean(categorys, axis=0)
    return x