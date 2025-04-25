## Overview

The Literature Review Assistant is a web application designed to help researchers and students streamline the process of reviewing academic papers. Built with Flask, this app allows users to upload multiple PDF papers, extracts their text, and generates a summarized analysis using AI (via DeepSeek API with OpenAI as a fallback). The app provides key findings, methodologies, gaps in research, suggested research questions, and a word cloud visualization of key themes. The results can be exported as a PDF for easy sharing and inclusion in research workflows.

This project showcases my skills in web development (Flask, HTML, CSS, JavaScript), API integration (DeepSeek, OpenAI), text processing (PyPDF2), and data visualization (wordcloud, matplotlib). It was developed as part of my portfolio to demonstrate my ability to build practical tools for academic research.

## Features


- **Multiple PDF Upload**: Upload one or more PDF papers to analyze simultaneously.



- **AI-Powered Summarization**: Uses DeepSeek API (with OpenAI fallback) to generate summaries, including:


  - Key Findings



  - Methodologies



  - Gaps in Research



  - Suggested Research Questions


- **Word Cloud Visualization**: Generates a word cloud to highlight key themes and terms from the summary.


- **Export to PDF**: Download the analysis as a two-page PDF, with Suggested Research Questions and the word cloud on the second page.


- **Dark/Light Mode**: Toggle between dark and light themes for better readability.


- **Font Size Adjustment**: Adjust font size for accessibility.



- **Error Handling**: Robust error handling for API failures, invalid file uploads, and more.


## Tech Stack


- **Backend**: Flask (Python)



- **Frontend**: HTML, CSS, JavaScript



- **Text Extraction**: PyPDF2



- **AI Integration**: DeepSeek API, OpenAI API (fallback)



- **Visualization**: wordcloud, matplotlib



- **Environment Management**: python-dotenv



- **Dependencies**: Managed via requirements.txt
  

## Setup Instructions

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.8+

- Git

- A DeepSeek API key (and optionally an OpenAI API key for fallback)

  - Sign up for DeepSeek at dashboard.deepseek.com.

  - (Optional) Sign up for OpenAI at platform.openai.com.


### Steps

1. Clone the Repository:

```bash
git clone https://github.com/your-username/Literature-Review-Assistant.git
cd Literature-Review-Assistant
```


2. Set Up a Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


3. Install Dependencies:
```bash
pip install -r requirements.txt
```


4. Configure Environment Variables: Create a .env file in the project root and add your API keys:
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional, for fallback
```


5. Run the Application:
```bash
python app.py
```
The app will run at http://127.0.0.1:5000.


## Usage


1. **Access the App**: Open your browser and go to http://127.0.0.1:5000.


2. **Upload Papers**:


 - Click the file input field to select one or more PDF papers.

 - You can hold Ctrl/Cmd to select multiple files or drag and drop them.


3. **Analyze**:

 - Click the "Analyze" button to process the papers.

 - The app will extract text, send it to the DeepSeek API (or OpenAI if DeepSeek fails), and generate a summary.


4. **View Results**:


- The results page displays:

  - Key Findings


  - Methodologies



  - Gaps in Research



  - Suggested Research Questions



  - A word cloud of key themes



- Use the theme toggle (🌓) to switch between dark and light modes.



- Adjust font size using the dropdown (A-, A, A+).



5. **Export to PDF**:

- Click "Download as PDF" to save the results as a two-page PDF.


- The PDF includes Suggested Research Questions and the word cloud on the second page.


## Project Structure

```
Literature-Review-Assistant/
├── app.py                  # Main Flask application
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (not tracked)
├── .gitignore              # Files to ignore in Git
├── README.md               # Project documentation
├── static/                 # Static files (e.g., wordcloud.png)
├── templates/              # HTML templates
│   ├── index.html          # Upload page
│   └── results.html        # Results page
└── uploads/                # Temporary folder for uploaded PDFs (not tracked)
```

## Demo Video

Below is a GIF demonstrating how the Literature Review Assistant works, from uploading papers to viewing results and exporting to PDF:


![Literature_Review_Assistant](https://github.com/user-attachments/assets/5e49f7bf-a566-4d00-82bf-424ed8590af0)



## Challenges and Solutions

- **Threading Issue with Matplotlib on macOS**:

  - **Challenge**: Matplotlib crashed when generating the word cloud due to GUI threading issues on macOS.

  - **Solution**: Switched to the Agg backend (matplotlib.use('Agg')) to ensure non-interactive plotting, making it compatible with Flask’s threading model.

- **Dark Mode in PDF Output**:

  - **Challenge**: The PDF output rendered in dark mode, making it unreadable.

  - **Solution**: Updated the @media print styles to override dark mode variables, ensuring a light theme (white background, black text) in the PDF.

- **API Cost Management**:

  - **Challenge**: DeepSeek API has usage limits, which could lead to failures.

  - **Solution**: Implemented a fallback to OpenAI API when DeepSeek fails (e.g., due to insufficient balance).

## Future Improvements

- **Interactive Visualizations**: Add interactivity to the word cloud (e.g., hover to see word frequency) using D3.js.

- **Concept Maps**: Generate concept maps to show relationships between key terms using NLP and graph libraries.

- **Citation Generation**: Extract and format citations from the uploaded papers.

- **Server-Side PDF Generation**: Use weasyprint for more consistent PDF output across browsers.

- **User Authentication**: Add user accounts to save and manage analyses.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or collaboration, feel free to reach out:

GitHub: [samaneh-shn](https://github.com/samaneh-shn)

Email: shirinnezhad.samaneh@gmail.com
