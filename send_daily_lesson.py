import os
import asyncio
from datetime import datetime
from telegram import Bot
from openai import OpenAI
import pytz
import httpx

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Tbilisi timezone
TBILISI_TZ = pytz.timezone('Asia/Tbilisi')

def generate_daily_lesson() -> str:
    """Generate a single daily micro-lesson in Georgian"""
    
    prompt = """შექმენი ერთი დღიური მიკრო-გაკვეთილი ქართულ ენაზე, რომელიც აგებს ღირებულ ადამიანურ უნარს.

ᲛᲙᲐᲪᲠᲘ ᲬᲔᲡᲔᲑᲘ:
- მხოლოდ ქართული ენა
- სიგრძე: 180-230 სიტყვა
- БЕЗ EMOJI-ების გარეშე
- БЕЗ მოტივაციის, ფილოსოფიის ან ზოგადი საუბრის
- მხოლოდ პრაქტიკული გამოყენება

ᲡᲢᲠᲣᲥᲢᲣᲠᲐ (მკაცრად დაიცავი):

1) დღის უნარი (მოკლე სათაური)

2) ძირითადი იდეა (2-3 მოკლე წინადადება)

3) რეალური მაგალითი (ბიზნესი ან ყოველდღიური ცხოვრება)

4) მიკრო-სავარჯიშო (შესრულებადი 5 წუთში)

5) ხშირი შეცდომა (რას აკეთებენ ადამიანები არასწორად)

6) ერთი სტრიქონიანი მოქმედება (ზუსტად ერთი წინადადება)

ᲣᲜᲐᲠᲔᲑᲘᲡ ᲙᲐᲢᲔᲒᲝᲠᲘᲔᲑᲘ (ბუნებრივად ცვალე):
- მოლაპარაკება
- კრიტიკული აზროვნება
- კომუნიკაცია
- გაყიდვები
- მარკეტინგული ფსიქოლოგია
- დროის მართვა
- გადაწყვეტილების მიღება
- სისტემური აზროვნება

NU დაუსვა კითხვები მკითხველს.
NU ახსენო რომ AI ხარ.
NU გაიმეორო უნარები ხშირად.

მიაწოდე ზუსტად ერთი გაკვეთილი."""

    try:
        # Initialize OpenAI client with explicit http_client
        http_client = httpx.Client()
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            http_client=http_client
        )
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "შენ ხარ ელიტური უნარების ინსტრუქტორი და მწვრთნელი. შენი მიზანია პრაქტიკული, სწრაფად გამოსაყენებელი მიკრო-გაკვეთილების შექმნა ქართულ ენაზე."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=1000
        )
        
        http_client.close()
        return response.choices[0].message.content
    
    except Exception as e:
        return f"შეცდომა გაკვეთილის გენერირებისას: {str(e)}"

async def send_lesson():
    """Send the daily micro-lesson"""
    try:
        print("Generating daily skill lesson...")
        lesson = generate_daily_lesson()
        
        # Initialize bot
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        print(f"Sending lesson to chat {CHAT_ID}...")
        await bot.send_message(
            chat_id=CHAT_ID,
            text=lesson,
            parse_mode=None
        )
        
        print("✅ Daily lesson sent successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

def main():
    """Main function"""
    if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY or not CHAT_ID:
        print("❌ Missing required environment variables!")
        print("Please set: TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, TELEGRAM_CHAT_ID")
        return
    
    print("📚 Starting Daily Skill Lesson Bot...")
    print(f"📅 Current time (Tbilisi): {datetime.now(TBILISI_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run the async function
    asyncio.run(send_lesson())

if __name__ == '__main__':
    main()
