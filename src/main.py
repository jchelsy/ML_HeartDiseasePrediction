# Import libraries
import io
import os
from src import resource_dir
from math import e
import numpy as np
import pandas as pd
from sklearn import tree  # DT Lib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import openpyxl
import tkinter as tk
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
import cairosvg
import warnings  # suppress warnings
warnings.filterwarnings("ignore")


################################################

# DATA FROM:
# https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction

"""
Age                 - Patient age (in years)
Sex                 - Patient gender  (Male=0 ; Female=1)
ChestPainType       - Chest pain   (TA=0  [typical angina] ;     ATA=1  [atypical angina] ;
                                    NAP=2  [non-anginal pain] ;  ASY=3  [asymptomatic])
RestingBP           - Resting blood pressure  (in mm Hg)
Cholesterol         - Level of cholesterol  (in mm/dl)
FastingBS           - Fasting blood sugar  > 120 mg/dl  (1=true, if fasting blood sugar > 120 mg/dl ; 0 = false)
RestingECG          - Resting electrocardiographic results  (Normal=0 ; ST=1  [having ST-T wave abnormality] ; 
                                    LVH=2  [showing probable/definite left ventricular hypertrophy by Estes' criteria] )
MaxHR               - Maximum heart rate achieved
ExerciseAngina      - Exercise-induced angina  (Yes=1 ; No=0)
Oldpeak             - ST depression induced by exercise relative to rest
ST_Slope            - The slope of the peak exercise ST segment  (Up-sloping=1 ; Flat=0 ; Down-sloping=2)

HeartDisease        - DIAGNOSIS OF HEART DISEASE (angiographic disease status)
                        0 =  > 50% diameter narrowing  -  LESSER CHANCE OF HEART DISEASE
                        1 =  < 50% diameter narrowing  -  GREATER CHANCE OF HEART DISEASE
"""

#######################
# REMOVED DATA VALUES #
#######################

"""
REMOVAL COUNT: 172 rows

Where 'Cholesterol' is 0 (invalid data)...

Lines:
295-417, 423, 425, 426, 429-432, 436-444, 448, 451-453, 455, 457-461, 463, 465, 466, 
468, 469, 472-474, 476, 477, 479, 481-483, 485, 486, 494, 510, 516, 517, 520, 537, 538
"""


################################################


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        """ ====================
             PAGE CONFIGURATION
            ==================== """
        # Set the default fonts
        self.small_font = font.Font(self, family="Cambria", size=12)
        self.medium_font = font.Font(self, family="Cambria", size=14)
        self.title_font = font.Font(self, family="Tw Cen MT Condensed", size=16, weight="bold")
        self.header_font = font.Font(self, family="Tw Cen MT Condense", size=24, weight="bold")

    """ Method to lift a page to the topmost "layer" (to view a page) """
    def show(self):
        # Raise page to the top of the "stack" of pages
        self.lift()


# Page 1  -  LANDING PAGE
class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        """ ========================
             INITIALIZE VARIABLE(S)
            ======================== """
        # Initialize the image logo (convert SVG to PNG data, then convert to an ImageTk.PhotoImage object)
        logo_imgdata = cairosvg.svg2png(url=os.path.join(resource_dir, "logo.svg"))
        logo_im = Image.open(io.BytesIO(logo_imgdata))
        self.logo_img = ImageTk.PhotoImage(logo_im)

        """ ====================
             PAGE CONFIGURATION
            ==================== """
        # Create all widgets
        self.header_title = tk.Label(self, text="Heart Disease", font=self.header_font)
        self.header_subtitle = tk.Label(self, text="Are You At Risk?", font=self.title_font)
        self.logo = tk.Label(self, image=self.logo_img)
        self.start_btn = tk.Button(self, text="Start", font=self.medium_font)

        # Place all widgets
        self.header_title.pack(ipady=15)
        self.header_subtitle.pack(ipady=5)
        self.logo.pack(ipady=40)
        self.start_btn.pack()


