# help_commands.py

from datetime import datetime
import discord

def get_help_embed():
    embed = discord.Embed(
        title="Bot Command Help",
        description="Here's a list of all commands available across our bots.",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    # eBay bot command with updated command name
    embed.add_field(
        name="eBay Bot Commands",
        value="Commands for managing views on eBay listings.",
        inline=False
    )
    embed.add_field(
        name="!views <number_of_views> <ebay_listing_url>",
        value="Adds the specified number of views to an eBay listing.",
        inline=False
    )
    
    # Mercari bot commands, if any specific commands are needed
    embed.add_field(
        name="Mercari Bot Commands",
        value="Commands for managing views on Mercari listings.",
        inline=False
    )
    embed.add_field(
        name="!mercariviews <number_of_views> <mercari_listing_url>",
        value="Adds the specified number of views to a Mercari listing.",
        inline=False
    )
    
    # OfferUp bot commands
    embed.add_field(
        name="OfferUp Bot Commands",
        value="Commands for managing views on OfferUp listings.",
        inline=False
    )
    embed.add_field(
        name="!offerupviews <number_of_views> <offerup_listing_url>",
        value="Adds the specified number of views to an OfferUp listing.",
        inline=False
    )
    
    # General bot commands
    embed.add_field(
        name="General Commands",
        value="Commands that apply across all bots.",
        inline=False
    )
    embed.add_field(
        name="!help",
        value="Displays this help message with a list of available commands.",
        inline=False
    )

    return embed
