import discord
import cloudscraper  # Import cloudscraper to handle Cloudflare
from datetime import datetime
import time
from config import TOKEN, MAX_VIEWS

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True  # Enables reading message content

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!offerupviews'):
        try:
            parts = message.content.split(' ')
            if len(parts) < 3:
                await message.channel.send("Usage: `!offerupviews <number_of_views> <offerup_listing_url>`")
                return

            number_of_views = int(float(parts[1]))
            link = parts[2]

            if number_of_views > MAX_VIEWS:
                await message.channel.send(f"Maximum allowed views is {MAX_VIEWS}")
                return

            embed = discord.Embed(
                title='OfferUp Views Bot',
                description=f'Adding {number_of_views} views...',
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='OfferUp Link', value=link)
            await message.channel.send(embed=embed)

            # Initialize Cloudscraper to bypass Cloudflare
            scraper = cloudscraper.create_scraper()

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Referer': 'https://offerup.com',
                'DNT': '1'
            }

            successful_views = 0
            for i in range(number_of_views):
                try:
                    response = scraper.get(link, headers=headers, timeout=10)
                    if response.status_code == 200:
                        successful_views += 1
                        print(f"View {successful_views} added successfully.")
                    else:
                        print(f"Failed to add view {i + 1}, status code: {response.status_code}")

                except cloudscraper.exceptions.CloudflareChallengeError as e:
                    print(f"Cloudflare challenge failed: {e}")
                    break
                except Exception as e:
                    print(f"Error occurred: {e}")
                
                # Optional delay between requests
                time.sleep(1)

            embed = discord.Embed(
                title='OfferUp Views Bot',
                description=f'Successfully added {successful_views} views.',
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='OfferUp Link', value=link)
            await message.channel.send(embed=embed)

        except Exception as e:
            await message.channel.send(f"Error: {e}")

client.run(TOKEN)
