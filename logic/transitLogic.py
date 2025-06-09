# logic/transitLogic.py

zodiac_to_number = {
    'Aries': 1, 'Taurus': 2, 'Gemini': 3, 'Cancer': 4,
    'Leo': 5, 'Virgo': 6, 'Libra': 7, 'Scorpio': 8,
    'Sagittarius': 9, 'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12
}

def prepare_divisional_chart(planets, asc_zodiac_number):
    chart = {}
    for i in range(1, 13):
        zodiac_num = ((asc_zodiac_number + i - 2) % 12) + 1
        chart[i] = {"planets": [], "zodiac": zodiac_num}

    chart[1]["planets"].append("Asc")

    zodiac_to_number = {
        'Aries': 1, 'Taurus': 2, 'Gemini': 3, 'Cancer': 4,
        'Leo': 5, 'Virgo': 6, 'Libra': 7, 'Scorpio': 8,
        'Sagittarius': 9, 'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12
    }

    for planet, data in planets.items():
        zodiac = data['zodiac']
        zodiac_num = zodiac_to_number[zodiac]
        house_num = ((zodiac_num - asc_zodiac_number) % 12) + 1
        chart[house_num]["planets"].append(planet)

    return chart