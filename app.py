from flask import Flask, request, render_template
import PyPDF2
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI  # v1.0+ export
from wordcloud import WordCloud, STOPWORDS
import matplotlib
# Use Agg backend for non-interactive plotting
matplotlib.use('Agg')
import matplotlib.pyplot as plt

load_dotenv()  # Load environment variables

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Fallback to OpenAI GPT if DeepSeek balance is insufficient and key is set
def fallback_to_openai(text):
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        return {"error": "OpenAI API key not found. Please set OPENAI_API_KEY to use fallback."}

    client = OpenAI(api_key=openai_key.strip())
    prompt = (
        "Please summarize the following text from one or multiple academic papers in three paragraphs:\n"
        "1. A summary of the key findings across one or all papers in 2–3 sentences.\n"
        "2. A description of the methodologies used across one or all papers in 2–3 sentences.\n"
        "3. An identification of gaps in research across one or all papers in 2–3 sentences.\n"
        "Additionally, in a fourth paragraph, suggest 1–2 research questions for further investigation based on the identified gaps.\n"
        "Do not include headings like 'Key Findings', 'Methodologies', 'Gaps in Research', or 'Suggested Research Questions' in the response.\n\n"
        f"{text[:4000]}"
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7
        )
        content = resp.choices[0].message.content
        parts = [p.strip() for p in content.split("\n\n")]
        return {
            "key_findings": parts[0] if parts else "No findings extracted.",
            "methodologies": parts[1] if len(parts) > 1 else "No methodologies extracted.",
            "gaps": parts[2] if len(parts) > 2 else "No gaps extracted.",
            "research_questions": parts[3] if len(parts) > 3 else "No research questions suggested."
        }
    except Exception as e:
        return {"error": f"OpenAI fallback failed: {str(e)}"}

# DeepSeek API function
def process_with_llm(text):
    ds_key = os.getenv("DEEPSEEK_API_KEY")
    if not ds_key:
        return {"error": "DeepSeek API key not found. Set DEEPSEEK_API_KEY in environment variables."}

    api_url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {ds_key.strip()}",
        "Content-Type": "application/json"
    }

    prompt = (
        "Summarize the following text from multiple academic papers in three paragraphs:\n"
        "1. A summary of the key findings across all papers in 2–3 sentences.\n"
        "2. A description of the methodologies used across all papers in 2–3 sentences.\n"
        "3. An identification of gaps in research across all papers in 2–3 sentences.\n"
        "Additionally, in a fourth paragraph, suggest 1–2 research questions for further investigation based on the identified gaps.\n"
        "Do not include headings like 'Key Findings', 'Methodologies', 'Gaps in Research', or 'Suggested Research Questions' in the response.\n\n"
        f"Text: {text[:4000]}"
    )

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400,
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 402:
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                return fallback_to_openai(text)
            return {"error": (
                "❗️ Insufficient DeepSeek balance. Please top up at https://dashboard.deepseek.com/billing."
            )}

        response.raise_for_status()
        result = response.json().get('choices', [])[0].get('message', {}).get('content', '')
        sections = [s.strip() for s in result.split("\n\n")]
        return {
            "key_findings": sections[0] if sections else "No findings extracted.",
            "methodologies": sections[1] if len(sections) > 1 else "No methodologies extracted.",
            "gaps": sections[2] if len(sections) > 2 else "No gaps extracted.",
            "research_questions": sections[3] if len(sections) > 3 else "No research questions suggested."
        }
    except requests.exceptions.HTTPError:
        return {"error": f"DeepSeek API error {response.status_code}: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except (KeyError, IndexError) as e:
        return {"error": f"Error parsing response: {str(e)}"}

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Function to generate a word cloud
def generate_word_cloud(text):
    # Combine stop words
    stopwords = set(STOPWORDS)
    stopwords.update(["study", "research", "paper", "papers"])  # Add common academic words to exclude

    # Generate word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=stopwords,
        min_font_size=10
    ).generate(text)

    # Save the word cloud to a file
    wordcloud_path = os.path.join(app.config['STATIC_FOLDER'], 'wordcloud.png')
    plt.figure(figsize=(8, 4), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(wordcloud_path, format='png')
    plt.close()

    return '/static/wordcloud.png'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files')
    if not files or not all(file.filename.lower().endswith('.pdf') for file in files if file):
        return render_template('index.html', error="Please upload one or more PDF files")

    combined_text = ""
    for file in files:
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            text = extract_text_from_pdf(filepath)
            os.remove(filepath)
            if text.startswith("Error"):
                return render_template('index.html', error=f"Error processing {file.filename}: {text}")
            combined_text += f"\n\nPaper: {file.filename}\n{text}"

    if not combined_text.strip():
        return render_template('index.html', error="No valid content extracted from the uploaded files")

    summary = process_with_llm(combined_text)
    if "error" in summary:
        return render_template('index.html', error=summary["error"])

    # Combine summary text for word cloud
    summary_text = " ".join([
        summary['key_findings'],
        summary['methodologies'],
        summary['gaps'],
        summary['research_questions']
    ])

    # Generate word cloud
    wordcloud_url = generate_word_cloud(summary_text)

    return render_template('results.html', 
        key_findings=summary['key_findings'],
        methodologies=summary['methodologies'],
        gaps=summary['gaps'],
        research_questions=summary['research_questions'],
        wordcloud_url=wordcloud_url
    )

if __name__ == '__main__':
    app.run(debug=True)