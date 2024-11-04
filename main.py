import discord
import cloudscraper
import random
import time
from datetime import datetime
from config import TOKEN, MAX_VIEWS
from help_commands import get_help_embed  # Import the help function for help command

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True  # Enables reading message content

client = discord.Client(intents=intents)

# User-Agent rotation list
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Help command
    if message.content.startswith('!help'):
        embed = get_help_embed()
        await message.channel.send(embed=embed)

    # eBay views command
    elif message.content.startswith('!views'):
        await handle_views_command(message, platform="eBay", referer="https://www.ebay.com/")

    # Mercari views command
    elif message.content.startswith('!mercariviews'):
        await handle_views_command(message, platform="Mercari", referer="https://mercari.com")

    # OfferUp views command
    elif message.content.startswith('!offerupviews'):
        await handle_views_command(message, platform="OfferUp", referer="https://offerup.com")

async def handle_views_command(message, platform, referer):
    """Generic handler for views commands."""
    try:
        parts = message.content.split(' ')
        if len(parts) < 3:
            await message.channel.send(f"Usage: `!{platform.lower()}views <number_of_views> <listing_url>`")
            return

        number_of_views = int(parts[1])
        link = parts[2]

        if number_of_views > MAX_VIEWS:
            await message.channel.send(f"Maximum allowed views is {MAX_VIEWS}")
            return

        embed = discord.Embed(
            title=f'{platform} Views Bot',
            description=f'Adding {number_of_views} views to {link}...',
            timestamp=datetime.utcnow()
        )
        await message.channel.send(embed=embed)

        # Initialize Cloudscraper
        scraper = cloudscraper.create_scraper()
        successful_views = 0

        for i in range(number_of_views):
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Referer': referer,
                'DNT': '1',
                'Connection': 'keep-alive'
            }

            try:
                response = scraper.get(link, headers=headers)
                if response.status_code == 200:
                    successful_views += 1
                    print(f"{platform} view {successful_views} added successfully.")
                else:
                    print(f"Failed to add {platform} view {i + 1}, status code: {response.status_code}")
                    if response.status_code == 503:
                        print("503 Service Unavailable - Server might be blocking requests.")
                        break

            except cloudscraper.exceptions.CloudflareChallengeError as e:
                print(f"Cloudflare challenge failed for {platform}: {e}")
                break
            except Exception as e:
                print(f"Error occurred for {platform}: {e}")

            # Optional delay to prevent rate limiting
            time.sleep(1)

        # Success message
        embed = discord.Embed(
            title=f'{platform} Views Bot',
            description=f'Successfully added {successful_views} views.',
            timestamp=datetime.utcnow()
        )
        await message.channel.send(embed=embed)

    except ValueError:
        await message.channel.send(f"Please provide a valid number of views for {platform}.")
    except IndexError:
        await message.channel.send(f"Usage: `!{platform.lower()}views <number_of_views> <listing_url>`")
    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")
        print(f"Error: {e}")

client.run(TOKEN)
