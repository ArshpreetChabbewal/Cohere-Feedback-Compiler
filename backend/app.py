from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import cohere
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app) 

co = cohere.Client(os.getenv('COHERE_API_KEY'))

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    reviews_df = pd.read_csv(file)
    if 'review' not in reviews_df.columns:
        return jsonify({'error': 'CSV file must have a "review" column'}), 400

    reviews = reviews_df['review'].tolist()
    individual_summaries = [summarize_feedback(review) for review in reviews]
    overall_summary = summarize_feedback(" ".join(reviews))

    summaries_df = pd.DataFrame({
        'review': reviews,
        'summary': individual_summaries
    })
    summaries_df['overall_summary'] = overall_summary

    output_file = 'summaries.csv'
    summaries_df.to_csv(output_file, index=False)

    return jsonify({
        'individual_summaries': individual_summaries,
        'overall_summary': overall_summary,
        'download_url': output_file
    })

def summarize_feedback(feedback, max_tokens=100):
    prompt = f"Summarize the following customer feedback:\n\n{feedback}\n\nSummary:"
    
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7,
        stop_sequences=["Summary:"]
    )
    
    summary = response.generations[0].text.strip()
    return summary

@app.route('/summaries.csv', methods=['GET'])
def download_file():
    return send_from_directory('.', 'summaries.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
