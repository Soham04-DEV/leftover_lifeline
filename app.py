from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Function to initialize the database
def init_db():
    try:
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS survey_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_or_firm TEXT,
                age INTEGER,
                source_of_waste TEXT,
                home_waste_per_week INTEGER,
                home_types_of_waste TEXT,
                home_compost_aware TEXT,
                home_pay_for_collection TEXT,
                home_tools_needed TEXT,
                hotel_waste_per_day INTEGER,
                hotel_types_of_waste TEXT,
                hotel_monitor_system TEXT,
                hotel_donate_food TEXT,
                hotel_challenges TEXT,
                industry_waste_per_day INTEGER,
                industry_stage_of_waste TEXT,
                industry_types_of_waste TEXT,
                industry_current_methods TEXT,
                industry_reduction_steps TEXT,
                farm_percentage_waste INTEGER,
                farm_causes_of_waste TEXT,
                farm_unharvested_food TEXT,
                farm_aware_of_initiatives TEXT,
                farm_support_needed TEXT,
                vendor_waste_per_day INTEGER,
                vendor_reasons_for_waste TEXT,
                vendor_management_methods TEXT,
                vendor_interested_in_service TEXT,
                vendor_support_needed TEXT,
                other_description TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized and 'survey_responses' table is ready.")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")

# Call the function to initialize the database when the app starts
init_db()

# A simple route to check if the backend is running
@app.route('/', methods=['GET'])
def home():
    return "The backend server is running!"

# Route to handle form submission
@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    try:
        data = request.json
        print("Received survey data:", data)

        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO survey_responses (
                name_or_firm, age, source_of_waste,
                home_waste_per_week, home_types_of_waste, home_compost_aware, home_pay_for_collection, home_tools_needed,
                hotel_waste_per_day, hotel_types_of_waste, hotel_monitor_system, hotel_donate_food, hotel_challenges,
                industry_waste_per_day, industry_stage_of_waste, industry_types_of_waste, industry_current_methods, industry_reduction_steps,
                farm_percentage_waste, farm_causes_of_waste, farm_unharvested_food, farm_aware_of_initiatives, farm_support_needed,
                vendor_waste_per_day, vendor_reasons_for_waste, vendor_management_methods, vendor_interested_in_service, vendor_support_needed,
                other_description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name_or_firm'), data.get('age'), data.get('source_of_waste'),
            data.get('home_waste_per_week'), data.get('home_types_of_waste'), data.get('home_compost_aware'), data.get('home_pay_for_collection'), data.get('home_tools_needed'),
            data.get('hotel_waste_per_day'), data.get('hotel_types_of_waste'), data.get('hotel_monitor_system'), data.get('hotel_donate_food'), data.get('hotel_challenges'),
            data.get('industry_waste_per_day'), data.get('industry_stage_of_waste'), data.get('industry_types_of_waste'), data.get('industry_current_methods'), data.get('industry_reduction_steps'),
            data.get('farm_percentage_waste'), data.get('farm_causes_of_waste'), data.get('farm_unharvested_food'), data.get('farm_aware_of_initiatives'), data.get('farm_support_needed'),
            data.get('vendor_waste_per_day'), data.get('vendor_reasons_for_waste'), data.get('vendor_management_methods'), data.get('vendor_interested_in_service'), data.get('vendor_support_needed'),
            data.get('other_description')
        ))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Survey submitted successfully!'})

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500

    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'success': False, 'message': f'An unexpected error occurred: {e}'}), 500

# New route to view the data
@app.route('/view-data', methods=['GET'])
def view_data():
    try:
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("SELECT * FROM survey_responses")
        rows = c.fetchall()
        conn.close()
        return jsonify(rows)
    except sqlite3.Error as e:
        print(f"Database error during data retrieval: {e}")
        return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'success': False, 'message': f'An unexpected error occurred: {e}'}), 500