# Page 2  -  INPUT INFORMATION
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        """ ========================
             INITIALIZE VARIABLE(S)
            ======================== """
        # Italicized font
        self.italic_font = font.Font(self, family="Cambria", size=12, slant="italic")

        ########################################
        # INITIALIZE ALL INPUT VALUE VARIABLES #
        ########################################
        self.val_age = tk.StringVar(value="0")

        self.val_sex = tk.StringVar(value="Select...")
        self.val_sex_options = ["Male", "Female"]
        ##########
        self.val_pain = tk.StringVar(value="Select...")
        self.val_pain_options = ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"]
        ##########
        self.val_bs = tk.StringVar(value="Select...")
        self.val_bs_options = ["Yes", "No"]
        ##########
        self.val_bp = tk.StringVar(value="0")

        self.val_chol = tk.StringVar(value="0")
        ##########
        self.val_ecg = tk.StringVar(value="Select...")
        self.val_ecg_options = ["Normal", "ST-T Wave Abnormality", "Probable Left Ventricular Hypertrophy"]
        ##########
        self.val_hr = tk.StringVar(value="0")
        ##########
        self.val_angina = tk.StringVar(value="Select...")
        self.val_angina_options = ["Yes", "No"]
        ##########
        self.val_peak = tk.StringVar(value="0")
        ##########
        self.val_slope = tk.StringVar(value="Select...")
        self.val_slope_options = ["Up-sloping", "Flat", "Down-sloping"]

        """ ====================
             PAGE CONFIGURATION
            ==================== """

        ###########################
        # CREATE FRAMES (per row) #
        ###########################
        self.row1 = tk.Frame(self)
        self.row2 = tk.Frame(self)
        self.row3 = tk.Frame(self)
        self.row4 = tk.Frame(self)
        self.row5 = tk.Frame(self)
        self.row6 = tk.Frame(self)
        self.row7 = tk.Frame(self)
        self.row8 = tk.Frame(self)
        self.row9 = tk.Frame(self)

        #################
        # CREATE LABELS #
        #################
        self.label_age = tk.Label(self.row1, text="Age:", font=self.small_font)
        self.label_sex = tk.Label(self.row1, text="Gender:", font=self.small_font)
        self.label_pain = tk.Label(self.row2, text="Is the patient experiencing chest pain?", font=self.small_font)
        self.label_bs = tk.Label(self.row3, text="Is the patient fasting?", font=self.small_font)
        self.label_bp = tk.Label(self.row4, text="Resting BP (mm Hg):", font=self.small_font)
        self.label_chol = tk.Label(self.row4, text="Cholesterol (mm/dl):", font=self.small_font)
        self.label_ecg = tk.Label(self.row5, text="Resting ECG results:", font=self.small_font)
        self.label_hr = tk.Label(self.row6, text="Maximum heart-rate achieved:", font=self.small_font)
        self.label_angina = tk.Label(self.row7, text="Does the patient have exercise-induced angina?", font=self.small_font)
        self.label_peak = tk.Label(self.row8, text="Oldpeak:", font=self.small_font)
        self.label_slope = tk.Label(self.row9, text="ST Slope:", font=self.small_font)

        #######################
        # CREATE INPUT FIELDS #
        #######################
        self.input_age = tk.Spinbox(self.row1, from_=0, to=99, textvariable=self.val_age, wrap=False, width=3)
        self.input_sex = tk.OptionMenu(self.row1, self.val_sex, *self.val_sex_options)
        self.input_pain = tk.OptionMenu(self.row2, self.val_pain, *self.val_pain_options)
        self.input_bs = tk.OptionMenu(self.row3, self.val_bs, *self.val_bs_options)
        self.input_bp = tk.Spinbox(self.row4, from_=0, to=999, textvariable=self.val_bp, wrap=False, width=3)
        self.input_chol = tk.Spinbox(self.row4, from_=0, to=999, textvariable=self.val_chol, wrap=False, width=3)
        self.input_ecg = tk.OptionMenu(self.row5, self.val_ecg, *self.val_ecg_options)
        self.input_hr = tk.Spinbox(self.row6, from_=0, to=999, textvariable=self.val_hr, wrap=False, width=3)
        self.input_angina = tk.OptionMenu(self.row7, self.val_angina, *self.val_angina_options)
        self.input_peak = tk.Spinbox(self.row8, from_=-10, to=10, textvariable=self.val_peak, wrap=False, width=3,
                                     increment=0.5)
        self.input_slope = tk.OptionMenu(self.row9, self.val_slope, *self.val_slope_options)

        #####################
        # PLACE ALL CONTENT #
        #####################
        self.label_age.grid(row=0, column=0, padx=5, pady=5)
        self.input_age.grid(row=0, column=1, padx=0, pady=5)

        self.label_sex.grid(row=0, column=2, padx=(20, 5), pady=5)
        self.input_sex.grid(row=0, column=3, padx=0, pady=5)
        ##########
        self.label_pain.grid(row=0, column=0, padx=5, pady=5)
        self.input_pain.grid(row=0, column=1, padx=0, pady=5)
        ##########
        self.label_bs.grid(row=0, column=0, padx=5, pady=5)
        self.input_bs.grid(row=0, column=1, padx=5, pady=5)
        ##########
        self.label_bp.grid(row=0, column=0, padx=5, pady=5)
        self.input_bp.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.label_chol.grid(row=1, column=0, padx=5, pady=5)
        self.input_chol.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ##########
        self.label_ecg.grid(row=0, column=0, padx=5, pady=5)
        self.input_ecg.grid(row=0, column=1, padx=5, pady=5)
        ##########
        self.label_hr.grid(row=0, column=0, padx=5, pady=5)
        self.input_hr.grid(row=0, column=1, padx=5, pady=5)
        ##########
        self.label_angina.grid(row=0, column=0, padx=5, pady=5)
        self.input_angina.grid(row=0, column=1, padx=5, pady=5)
        ##########
        self.label_peak.grid(row=0, column=0, padx=5, pady=5)
        self.input_peak.grid(row=0, column=1, padx=5, pady=5)
        ##########
        self.label_slope.grid(row=0, column=0, padx=5, pady=5)
        self.input_slope.grid(row=0, column=1, padx=5, pady=5)

        ##########################
        # PLACE ALL (ROW) FRAMES #
        ##########################
        self.row1.pack(side="top", anchor="w")
        self.row2.pack(side="top", anchor="w")
        self.row3.pack(side="top", anchor="w")
        self.row4.pack(side="top", anchor="w")
        self.row5.pack(side="top", anchor="w")
        self.row6.pack(side="top", anchor="w")
        self.row7.pack(side="top", anchor="w")
        self.row8.pack(side="top", anchor="w")
        self.row9.pack(side="top", anchor="w")

        # SUBMIT BUTTON
        self.submit_btn = tk.Button(self, text="Submit", font=self.medium_font)
        self.submit_btn.pack(side="bottom", anchor="center", pady=20)

        # REMOVE FOCUS FROM WIDGET BY CLICKING OFF
        self.bind_all("<1>", lambda event: event.widget.focus_set())

        # BIND INPUT EVENTS TO CHANGE LABEL COLOR BACK FROM RED (if applicable)
        #   (<FocusIn> event detects when a particular widget is focused on - to detect their selection)
        self.input_age.bind("<FocusIn>", self.config_age)
        self.input_sex.bind("<FocusIn>", self.config_sex)
        self.input_pain.bind("<FocusIn>", self.config_pain)
        self.input_bs.bind("<FocusIn>", self.config_bs)
        self.input_bp.bind("<FocusIn>", self.config_bp)
        self.input_chol.bind("<FocusIn>", self.config_chol)
        self.input_ecg.bind("<FocusIn>", self.config_ecg)
        self.input_hr.bind("<FocusIn>", self.config_hr)
        self.input_angina.bind("<FocusIn>", self.config_angina)
        self.input_peak.bind("<FocusIn>", self.config_peak)
        self.input_slope.bind("<FocusIn>", self.config_slope)

    def reset(self):
        self.val_age.set("0")
        self.val_sex.set("Select...")
        self.val_pain.set("Select...")
        self.val_bs.set("Select...")
        self.val_bp.set("0")
        self.val_chol.set("0")
        self.val_ecg.set("Select...")
        self.val_hr.set("0")
        self.val_angina.set("Select...")
        self.val_peak.set("0.0")
        self.val_slope.set("Select...")

    def config_age(self, event):
        if self.label_age["fg"] == "red":
            self.label_age.config(fg="black")

    def config_sex(self, event):
        if self.label_sex["fg"] == "red":
            self.label_sex.config(fg="black")

    def config_pain(self, event):
        if self.label_pain["fg"] == "red":
            self.label_pain.config(fg="black")

    def config_bs(self, event):
        if self.label_bs["fg"] == "red":
            self.label_bs.config(fg="black")

    def config_bp(self, event):
        if self.label_bp["fg"] == "red":
            self.label_bp.config(fg="black")

    def config_chol(self, event):
        if self.label_chol["fg"] == "red":
            self.label_chol.config(fg="black")

    def config_ecg(self, event):
        if self.label_ecg["fg"] == "red":
            self.label_ecg.config(fg="black")

    def config_hr(self, event):
        if self.label_hr["fg"] == "red":
            self.label_hr.config(fg="black")

    def config_angina(self, event):
        if self.label_angina["fg"] == "red":
            self.label_angina.config(fg="black")

    def config_peak(self, event):
        if self.label_peak["fg"] == "red":
            self.label_peak.config(fg="black")

    def config_slope(self, event):
        if self.label_slope["fg"] == "red":
            self.label_slope.config(fg="black")


