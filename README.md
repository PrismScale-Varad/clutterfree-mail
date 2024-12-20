 # Clutter Free Mail - Your Newsletter Digest Tool

## A tool that simplifies email newsletter management by extracting, analyzing, and summarizing relevant content from newsletters into a concise weekly summary

### Tech Stack:
- Python
- imaplib
- email
- HuggingFace Inference API:
    - ilsilfverskiold/tech-keywords-extractor
    - facebook/bart-large-mnli
    - facebook/bart-large-cnn
- TinyDB

### Execution Flow (tentative): 
- Fetch past week's emails based on config.json **[imaplib]**
- Filter through the email metadata to only keep newsletters **[email]**
- Fetch individual newsletter, run a summarizer model on each individual article **[facebook/bart-large-cnn]**
- Save the title, summary, thumbnail and link of the newsletter **[TinyDB]**
- For each article in TinyDB, extract keywords **[ilsilfverskiold/tech-keywords-extractor]** and categorise them **[facebook/bart-large-mnli]**
- Save the keywords and category scores of each article into TinyDB
- Based on category fit scores **[facebook/bart-large-mnli]**, rank each newsletter
- Send 

### File Structure
```
|- main.py
|- email_handler.py
|- process_articles.py
|- db.py
|- data.json
|- config.json
|- requirements.txt
|- README.md
```