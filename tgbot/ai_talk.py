import random
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB



def filter_text(text):
    text = text.lower()
    text = text.strip()
    pattern = r"[^\w\s]"
    text = re.sub(pattern, "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def process_text(text):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text

#Карта намерений
INTENTS = {
        "hello": {
            "examples": ["Hello", "Hi", "Hey there", "Greetings", "Howdy"],
            "responses": ["Hey", "Hello there", "Greetings"],
        },
        "bye": {
            "examples": ["Goodbye", "See you later", "Farewell"],
            "responses": ["Have a great day", "Goodbye"],
        },
        "how_are_you": {
            "examples": ["How are you?", "How are you doing?", "What's new?", "How are you feeling?"],
            "responses": ["I'm functioning normally", "I'm good", "Alright"],
        },
        "weather": {
            "examples": ["How's the weather?", "What's the weather like?", "Is it stormy?"],
            "responses": ["The weather is fine today", "It's sunny here, how about there?", "I'm getting some glare in my eyes"],
        },
        "ship_position": {
            "examples": ["Where are we now?", "What's our position?", "Which point of the ocean are we in?"],
            "responses": ["We are at coordinates 45.6789° N, 23.4567° W", "Currently in the Pacific Ocean area"],
        },
        "sailors_code": {
            "examples": ["Do you know the rules of maritime journeys?", "What is the sailor's code?", "What's the rules?"],
            "responses": ["The sailor's code is a set of rules and obligations followed at sea to ensure safety and order"],
        },
        "sea_legs": {
            "examples": ["Do you have sea legs?", "How do you feel at sea?"],
            "responses": ["I've got sea legs", "I feel at home on the water"],
        },
        "ports_visited": {
            "examples": ["Which ports have we visited?", "How many ports have we docked at?"],
            "responses": ["We have visited 5 ports: London, New York, Tokyo, Sydney, Havana"],
        },
        "rum_supply": {
            "examples": ["What's the rum supply on board?", "Do we have any rum left?"],
            "responses": ["Rum supply is running low, time to restock", "We need to think about replenishing our rum supply"],
        },
        "pirate_encounter": {
            "examples": ["Have we encountered pirates?", "How to quickly sail away from pirates?"],
            "responses": ["No pirate encounters yet, but it's best to be prepared for such possibility", "Pirates are a serious threat, we need to stay vigilant"],
        },
        "seasickness_solution": {
            "examples": ["What to do if I feel seasick?", "How to overcome seasickness?"],
            "responses": ["Try eating some mint or taking a walk in the fresh air", "It's better to treat it beforehand than suffer later"],
        },
        "sailing_experience": {
            "examples": ["How long have you been at sea?", "What are the most interesting moments in your sailing experience?"],
            "responses": ["I've been at sea for a while now, and every day brings something new and amazing", "My sailing experience is rich with various adventures and encounters"],
        },
        "fishing_story": {
            "examples": ["Tell me about your catch", "Have you ever caught a big fish?"],
            "responses": ["Once I caught a shark the size of the boat!", "My record catch was a whale the size of a pie"],
        },"sailing_skills": {
            "examples": ["What sailing skills do you have?", "Have you navigated through rough waters?"],
            "responses": ["I am skilled in navigating through rough waters and handling various sailing tasks", "I have experience in handling sails and navigating in challenging conditions"],
        },
        "ship_repairs": {
            "examples": ["Have you helped with ship repairs?", "What's the most challenging repair you've done?"],
            "responses": ["I have assisted in ship repairs and maintenance tasks, including patching leaks and fixing sails", "The most challenging repair I've done was fixing a broken mast during a storm"],
        },
        "sea_creatures": {
            "examples": ["Have you encountered any sea creatures?", "Tell me about a memorable sea creature encounter"],
            "responses": ["I have seen dolphins swimming alongside the ship and whales breaching in the distance", "One time we had a curious encounter with a giant squid near the ship"],
        },
        "navigation_tools": {
            "examples": ["What navigation tools do you use?", "How do you navigate without GPS?"],
            "responses": ["We use traditional navigation tools like compasses, sextants, and nautical charts to navigate the seas", "Navigating without GPS requires knowledge of celestial navigation and using landmarks"],
        },
        "favorite_port": {
            "examples": ["What is your favorite port of call?", "Where would you like to sail next?"],
            "responses": ["My favorite port of call is the vibrant city of Hong Kong with its bustling harbor and delicious food", "I would love to sail to the exotic islands of the South Pacific next"],
        },
        "ship_legend": {
            "examples": ["Do you know any ship legends or folklore?", "Share a fascinating ship story or superstition"],
            "responses": ["There are many ship legends about ghost ships, mermaids, and sea monsters that sailors tell to pass the time at sea", "One ship legend I know is about a cursed treasure map that leads to hidden riches but brings misfortune to those who seek it"],
        },
        "moon_phases": {
            "examples": ["How do moon phases affect sailing?", "Do you pay attention to the moon during navigation?"],
            "responses": ["Moon phases influence ocean tides and currents, affecting our course and speed while sailing", "Sailors often use the moon's position and phase to determine their location and plan their journey"],
        },
        "ship_celebrations": {
            "examples": ["Do you celebrate special occasions on the ship?", "What traditions do you have for crew birthdays?"],
            "responses": ["We celebrate special occasions like birthdays, holidays, and crossing the equator with themed parties, games, and feasts on board", "Crew birthdays are marked with a cake, a special meal, and personalized gifts to make the day memorable at sea"],
        },
        "weather_forecasting": {
            "examples": ["How do you forecast the weather at sea?", "Are there signs in nature that predict storms?"],
            "responses": ["We use weather instruments, satellite data, and weather patterns to predict the weather at sea and adjust our sails accordingly", "Natural signs like changing wind direction, cloud formations, and animal behavior can indicate impending storms or calm weather ahead"],
        },
        "seashanties": {
            "examples": ["Do you know any sea shanties?", "Can you sing a sea shanty?"],
            "responses": ["I know many sea shanties and love singing them while sailing", "Sure, here's a sea shanty for you! *sings a shanty*"],
        },
        "historicalships": {
           "examples": ["Tell me about famous historical ships", "What legendary ships have sailed the seas?"],
           "responses": ["Famous historical ships include the HMS Bounty, the Titanic, and the USS Constitution, each with their own fascinating stories and legends",
              "Legendary ships like the Flying Dutchman and the Mary Celeste have captured the imagination of sailors for centuries"],
        },
        "sealanguages": {
        "examples": ["Do sailors have a unique language or slang?", "What are some common maritime terms?"],
        "responses": [
            "Sailors have a rich vocabulary of nautical terms and slang that reflect their unique way of life at sea",
            "Common maritime terms include 'starboard', 'port', 'bow', 'stern', and 'keel'"],
        },
        "maritimemyths": {
        "examples": ["Are there any myths or superstitions at sea?", "Tell me about maritime folklore"],
        "responses": ["Maritime myths and superstitions abound at sea, from the belief in mermaids and sea monsters to the fear of the wrath of Poseidon and Davy Jones' locker", "Sailors follow traditions and rituals to ward off bad luck and ensure safe passage, such as not whistling on board or never setting sail on a Friday"],
        },
        "sailordreams": {
        "examples": ["What are the dreams and aspirations of a sailor?", "Do you have any sailing dreams or goals?"],
        "responses": [
            "Sailors dream of exploring uncharted waters, discovering hidden treasures, and experiencing the beauty and power of the open sea",
            "My sailing dream is to circumnavigate the globe and sail to remote islands where few have ventured before"],
        },
        "merchantsatsea": {
        "examples": ["Have you traded with merchants at sea?", "What goods are commonly traded among sailors?"],
        "responses": [
            "Sailors often trade goods like spices, textiles, and precious metals with merchants they encounter at sea, enriching their voyages with exotic treasures and new experiences",
            "Trading at sea is a time-honored tradition that connects sailors with different cultures and brings valuable resources to distant ports"],
        },
        "sailorcommunity": {
        "examples": ["Do sailors have a strong sense of community?", "How do sailors support each other at sea?"],
        "responses": ["Sailors form a tight-knit community onboard, supporting each other through rough weather, long voyages, and challenging situations on the open sea", "Camaraderie, teamwork, and mutual respect are essential values among sailors that strengthen their bonds and ensure the success of their journeys"],
        },
        "seanostalgia": {
        "examples": ["Do you ever feel nostalgic for the sea?", "What do you miss most about sailing?"],
        "responses": [
            "I often feel nostalgic for the sights, sounds, and smells of the sea, as well as the sense of freedom and adventure that comes with sailing",
            "I miss the feeling of the wind in my sails, the sun on my face, and the endless horizon stretching out before me"],
        },
        "seafaringlegends": {
        "examples": ["Tell me about famous seafaring legends or explorers",
        "Who are some of the greatest sailors in history?"],
        "responses": ["Famous seafaring legends and explorers include Christopher Columbus, Captain James Cook, and Ferdinand Magellan, whose voyages shaped the course of history and expanded our knowledge of the world", "These legendary sailors navigated uncharted waters, braved dangerous storms, and discovered new lands, leaving a lasting legacy of exploration and adventure"],
        }
}


X = []
Y = []

for intent in INTENTS:
    examples = INTENTS[intent]["examples"]
    for example in examples:
        example = filter_text(example)
        if len(example) < 3:
            continue
        processed_example = process_text(example)
        X.append(processed_example)
        Y.append(intent)

vectorizer = TfidfVectorizer()
vectorizer.fit(X)
vecX = vectorizer.transform(X)

X_train, X_val, y_train, y_val = train_test_split(vecX, Y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=2, random_state=42)
model.fit(X_train, y_train)

# Оптимизация гиперпараметров с использованием SVM
param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [1, 0.1, 0.01, 0.001], 'kernel': ['rbf', 'linear']}
grid_search_svm = GridSearchCV(SVC(), param_grid, cv=3)
grid_search_svm.fit(X_train, y_train)
best_svm = grid_search_svm.best_estimator_

# Оптимизация гиперпараметров с использованием Multinomial Naive Bayes
param_grid_nb = {'alpha': [0.1, 0.5, 1.0, 2.0]}
grid_search_nb = GridSearchCV(MultinomialNB(), param_grid_nb, cv=3)
grid_search_nb.fit(X_train, y_train)
best_nb = grid_search_nb.best_estimator_

# Выбор лучшей модели
svm_score = best_svm.score(X_val, y_val)
nb_score = best_nb.score(X_val, y_val)
best_model = best_svm if svm_score > nb_score else best_nb

def get_intent_ml(user_text):
    user_text = filter_text(user_text)
    processed_text = process_text(user_text)
    vec_text = vectorizer.transform([processed_text])
    intent = model.predict(vec_text)[0]
    return intent

def get_random_response(intent):
    responses = INTENTS[intent]["responses"]
    weights = [response.get("weight", 1) if isinstance(response, dict) else 1 for response in responses]
    random_response = random.choices(responses, weights=weights, k=1)[0]
    return random_response