# Page 3  -  OUTPUT RESULT
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        """ ========================
             INITIALIZE VARIABLE(S)
            ======================== """
        self.prediction_result = 5

        # Initialize 'thumbs up' image (convert SVG to PNG data, then convert to an ImageTk.PhotoImage object)
        thumbs_up_imgdata = cairosvg.svg2png(url=os.path.join(resource_dir, "thumbs-up.svg"))
        thumbs_up_im = Image.open(io.BytesIO(thumbs_up_imgdata))
        self.thumbs_up_img = ImageTk.PhotoImage(thumbs_up_im)

        # Initialize 'warning' image (convert SVG to PNG data, then convert to an ImageTk.PhotoImage object)
        warning_imgdata = cairosvg.svg2png(url=os.path.join(resource_dir, "warning.svg"))
        warning_im = Image.open(io.BytesIO(warning_imgdata))
        self.warning_img = ImageTk.PhotoImage(warning_im)

        """ ====================
             PAGE CONFIGURATION
            ==================== """
        # Create all widgets
        self.label1 = tk.Label(self, text="Results", font=self.title_font)
        self.img = tk.Label(self, image=self.warning_img)
        self.label2 = tk.Label(self, text="a", font=self.header_font)

        # Place all widgets
        self.label1.pack(pady=50)
        self.img.pack(pady=10)
        # self.label2.pack(side="bottom", pady=50)
        self.label2.pack(pady=20)

        # ADD 'RESTART' BUTTON
        self.restart_btn = tk.Button(self, text="\u21BA", font=self.medium_font, height=1)
        self.restart_btn.pack(side="bottom", anchor="e", padx=3, pady=3)

    def update_prediction(self, prediction):
        # Update the prediction variable
        self.prediction_result = prediction

        # If the prediction is NO - [GOOD RESULT - likely no heart disease]
        if self.prediction_result == 1:
            # Set the 'thumbs up' image
            self.img.config(image=self.thumbs_up_img)

            # Update the result text
            self.label2.config(text="You're CLEAR!")

        # If the prediction is YES - [BAD RESULT - possible heart disease]
        elif self.prediction_result == 0:
            # Set the 'warning' image
            self.img.config(image=self.warning_img)

            # Update the result text
            self.label2.config(text="You're AT RISK!")

        # Otherwise (this should NEVER pass, as the prediction result should ONLY be 0 or 1)
        else:
            print("ERROR: BROKEN PREDICTION")
            self.master.destroy()

    def reset(self):
        self.prediction_result = 5


