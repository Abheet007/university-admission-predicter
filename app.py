from flask import Flask                               # for creating web application
from flask import render_template                     # for rendering index.html from templates
from flask import request                             # for making GET and POST requests
from flask import Markup                              # for rendering seaborn plot
import io, os, base64                                 # For converting seaborn plot to base 64
import matplotlib.pyplot as plt                       # for creating visualizations
import seaborn as sb                                  # for creating visualizations
import pandas as pd                                   # for doing Data Analysis  
import numpy as np                                    # for implementing numpy arrays
from sklearn.linear_model import LinearRegression     # for implementing multiple linear regression
import threading                                      # for creating threads


app = Flask(__name__)

# Performing Elementary Data Import, Analysis and Wrangling


data = pd.read_csv(r"admission.csv", encoding='utf-8')
data=data.drop(columns=['Serial No.'])
Data=data.rename(columns={'GRE Score':'GRE','TOEFL Score':'TOEFL','University Rating':'university_Rating','Chance of Admit ':'Chance_of_Admit'},inplace=True)
data['Chance_of_Admit']=data['Chance_of_Admit']**2
data = data[data.Chance_of_Admit >0.40]
data.reset_index(drop = True, inplace = True)

# Function Responsible for performing Multiple Linear Regression on the given dataframe and return predicted 
# chances of Admission

def main_prediction_func(lst):
  global data
  x = data.iloc[:, :-1].values
  y = data.iloc[:, 7].values
  # Shuffle your dataset 
  shuffle_df = data.sample(frac=1)
  # Define a size for your train set 
  train_size = int(0.7 * len(data))
  # Split your dataset 
  train_set = shuffle_df[:train_size]
  test_set = shuffle_df[train_size:]
  X_train = train_set.iloc[:, :-1].values
  y_train = train_set.iloc[:, 7].values
  X_test = test_set.iloc[:, :-1].values
  y_test = test_set.iloc[:, 7].values
  # Initializing Model
  regressor= LinearRegression()
  # Fitting Model  
  regressor.fit(X_train, y_train)
  # Predicting Chances of Admission 
  y_pred= regressor.predict(lst) 
  # Logging the Accuracy Metrics and Coefficients
  print('Train Score: ', regressor.score(X_train, y_train))  
  print('Test Score: ', regressor.score(X_test, y_test)) 
  print('Coefficients: ', regressor.coef_)
  # Converting Predicted Value to Percentage
  y_pred=y_pred*100
  # Predicted Percentage returned
  return "<h2>"+((str(y_pred).replace("[","")).replace("]",""))+"%</h2>"

# Function Responsible for creating Visualizations

def plot_maker():
  # Using Seaborn to create a heatmap of relevant independent variable
  plt.figure(figsize=(15,7))
  cr = data.corr()
  sb.heatmap(cr, annot=True, linewidths=0.10, fmt= '.5f',cmap="YlGnBu")
  img = io.BytesIO()
  # Saving Plot as a png image
  plt.savefig(img, format='png')
  img.seek(0)
  # Converting image to base 64 value for sending it to Webpage for rendering
  plot_url = base64.b64encode(img.getvalue()).decode()
  # Storing the base 64 value in form of a URL to a Variable
  my_plot = Markup('<img src="data:image/png;base64,{}" style="width:70%;border:1px solid black">'.format(plot_url))
  # Returning the base64 URL variable
  return my_plot

# Main function responsible for rendering of Home page

@app.route("/", methods = ['POST','GET'])
def home_():
    return render_template('index.html')

# Function responsible for collecting the data sent through POST request through the form in home page and
# assigning the values to variables for the purpose of calling the prediction function and plot maker function.

@app.route("/prediction_wala_page", methods = ['POST','GET'])
def prediction_page():
    res = None
    naam = None
    plot_url = "No Plot Available for this Process"
    lst = None
    if request.method == "POST":
        phla_naam = (request.form["firstname"])
        aakhri_naam = (request.form["lastname"])
        gre_score = (request.form["gre_score"])
        toefl_score = (request.form["toefl_score"])
        univ_rating = (request.form["univ_rating"])
        sop = (request.form["sop"])
        lor = (request.form["lor"])
        cgpa = (request.form["cgpa"])
        research = (request.form["research"])
        lst = [[gre_score,toefl_score,univ_rating,sop,lor,cgpa,research]]
        naam = phla_naam+" "+aakhri_naam
        # thread = threading.Thread(target=plot_banane_wala)
        # thread.start()
        # thread.join()
        res = main_prediction_func(lst)
        plot_url = plot_maker()
        
    return '''
    <!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <!-- Fontawesome Kit -->
    <script src="https://kit.fontawesome.com/5de545e21a.js" crossorigin="anonymous"></script>
 
    <title>Prediction</title>
  </head>
  <body>
    <h1></h1>


<div class="alert alert-success" role="alert">
  <h4 class="alert-heading">Disclaimer</h4>
  <p>Please note that the Admission cutoffs depend on many parameters and may fluctuate.</p>
  <hr> 
  <p class="mb-0">This is just an estimated prediction.</p>
</div>
<br/>
<br/>
<center>
<div class="card">
  <div class="card-body">
        <p> Hi {naam}! Your chances of getting in this college are :- <br/>
    {res}
  </div>
</div>

<p><i class="fas fa-chart-bar"></i>&nbsp;&nbsp;&nbsp;Dependent Variables</p>
<div id="plot_here">
    {plot_url}
</div>
</center>
<br/>
<br/>
</div>
  <div class="footer" style="position: fixed;left: 0;bottom: 0;width: 100%;background-color: #181818;color: white;text-align: center;">
  <p style="padding-top:6px">&#169;&nbsp;Abheet Singh, Ayushi Singh</p>
</div>
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
</html>
    '''.format(res=res,naam = naam,plot_url = plot_url)


if __name__ == "__main__":
    app.run(debug=True)