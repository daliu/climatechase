import time
import json
import random
from flask import Flask, request, json
app = Flask(__name__)

# Wind, solar, nuclear, fossil
input_to_ghg_map = {
            "nuclear": -0.05,
            "solar": -0.03,
            "wind": -0.02,
            "fossil": .4}

# Possible Disasters and Probability of Occurance
disasters = {
    'sea_levels': .01,
    'electricity_prices': .05,
    'crop_shortage': .1,
    'armed_conflict': .22,
    'hurricane': .65
}

disaster_cost = {
    'sea_levels': .2,
    'electricity_prices': .05,
    'crop_shortage': .1,
    'armed_conflict': .01,
    'hurricane': .3
}

jsonObject = {
        'Start_Year': 2017,
        'Budget': 100.0,
        'GHG': 10000.0,
        'GDP': 100.0,
        'Curr_Year': 2017,
        'solar': 0,
        'wind': 0,
        'nuclear': 0,
        'fossil': 0,
        'GDP_Growth': 1.01,

        'Sea_Levels': 0,
        'Electricity_Price': 0,
        'Agriculture': 0,
        'Hurricanes_Happen': False,
        'AC_Happen': False,

        'Win': False,
        'Game_Over': False

    }

#########################################################
# Processing & Trigger Functions
#########################################################

    # 1) add money to wind investment
    # 2) Calculate probability of certain action due to wind investment (above/below threshold)
    #     a) Probability of something good happening increases the more wind investment we have
    #     b) Probability of something bad happening increases the longer the game runs (unless we invested properly)
    # 3) Return that something happens

def have_lost():
    return jsonObject['Game_Over'] or jsonObject['GDP'] < 0 or jsonObject['Budget'] < 0 or jsonObject['GHG'] > 1000000

def have_won():
    return jsonObject['GHG'] < 100

def update_year():
    jsonObject['Curr_Year'] += 1
    return jsonObject

def update_ghg(input_to_ghg_map):
    solar_benefit = jsonObject['solar'] * input_to_ghg_map['solar']
    wind_benefit = jsonObject['wind'] * input_to_ghg_map['wind']
    nuclear_benefit = jsonObject['nuclear'] * input_to_ghg_map['nuclear']
    fossil_benefit = jsonObject['fossil'] * input_to_ghg_map['fossil']
    energy_investments = solar_benefit + wind_benefit + nuclear_benefit + fossil_benefit
    jsonObject['GHG'] *= (1.002 + energy_investments)
    return jsonObject

def update_budget(investment = ''):
    global disasters
    # Lose money for disasters
    for disaster, probability in [tup for tup in disasters.items()]:
        if random.random() > probability / 3:
            jsonObject['Budget'] -= jsonObject['Budget'] * disaster_cost[disaster]
            print(disaster + " has occured.")

    # Transfer $$$ to investment
    if investment in jsonObject:
        amount_invested = jsonObject['Budget'] / 10.0
        jsonObject[investment] += amount_invested
        jsonObject['Budget'] -= input_to_ghg_map[investment] * amount_invested
        jsonObject['Budget'] += input_to_ghg_map[investment] * amount_invested
        print("Amount invested in " + investment + ": " + str(amount_invested))

    jsonObject['GDP'] += (jsonObject['GDP_Growth'] + random.uniform(-.05, .0)) / 2
    jsonObject['Budget'] += jsonObject['GDP'] / 100
    jsonObject['Budget']
    return jsonObject

def update_game(investment = ''):
    global jsonObject
    if have_won():
        jsonObject['Game_Over'] = True
        print("You have successfully avoided global warming!")
        jsonObject['Win'] = True
        return jsonObject
    if have_lost():
        jsonObject['Game_Over'] = True
        print("Global Warming has overtaken the world. Humanity cannot continue.")
        return jsonObject

    update_year()
    update_ghg(input_to_ghg_map)
    update_budget(investment)
    return jsonObject

#########################################################
# Routes
#########################################################

@app.route("/")
def home():
    global jsonObject
    if not jsonObject['Game_Over']:
        update_game()
    return json.dumps(jsonObject)

@app.route('/instructions/')
def instructions():
    return json.dumps(jsonObject)

@app.route('/about/')
def about():
    return json.dumps(jsonObject)

@app.route('/play/')
def play():
    return json.dumps(jsonObject)

@app.route('/give_data/', methods=['GET'])
def give_data():
    if request.method == 'GET':
        return str([jsonObject])

@app.route('/receive_data/', methods=['POST'])
def receive_data():
    global jsonObject
    if request.method == 'POST':
        jsonObject = request.get_json()
        return "Successfully gotten Front-End code."

@app.route('/lose/', methods=['GET'])
def lose():
    global jsonObject
    jsonObject['Budget'] -= 1000000000000
    jsonObject['Game_Over'] = True
    return json.dumps(jsonObject)

@app.route('/win/', methods=['GET'])
def win():
    global jsonObject
    jsonObject['Budget'] += 1
    jsonObject['Game_Over'] = False
    return json.dumps(jsonObject)


#########################################################
# Button Routes
#########################################################

@app.route('/wind/', methods=['POST'])
def wind():
    if request.method == 'POST':
        global jsonObject
        jsonObject = request.get_json()
        update_game('wind')
        return json.dumps(jsonObject)

@app.route('/nuclear/', methods=['POST'])
def nuclear():
    if request.method == 'POST':
        global jsonObject
        jsonObject = request.get_json()
        update_game('nuclear')
        return json.dumps(jsonObject)

@app.route('/solar/', methods=['POST'])
def solar():
    if request.method == 'POST':
        global jsonObject
        jsonObject = request.get_json()
        update_game('solar')
        return json.dumps(jsonObject)

@app.route('/fossil/', methods=['POST'])
def fossil():
    if request.method == 'POST':
        global jsonObject
        jsonObject = request.get_json()
        update_game('fossil')
        return json.dumps(jsonObject)

if __name__ == "__main__":
    app.run(debug=True)

