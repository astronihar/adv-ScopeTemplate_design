from flask import Flask, render_template
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key'

zodiac_list = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

@app.route('/transit')
def transit():
    try:
        response = requests.get('http://127.0.0.1:5000/api/astronihar/d1')
        data = response.json()
    except Exception as e:
        return f"Error fetching planetary data: {e}"

    asc_zodiac = data['ascendant']['zodiac']
    asc_index = zodiac_list.index(asc_zodiac)  # 0-based index
    asc_house = 1  # Ascendant always goes into 1st house

    # Build rotated zodiac chart so 1st house = ascendant's zodiac
    rotated_zodiacs = zodiac_list[asc_index:] + zodiac_list[:asc_index]
    rotated_zodiac_numbers = [(zodiac_list.index(z) + 1) for z in rotated_zodiacs]  # Zodiac number 1–12

    # Create 12-house chart with zodiac numbers
    chart = {}
    for i in range(1, 13):
        chart[i] = {
            'zodiac': rotated_zodiac_numbers[i - 1],  # 1-based zodiac number
            'planets': []
        }

    # Add Ascendant
    chart[1]['planets'].append("Ascendant")

    # Add planets with zodiac number and degree
    for planet, info in data['planets'].items():
        try:
            planet_zodiac = info['zodiac']
            degree = round(info['degree'], 5)
            planet_zod_index = zodiac_list.index(planet_zodiac)

            # Find which house this zodiac falls into from ascendant
            house_pos = (planet_zod_index - asc_index) % 12 + 1
            zodiac_number = zodiac_list.index(planet_zodiac) + 1
            chart[house_pos]['planets'].append(f"{planet}^{degree} ({zodiac_number})")
        except Exception as e:
            continue

    return render_template('transit.html', divisionals={'D1': chart})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
