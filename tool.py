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


class ReviewAnnotator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.annotation_group = None
        self.setWindowTitle("Review Annotator")
        self.setGeometry(100, 100, 1000, 800)
        self.current_file = None  # Track the currently loaded file
        self.temp_file = None  # Track the associated temp file
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
            self.temp_data = pd.read_excel(self.temp_file)
        else:
            self.temp_data = pd.DataFrame(columns=["review", "annotation"])

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
            "font-size: 15px; font-family: Times New Roman ; background-color: #e9e9e9;border: 1px solid #f7f7b7; border-radius: 8px;"
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
            4.Examples: Here are some examples to help you understand how to assign the labels:<br>
-If the review is advising or requestiing to update any privacy related feature of the app: Assign Label 1 (Privacy-Related Feature request).<br>
-If the review is reporting that their personal data was exposed due to a bug: Assign Label 2 (Privacy-Related Bug).<br>
-If the review is discussing the app's user interface and has no mention of privacy: Assign Label 0 (Not Privacy-Related).<br><br>
            <span style="font-weight: bold;font-size: 16px;">Examples:</span><br>
            - If the review is advising or requesting an update of a privacy-related feature: Assign Label 1.<br>
            - If the review reports that personal data was exposed due to a bug: Assign Label 2.<br>
            - If the review does not discuss any privacy-related aspects: Assign Label 0.<br>
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
            "font-size: 15px; font-family: Times New Roman ; background-color: #e9e9e9;border: 1px solid #f7f7c6; border-radius: 8px;"
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
        # Stylesheet for radio buttons (modify as needed)
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

       

        # add_file_button = QPushButton("Add File", self)
        # add_file_button.clicked.connect(self.load_excel_file)
        # right_layout.addWidget(add_file_button)
        
        self.show_next_review()

        # Create a horizontal layout for "Previous" and "Next" buttons
        button_layout = QHBoxLayout()

        next_button = QPushButton("Next>>", self)
        previous_button = QPushButton("<<Previous", self)
        next_button.clicked.connect(self.show_next_review)
        previous_button.clicked.connect(self.show_previous_review)
        button_layout.addWidget(previous_button)
        button_layout.addWidget(next_button)

        right_layout.addLayout(button_layout)

        next_button.setStyleSheet(
            "font-size: 16px; background-color: #4CAF50; font-family: Poppins; padding: 5px; color: white; font-weight: bold;"
        )
        previous_button.setStyleSheet(
            "font-size: 16px; background-color: #4CAF50; font-family: Poppins; padding: 5px; color: white; font-weight: bold"
        )
        save_button = QPushButton("Save Progress", self)
        save_button.clicked.connect(self.save_progress)
        right_layout.addWidget(save_button)
        save_button.setStyleSheet(
            "font-size: 16px; background-color: #008CBA;font-family: Poppins ;padding: 5px; color: white;font-weight:bold;"
        )

    def show_previous_review(self):
        if hasattr(self, "data") and hasattr(self, "temp_data"):
            while (
                self.index > 0
                and self.data.columns[0] in self.temp_data["review"].values
            ):
                self.index -= 1

            if self.index >= 0:
                self.index -= 1  # Go to the previous review
                review = self.data.iloc[self.index, 0]
                self.review_text.clear()
                self.review_text.insertPlainText(review)

                # Retrieve the annotation for this review
                annotation = self.temp_data[self.temp_data["review"] == review][
                    "annotation"
                ].values
                if len(annotation) > 0:
                    self.annotation_group.button(annotation[0]).setChecked(True)
                else:
                    # Uncheck all radio buttons in the group
                    for button_id in [0, 1, 2]:
                        self.annotation_group.button(button_id).setChecked(False)

    def show_next_review(self):
        if hasattr(self, "data") and hasattr(self, "temp_data"):
            while self.index < len(self.data):
                review = self.data.iloc[self.index, 0]
                if review not in self.temp_data["review"].values:
                    break
                self.index += 1

            if self.index < len(self.data):
                review = self.data.iloc[self.index, 0]
                self.review_text.clear()
                self.review_text.insertPlainText(review)

                # Check if any radio button is selected
                annotation = self.annotation_group.checkedId()
                if annotation == -1:
                    annotation = 0  # Set a default value if none is selected

                # Update the annotation for the current review
                self.temp_data.loc[self.temp_data.shape[0]] = [review, annotation]

                # Uncheck all radio buttons
                for button_id in [0, 1, 2]:
                    self.annotation_group.button(button_id).setChecked(False)
            else:
                QMessageBox.information(self, "Info", "All reviews annotated!")
                self.save_progress()





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
            self.temp_file = f"temp_{os.path.basename(file_path)}"
            self.load_data()
            self.load_temp_data()
            self.index = -1
            self.show_next_review()
            QMessageBox.information(self, "Info", "File loaded successfully")

    def save_progress(self):
        self.temp_data.to_excel(self.temp_file, index=False)
        QMessageBox.information(self, "Info", "Progress saved to temp_reviews.xlsx")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    annotator = ReviewAnnotator()
    annotator.show()
    sys.exit(app.exec_())