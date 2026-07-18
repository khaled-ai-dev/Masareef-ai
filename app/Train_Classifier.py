import pandas as pd
import re # allows you to search, extract, split, and manipulate text based on complex character patterns.
import joblib # a library for saving/loading Python objects to disk, so we don't have to retrain every time the app runs.
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer # imports the tool that converts text into number, since ML models can't read words directly.
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score # three different ways of measuring how good a model's predictions are. Used to evaluate the results after training.
from app.Text_Normalizer import normalize_text

df = pd.read_csv("data/Bank_SMS_Dataset.csv", encoding="utf-8-sig")
print(f"Loaded {len(df)} rows.")

df["clean_text"] = df["sms_text"].apply(normalize_text) #run the function on every row of the "sms_text" column and store the new results in a new column called "clean_text".


before = len(df)
df = df.drop_duplicates(subset="clean_text").reset_index(drop=True)
after = len(df)
print(f"Removed {before - after} duplicate rows after normalization. {after} rows remain.")


X_train, X_test, y_train, y_test = train_test_split(df["clean_text"], df["transaction_type"], test_size=0.2, random_state=42, stratify=df["transaction_type"])
print(f"Training rows: {len(X_train)} | Testing rows: {len(X_test)}")


vectorizer = TfidfVectorizer(ngram_range=(3,5), min_df=2, analyzer="char_wb")
X_train_vector = vectorizer.fit_transform(X_train) #learns the vocabulary of the training text and converts its into numeric representation. 
X_test_vector = vectorizer.transform(X_test) #convert the test text into numbers.


Log_Regression = LogisticRegression(max_iter=1000, class_weight="balanced") # training a logistic regression model with modifications on iterations and class weight to focus on effective & accurate training.
Log_Regression.fit(X_train_vector, y_train) # Actual training. The model looks at the numeric training features & their correect labels & learns the relationship between them.
Log_Regression_Predictions = Log_Regression.predict(X_test_vector) # Uses the now trained model to guess labels for the test set, which its never seen labels for during training.
Log_Regression_Accuracy = accuracy_score(y_test, Log_Regression_Predictions) #Compares the model's guesses with the actual real correct answers.

Random_Forest = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced") # training a random forest model with 200 individual decision trees internally and combines their votes. This is just anothe rmodel to check which performs better rather than assuming.
Random_Forest.fit(X_train_vector, y_train) # Actual training using random forest model.
Random_Forest_Predictions = Random_Forest.predict(X_test_vector) # Uses the now trained random forest model to guess labels for the test set.
Random_Forest_Accuracy = accuracy_score(y_test, Random_Forest_Predictions) # Compares the random forest model's guesses with actual real correct answers.

print(f"\nLogistic Regression Accuracy: {Log_Regression_Accuracy:.4f}")
print(f"Random Forest Accuracy: {Random_Forest_Accuracy:.4f}") # Prints both accuracy scores to decide which is best to keep.


if Log_Regression_Accuracy >= Random_Forest_Accuracy:
    Best_model = Log_Regression
    Best_predictions = Log_Regression_Predictions
    Best_name = "Logistic Regression"
else:
    Best_model = Random_Forest
    Best_predictions = Random_Forest_Predictions
    Best_name = "Random Forest"
#the above compares both model accuracy scores to see which one performed better and use for evaluation and saving automatically without intervation or later modifications.


print(f"\nBest model: {Best_name}\n") #displays the best performing model
print("Classification Report:")
print(classification_report(y_test, Best_predictions)) #displays a breakdown of the 4 transaction types to see how often the model was precise and has a good recall.
print("Confusion matrix (rows=actual, columns=predicted):")
print(confusion_matrix(y_test, Best_predictions, labels=Best_model.classes_)) #builds a grid that shows which transaction types got mistaken for which (example: "Purchase" messages predicted as "Transfer")
print("Labels Order:", list(Best_model.classes_)) #displays the category names used in the confusion matrix/grid above.

joblib.dump(Best_model, "models/Transaction_Type_Classifier.jonlib") #saves a python object to a file on disk (the trained model, and the vectorizer, recall: used to convert new raw text into same numeric format the model expect) both must be loaded together to make a real prediciton later.
joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")
print("\nSaved model and vectorizer to models/") #confirms the save is completed without having to manually check the models folder (optional but professionally preferred).

