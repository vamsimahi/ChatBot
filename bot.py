from flask import Flask, render_template, request, jsonify
import pandas as pd
import difflib

app = Flask(__name__)

# Load both datasets
questions_df = pd.read_csv(r"C:\Users\Mahendra\Desktop\boot\datasets\conversationo.csv")
menu_df = pd.read_csv(r"C:\Users\Mahendra\Desktop\boot\datasets\Menu Items.csv")

# Clean up column names (trim spaces)
questions_df.columns = questions_df.columns.str.strip()
menu_df.columns = menu_df.columns.str.strip()

# Ensure required columns exist
if "Question" not in questions_df.columns or "Answer" not in questions_df.columns:
    raise ValueError("Questions dataset must contain 'Question' and 'Answer' columns.")

if "Section" not in menu_df.columns or "Item" not in menu_df.columns or "Price" not in menu_df.columns:
    raise ValueError("Menu dataset must contain 'Section', 'Item', and 'Price' columns.")

# Function to get the closest answer for general queries
def get_answer(user_input):
    user_input = str(user_input).strip().lower()
    questions = questions_df['Question'].astype(str).tolist()
    closest_match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)

    if closest_match:
        index = questions.index(closest_match[0])
        return questions_df.iloc[index]['Answer']
    else:
        return "I'm sorry, I don't have an answer for that."

# Function to get the full menu
def get_full_menu():
    sections = menu_df["Section"].unique()
    menu_text = "**📜 Menu Sections:**\n" + "\n".join(f"- {section}" for section in sections)
    menu_text += "\n\n(Ask for a section to see details, e.g., 'Show me Desserts')"
    return menu_text

# Function to fetch menu details (limited to 10 items per section)
def get_menu_details(section_name):
    section_name = str(section_name).strip().lower()
    
    # Filter menu by section and limit to first 10 items
    filtered_menu = menu_df[menu_df["Section"].str.lower() == section_name].head(10)

    if not filtered_menu.empty:
        menu_list = [f"🍽️ {row['Item']} - ₹{row['Price']}" for _, row in filtered_menu.iterrows()]
        return "\n".join(menu_list) + "\n\n(Top 10 items)"
    else:
        return "Sorry, this section is not available."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['message'].strip().lower()

    # Check if user is asking for the full menu
    if "menu" in user_input:
        response = get_full_menu()
    else:
        # Check if the user is asking for a specific section
        menu_sections = menu_df["Section"].str.lower().unique()
        matched_sections = [section for section in menu_sections if section in user_input]

        if matched_sections:
            response = get_menu_details(matched_sections[0])  # Show menu for the first matched section
        else:
            response = get_answer(user_input)

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