# Controls the main window container  -  contains, controls, & views Page(s)
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        """ ========================
             INITIALIZE VARIABLE(S)
            ======================== """
        # Set the file path for the imported dataset
        self.csv_data_file = os.path.join(resource_dir, "heart.csv")

        # Read the Excel file into a Pandas DataFrame
        self.df = pd.read_csv(self.csv_data_file)

        # Feature selection from data columns (features - X)
        self.X_features = self.df[[
            'Age',              # int64
            'Sex',              # int64   [ORIG. object]
            'ChestPainType',    # int64   [ORIG. object]
            'RestingBP',        # int64
            'Cholesterol',      # int64
            'FastingBS',        # int64
            'RestingECG',       # int64   [ORIG. object]
            'MaxHR',            # int64
            'ExerciseAngina',   # int64   [ORIG. object]
            'Oldpeak',          # float64
            'ST_Slope',         # int64   [ORIG. object]
        ]]

        # Target selection from data columns (label - y)
        self.y_label = self.df[['HeartDisease']]

        # Initialize the Classifier
        self.clf = tree.DecisionTreeClassifier()

        # !!! TRAIN the Classifier !!!
        self.clf = self.clf.fit(self.X_features, self.y_label)

        """ ======================
             WINDOW CONFIGURATION
            ====================== """

        ######################
        # Initializing Pages #
        ######################

        # Create object for each Page
        self.p1 = Page1(self)
        self.p2 = Page2(self)
        self.p3 = Page3(self)

        # Create container to hold all content  -  contains Page(s)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Place all pages (stacked atop one another) within the 'container' Frame (the "Page Stack")
        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        ########################
        # Button Configuration #
        ########################

        # "Start" Button on Page 1  -  navigates to Page2
        self.p1.start_btn.config(command=self.p2.show)
        # "Submit" Button on Page 2  -  checks if all fields have been entered, then runs the prediction & goes to Page3
        self.p2.submit_btn.config(command=self.submit_data)
        # "Restart" Button on Page 3  -  resets everything & navigates back to Page1
        self.p3.restart_btn.config(command=self.reset)

        ########################################

        # Display the first Page!
        self.p1.show()

    def submit_data(self):
        # Flag for checking if anything isn't filled out
        complete = True

        # Return all text back to default black (in case it is red from previously incomplete input fields)
        self.p2.label_age.config(fg="black")
        self.p2.label_sex.config(fg="black")
        self.p2.label_pain.config(fg="black")
        self.p2.label_bs.config(fg="black")
        self.p2.label_bp.config(fg="black")
        self.p2.label_chol.config(fg="black")
        self.p2.label_ecg.config(fg="black")
        self.p2.label_hr.config(fg="black")
        self.p2.label_angina.config(fg="black")
        # self.p2.label_peak.config(fg="black")  # Initializes to 0.0, which is VALID
        self.p2.label_slope.config(fg="black")

        # Check each input field for incomplete entries
        # (set 'complete' flag to False & the label text to red to indicate which field is incomplete)
        if self.p2.val_age.get() == "0":
            complete = False
            self.p2.label_age.config(fg="red")
        if self.p2.val_sex.get() == "Select...":
            complete = False
            self.p2.label_sex.config(fg="red")
        if self.p2.val_pain.get() == "Select...":
            complete = False
            self.p2.label_pain.config(fg="red")
        if self.p2.val_bs.get() == "Select...":
            complete = False
            self.p2.label_bs.config(fg="red")
        if self.p2.val_bp.get() == "0":
            complete = False
            self.p2.label_bp.config(fg="red")
        if self.p2.val_chol.get() == "0":
            complete = False
            self.p2.label_chol.config(fg="red")
        if self.p2.val_ecg.get() == "Select...":
            complete = False
            self.p2.label_ecg.config(fg="red")
        if self.p2.val_hr.get() == "0":
            complete = False
            self.p2.label_hr.config(fg="red")
        if self.p2.val_angina.get() == "Select...":
            complete = False
            self.p2.label_angina.config(fg="red")
        # if self.p2.val_peak.get() == "":
        #     return
        if self.p2.val_slope.get() == "Select...":
            complete = False
            self.p2.label_slope.config(fg="red")

        # If nothing was flagged as incomplete:
        if complete:
            # !!! Run the PREDICTION with the given test data !!!
            result = self.predict()
            # !!! Update the prediction result in Page 3 !!!
            self.p3.update_prediction(result)
            # Navigate to Page 3!
            self.p3.show()

    # Method to convert the text variable of all data values into their corresponding ACTUAL data value (features)
    def convert_values(self):
        # 'Age' feature
        age = int(self.p2.val_age.get())

        # 'Sex' feature
        gender = {
            'Male': 0,
            'Female': 1
        }[self.p2.val_sex.get()]

        # 'ChestPainType' feature
        pain = {
            'Typical Angina': 0,
            'Atypical Angina': 1,
            'Non-Anginal Pain': 2,
            'Asymptomatic': 3
        }[self.p2.val_pain.get()]

        # 'RestingBP' feature
        blood_pressure = int(self.p2.val_bp.get())

        # 'Cholesterol' feature
        cholesterol = int(self.p2.val_chol.get())

        # 'FastingBS' feature
        fasting = {
            'Yes': 1,
            'No': 0
        }[self.p2.val_bs.get()]

        # 'RestingECG' feature
        ecg = {
            'Normal': 0,
            'ST-T Wave Abnormality': 1,
            'Probable Left Ventricular Hypertrophy': 2
        }[self.p2.val_ecg.get()]

        # 'MaxHR' feature
        heartrate = int(self.p2.val_hr.get())

        # 'ExerciseAngina' feature
        angina = {
            'Yes': 1,
            'No': 0
        }[self.p2.val_angina.get()]

        # 'Oldpeak' feature
        old_peak = float(self.p2.val_peak.get())

        # 'ST_Slope' feature
        st_slope = {
            'Flat': 0,
            'Up-sloping': 1,
            'Down-sloping': 2
        }[self.p2.val_slope.get()]

        # Return a list of all feature data
        return [age, gender, pain, blood_pressure, cholesterol, fasting, ecg, heartrate, angina, old_peak, st_slope]

    # Method to run the prediction of the classifier
    def predict(self):
        # !!! Convert all text variables of submitted data to ACTUAL data to be used as FEATURES !!!
        test_features = self.convert_values()
        print(test_features)  # Output resulting features list to the console

        # Run the prediction through the trained classifier
        prediction_result = self.clf.predict([test_features])
        print("PREDICTION:", prediction_result)  # Output the prediction result

        # Return the prediction result
        return prediction_result

    def reset(self):
        self.p2.reset()
        self.p3.reset()

        self.p1.show()
