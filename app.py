from flask import Flask, render_template, session
import requests
from logic.transitLogic import prepare_divisional_chart

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session usage


@app.route('/transit')
def transit():
    # Fetch current planetary data from the internal API
    try:
        response = requests.get('http://127.0.0.1:5000/api/astronihar/d1')
        data = response.json()
    except Exception as e:
        return f"Error fetching planetary data: {e}"

    # Get ascendant zodiac number (1=Aries, ..., 12=Pisces)
    asc_zodiac = data['ascendant']['zodiac']
    asc_zodiac_number = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ].index(asc_zodiac) + 1

    # Prepare D1 chart using logic
    d1_chart = prepare_divisional_chart(data['planets'], asc_zodiac_number)

    # Pass the chart into the template
    return render_template('transit.html', divisionals={'D1': d1_chart})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
