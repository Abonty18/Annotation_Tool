import sys
import pandas as pd
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QTextEdit,
    QRadioButton,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QButtonGroup,
    QMessageBox,
    QSplitter,
    QFileDialog,
)
from text_processing import highlight_privacy_keywords
# Additional import for directory handling
import pathlib


class ReviewAnnotator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.annotation_group = None
        self.setWindowTitle("Review Annotator")
        self.setGeometry(100, 100, 1000, 800)
        self.current_file = None  # Track the currently loaded file
        self.temp_file = None  # Track the associated temp file
        self.index = -1 #for header
        self.data=list()
        self.privacy_keywords = ['information', 'service', 'personal', 'may', 'privacy', 'pocketguard', 'use', 'policy', 'account', 'party', 'data', 'third', 'financial', 'right', 'thirdparty', 'collect', 'user', 'provide', 'access', 'bank', 'request', 'collected', 'please', 'advisor', 'also', 'consent', 'device', 'law', 'processing', 'protection']
        self.initUI()

    def load_data(self):
        try:
            self.data = pd.read_excel(self.current_file, usecols=[0])
        except FileNotFoundError:
            QMessageBox.critical(
                self, "Error", f"Excel file '{self.current_file}' not found."
            )
            sys.exit()

    def load_temp_data(self):
        if os.path.exists(self.temp_file):
            self.temp_data = pd.read_excel(self.temp_file, usecols=[0, 1])
        else:
            self.temp_data = pd.DataFrame(columns=["review", "annotation"])

    def load_existing_annotations(self):
        if hasattr(self, "data") and not self.temp_data.empty:
            unannotated_indexes = set(range(len(self.data))) - set(self.temp_data.index)
            unannotated_indexes = {x - 1 for x in unannotated_indexes}  # Subtract 1 from each element
            print("Length of data:", len(self.data))
            print("Length of temp_data:", len(self.temp_data))
            print("Unannotated indexes:", unannotated_indexes)


            # Check if there are unannotated indexes
            if unannotated_indexes:
                self.index = min(unannotated_indexes)
            else:
                self.index = -1

            # Handle the case where the first review might be considered nan
            if self.index == 0:
                self.index = -1
                

        self.next_review()


    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Create a splitter to separate the left and right sections
        splitter = QSplitter(Qt.Horizontal)

        left_width = 300  # Adjust the width as needed

        # Left section with annotation guidelines
        left_section = QTextEdit(self)
        left_section.setReadOnly(True)
        left_section.setStyleSheet(
            "font-size: 17px; font-family: Times New Roman ; background-color: #e9e9e9;border: 1px solid #f7f7b7; border-radius: 8px;"
        )
        left_section.setHtml(
            """\
        <div style="text-align: center;">
        <span style="font-size: 20px; font-family: Times New Roman ; font-weight: bold; display: block;">Annotation Guideline</span><br>
            <span style="font-weight: bold;font-size: 16px;">Objective:</span>The goal of the annotation task is to categorize the reviews based on whether they are related to privacy features, privacy bugs, or neither.<br><br>
            <span style="font-weight: bold;font-size: 16px;">Label Categories:</span><br>
            1. Privacy-Related Feature Request (Label 1): Assign this label if the review is discussing a feature request of the app related to user privacy. This could include any mention of data protection, security, user consent, encryption, or other privacy-related features request.<br>
            2. Privacy-Related Bug (Label 2): Assign this label if the review is reporting a bug or issue related to user privacy. This could include any mention of data leaks, unauthorized access, unintended exposure of sensitive information, or other privacy-related bugs.<br>
            0. Not Privacy-Related (Label 0): Assign this label if the review is not discussing any privacy-related aspects. This could be a general review about the app's functionality, user experience, or other unrelated topics.<br><br>
            <span style="font-weight: bold;font-size: 16px;">Annotation Instructions:</span><br>
            1. Read the Review: Carefully read and understand the content of the review.<br>
            2. Identify Privacy Context: Determine whether the review is discussing any issue related to user privacy. This could include issues about data security, consent, encryption, data sharing, or any other privacy-related topics.<br>
            3. Assign Appropriate Label: Based on the content of the review, assign one of the three labels: 1 (Privacy-Related Feature request), 2 (Privacy-Related Bug), or 0 (Not Privacy-Related).<br><br>
            <span style="font-weight: bold;font-size: 16px;">Examples:</span><br>
            <table style="width:100%; border: 1px solid #000; border-collapse: collapse;">
      <tr>
        <th style="border: 1px solid #000; padding: 8px;">Review</th>
        <th style="border: 1px solid #000; padding: 8px;">Annotation Label</th>
      </tr>
      <tr>
        <td style="border: 1px solid #000; padding: 8px;">Read the privacy policy on apps before you put your personal information in. They openly tell you how they collect your information and who they "may" share it with. You are putting your most valuable information into these budgeting apps and if you pay for a service you shouldn't have your information shared. They make money off ads and the $7.99/month you pay for the plus plan.</td>
        <td style="border: 1px solid #000; padding: 8px;">1</td>
      </tr>
      <tr>
        <td style="border: 1px solid #000; padding: 8px;">I like it because of its simplicity to use. As others have mentioned, it could be a bit annoying at times when loading your data. It's been some 2 weeks for me and my bank information hasn't updated in PocketGuard.</td>
        <td style="border: 1px solid #000; padding: 8px;">2</td>
      </tr>
      <tr>
        <td style="border: 1px solid #000; padding: 8px;">It's a really good app. Great for managing spending and staying on top of your money but for me it's a new app. How do I know how good the security is? I need some sort of proof before I give my financial information to an app.</td>
        <td style="border: 1px solid #000; padding: 8px;">0</td>
      </tr>
      <tr>
        <td style="border: 1px solid #000; padding: 8px;">I love this app. Setting up budgets is easy. The only reason I gave it four stars is because I have to go through a lengthy process to connect with my bank account every day that I use the app. That may be an issue with the bank and not the app itself.</td>
        <td style="border: 1px solid #000; padding: 8px;">0</td>
      </tr>
      <tr>
        <td style="border: 1px solid #000; padding: 8px;">Added my bank just fine, but then failed to add my PayPal account. When trying to set up my income sources, it didn't even provide an option to "add" any, but instead listed the money deposits from my bank account, assuming those were my only income, and ONLY allowed me to choose from those! So I can't make cash for income? On top of all the INCREDIBLY personal questions it FORCES you to answer to even set it up (net worth, etc), this one is a *HARD PASS.* This app is not good.</td>
        <td style="border: 1px solid #000; padding: 8px;">2</td>
      </tr>
      <tr>
        <td style="border: 1px solid #000; padding: 8px;">I like the app but I think it'll be a good idea to have access to our credit card information and be able to connect the popular investment applications like Acorns, Robinhood, etc. Also, if we could pay bills ahead of time through the app that'll be neat too.</td>
        <td style="border: 1px solid #000; padding: 8px;">1</td>
      </tr>
    </table>
    <br>
    
    </div>
    """
)

        splitter.addWidget(left_section)
        splitter.setSizes([left_width, 0])
        main_layout.addWidget(splitter)

        # Right section with review text and annotation widgets
        right_section = QWidget(self)
        splitter.addWidget(right_section)
        right_layout = QVBoxLayout(right_section)

        # Add the "Add File" button at the top of the right section
        add_file_button = QPushButton("Add File", self)
        add_file_button.clicked.connect(self.load_excel_file)
        right_layout.addWidget(add_file_button)
        add_file_button.setStyleSheet(
            "font-size: 16px; background-color: #008CBA;font-family: Poppins ;padding: 5px; color: white;font-weight:bold;"
        )

        review_label = QLabel("Review", self)
        review_label.setStyleSheet(
            "font-size: 20px; font-family: 'Times New Roman '; text-align: center; font-weight: bold; background-color: #ababab; padding: 7px;border: 1px solid #949494;"
        )
        review_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(review_label)
        self.review_text = QTextEdit('<div style="text-align: center;font-size: 25px; vertical-align: middle;">Please add a file first to annotate<br><span style="font-size: 90px;">😺</span></div>', self)

        self.review_text.setStyleSheet(
            "font-size: 17px; font-family: Times New Roman ; background-color: #e9e9e9;border: 1px solid #f7f7c6; border-radius: 8px;"
        )
        right_layout.addWidget(self.review_text)

        # Create a label for the annotation radio buttons
        annotation_label = QLabel("Annotation Label", self)
        annotation_label.setStyleSheet(
            "font-size: 18px; font-family: Times New Roman ;padding: 3px; font-weight: bold; "
        )
        right_layout.addWidget(annotation_label)

        # Initialize the annotation group
        self.annotation_group = QButtonGroup(self)
        self.annotation_group.setExclusive(
            True
        )  # Make the radio buttons mutually exclusive
        
        # Create radio buttons and add them to the group
        
        self.radio_button_0 = QRadioButton("0", self)
        self.radio_button_1 = QRadioButton("1", self)
        self.radio_button_2 = QRadioButton("2", self)
        self.annotation_group.addButton(self.radio_button_0, 0)
        self.annotation_group.addButton(self.radio_button_1, 1)
        self.annotation_group.addButton(self.radio_button_2, 2)
       
        
        
       
        self.radio_button_0.setStyleSheet(
            "font-size: 16px;font-family: Times New Roman ;padding: 3px;font-weight:bold; "
        )
        self.radio_button_1.setStyleSheet(
            "font-size: 16px;font-family: Times New Roman ;padding: 3px;font-weight:bold; "
        )
        self.radio_button_2.setStyleSheet(
            "font-size: 16px;font-family: Times New Roman ;padding: 3px;font-weight:bold; "
        )
        
        radio_button_layout = QHBoxLayout()
        radio_button_layout.addWidget(self.radio_button_0)
        radio_button_layout.addWidget(self.radio_button_1)
        radio_button_layout.addWidget(self.radio_button_2)
        right_layout.addLayout(radio_button_layout)
        self.radio_button_0.clicked.connect(self.update_tempdata)
        self.radio_button_1.clicked.connect(self.update_tempdata)
        self.radio_button_2.clicked.connect(self.update_tempdata)
        # Create a horizontal layout for "Previous" and "Next" buttons
        button_layout = QHBoxLayout()

        self.next_button = QPushButton("Next>>", self)
        self.previous_button = QPushButton("<<Previous", self)
        # self.next_button.clicked.connect(self.show_next_review)
        # self.previous_button.clicked.connect(self.show_previous_review)
        self.next_button.clicked.connect(self.next_review)
        self.previous_button.clicked.connect(self.previous_review)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.next_button)
        # self.next_review()

        right_layout.addLayout(button_layout)

        self.next_button.setStyleSheet(
            "font-size: 16px; background-color: #4CAF50; font-family: Poppins; padding: 5px; color: white; font-weight: bold;"
        )
        self.previous_button.setStyleSheet(
            "font-size: 16px; background-color: #4CAF50; font-family: Poppins; padding: 5px; color: white; font-weight: bold"
        )
        self.save_button = QPushButton("Save Progress", self)
        self.save_button.clicked.connect(self.save_progress)
        right_layout.addWidget(self.save_button)
        self.save_button.setStyleSheet(
            "font-size: 16px; background-color: #008CBA;font-family: Poppins ;padding: 5px; color: white;font-weight:bold;"
        )
        
        self.radio_button_0.setEnabled(False)
        self.radio_button_1.setEnabled(False)
        self.radio_button_2.setEnabled(False)
        self.next_button.setEnabled(False)
        self.previous_button.setEnabled(False)
        self.save_button.setEnabled(False)

    def previous_review(self):
        if self.index > 0:
            self.index = self.index - 1
            self.next_button.setEnabled(True)

            if self.index == 0:
                self.previous_button.setEnabled(False)

            if hasattr(self, "data") and hasattr(self, "temp_data"):
                review = self.data.iloc[self.index, 0]
                highlighted_review = highlight_privacy_keywords(review, self.privacy_keywords)
                self.review_text.clear()
                self.review_text.setHtml(highlighted_review)

                # Retrieve the annotation for this review or set a default value
                annotation = self.temp_data[self.temp_data["review"] == review]["annotation"].values
                if len(annotation) > 0:
                    # Set the radio button based on the annotation (as an integer)
                    self.annotation_group.button(int(annotation[0])).setChecked(True)
                else:
                    # Set a default value (e.g., 0) or uncheck all radio buttons
                    for button_id in [0, 1, 2]:
                        self.annotation_group.button(button_id).setChecked(False)

    def next_review(self):
        
        if self.index <=len(self.data)-1:
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False) 

        if self.next_button.isEnabled():
            self.index=self.index+1
            print('index next ',self.index)
            
            if hasattr(self, "data") and hasattr(self, "temp_data"):
                
                
                # Increment the index
                while self.index < len(self.data):
                    review = self.data.iloc[self.index, 0]
                    if review not in self.temp_data["review"].values:
                        break

                if self.index < len(self.data):
                    review = self.data.iloc[self.index, 0]
                    highlighted_review = highlight_privacy_keywords(review, self.privacy_keywords)
                    self.review_text.clear()
                    self.review_text.setHtml(highlighted_review)

                    # Check if any radio button is selected
                    annotation = self.annotation_group.checkedId()
                    if annotation == -1:
                        annotation = 0  # Set a default value if none is selected

                    # Update the annotation for the previous review
                    
                    prev_review = self.data.iloc[self.index-1, 0]
                    # self.temp_data.loc[self.temp_data["review"] == prev_review, "annotation"] = annotation
                    self.temp_data.loc[self.index,'review']=review
                    self.temp_data.loc[self.index,'annotation']=annotation
                    print(self.temp_data)
                    # Uncheck all radio buttons
                    for button_id in [0, 1, 2]:
                        self.annotation_group.button(button_id).setChecked(False)
                else:
                    QMessageBox.information(self, "Info", "All reviews annotated!")
                    self.save_progress()


    def update_tempdata(self):
        if self.index >= 0 and self.index < len(self.data):
            annotation = self.annotation_group.checkedId()
            if annotation == -1:
                annotation = 0  # Set a default value if none is selected
            self.temp_data.at[self.index, 'annotation'] = annotation


    def load_excel_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx);;All Files (*)",
            options=options,
        )
        if file_path:
            self.current_file = file_path
            # Specify the folder name
            folder_name = "Annotated data"
            # Create the folder if it doesn't exist
            pathlib.Path(folder_name).mkdir(parents=True, exist_ok=True)
            self.temp_file = os.path.join(folder_name, f"temp_{os.path.basename(file_path)}")
            self.load_data()
            self.load_temp_data()
            self.load_existing_annotations()

            self.radio_button_0.setEnabled(True)
            self.radio_button_1.setEnabled(True)
            self.radio_button_2.setEnabled(True)
            self.next_button.setEnabled(True)
            self.previous_button.setEnabled(True)
            self.save_button.setEnabled(True)

            QMessageBox.information(self, "Info", "File loaded successfully")



    def save_progress(self):
        self.temp_data.to_excel(self.temp_file, index=False)
        QMessageBox.information(self, "Info", "Progress saved to temp_reviews.xlsx")

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    annotator = ReviewAnnotator()
    annotator.show()
    sys.exit(app.exec_())