import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

BOT_COLOR = discord.Color.gold()

class FreelancerBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True  
        intents.members = True  
        super().__init__(command_prefix="!", intents=intents)
        self.user_profiles = {}
        self.user_xp = {}
        self.daily_challenges = ["Build a landing page", "Create a Python script", "Design a logo"]

    async def on_ready(self):
        print(f'\U0001F680 Bot is online as {self.user}!')
        try:
            await self.tree.sync()  # Ensure commands are synced with Discord
            print("\u2705 Commands synced successfully!")
        except Exception as e:
            print(f"\u26A0\uFE0F Error syncing commands: {e}")


bot = FreelancerBot()


@bot.tree.command(name="help", description="List all available commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="\U0001F4D6 Freelancer Bot Commands", color=BOT_COLOR)
    embed.add_field(name="/about_me", value="Learn more about Santhosh Raj", inline=False)
    embed.add_field(name="/services", value="Explore offered services", inline=False)
    embed.add_field(name="/portfolio", value="View recent projects", inline=False)
    embed.add_field(name="/contact", value="Get in touch with Santhosh", inline=False)
    embed.add_field(name="/testimonials", value="Read client feedback", inline=False)
    embed.add_field(name="/tech_stack", value="Check out my tech skills", inline=False)
    embed.add_field(name="/latest_projects", value="See the latest completed projects", inline=False)
    embed.add_field(name="/freelancer_tips", value="Gain freelancing insights", inline=False)
    embed.add_field(name="/motivate", value="Get a motivational quote", inline=False)
    embed.add_field(name="/discounts", value="View ongoing offers", inline=False)
    embed.set_footer(text="Freelancer Bot - Your gateway to amazing projects!")
    
    await interaction.response.send_message(embed=embed)



@bot.tree.command(name="about_me", description="Learn more about me!")
async def about_me(interaction: discord.Interaction):
    await interaction.response.defer()

    embed = discord.Embed(
        title="👨‍💻 Meet Santhosh Raj",
        description="🚀 Full-Stack Developer | AI Enthusiast | Freelancer\n\n"
                    "💡 Expert in **Django, React, Next.js, AI, WebRTC & more!**\n\n"
                    "🎯 Let's build something amazing together!",
        color=BOT_COLOR
    )
    embed.set_thumbnail(url="https://discordbanners.vercel.app/static/img/profile_discord.jpg")  
    embed.set_image(url="https://discordbanners.vercel.app/static/img/banner.gif") 
    embed.set_footer(text="DEVIX Bot | Developed by Santhosh Raj")

    await interaction.followup.send(embed=embed, ephemeral=True)  

@bot.tree.command(name="set_profile", description="Set your profile information!")
async def set_profile(interaction: discord.Interaction, bio: str, skills: str):
    bot.user_profiles[interaction.user.id] = {"bio": bio, "skills": skills}
    await interaction.response.send_message("✅ Profile updated successfully!")

@bot.tree.command(name="view_profile", description="View your profile information!")
async def view_profile(interaction: discord.Interaction):
    profile = bot.user_profiles.get(interaction.user.id, {"bio": "Not set", "skills": "Not set"})
    embed = discord.Embed(title=f"👤 {interaction.user.name}'s Profile", color=BOT_COLOR)
    embed.add_field(name="Bio", value=profile["bio"], inline=False)
    embed.add_field(name="Skills", value=profile["skills"], inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily_challenge", description="Get a daily coding/design challenge!")
async def daily_challenge(interaction: discord.Interaction):
    challenge = random.choice(bot.daily_challenges)
    embed = discord.Embed(title="💡 Daily Challenge", description=challenge, color=BOT_COLOR)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="xp_status", description="Check your XP level!")
async def xp_status(interaction: discord.Interaction):
    xp = bot.user_xp.get(interaction.user.id, 0)
    embed = discord.Embed(title=f"🏆 {interaction.user.name}'s XP", description=f"XP: {xp}", color=BOT_COLOR)
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    bot.user_xp[message.author.id] = bot.user_xp.get(message.author.id, 0) + 10
    await bot.process_commands(message)

@bot.tree.command(name="quiz", description="Test your knowledge with a quiz!")
async def quiz(interaction: discord.Interaction):
    questions = {
        "What does HTML stand for?": "Hyper Text Markup Language",
        "What language is used for AI development?": "Python",
    }
    question, answer = random.choice(list(questions.items()))
    embed = discord.Embed(title="🎯 Quiz Time!", description=question, color=BOT_COLOR)
    await interaction.response.send_message(embed=embed)
    
    def check(msg):
        return msg.author == interaction.user and msg.content.lower() == answer.lower()
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        await msg.channel.send("✅ Correct Answer!")
    except:
        await msg.channel.send(f"❌ Time's up! The correct answer was: {answer}")

@bot.tree.command(name="ask", description="Ask an AI-powered question!")
async def ask(interaction: discord.Interaction, question: str):
    responses = ["That’s an interesting question!", "Let me think…", "I’m not sure, but I’ll find out!"]
    embed = discord.Embed(title="🤖 AI Response", description=random.choice(responses), color=BOT_COLOR)
    embed.set_image(url="https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="estimate", description="Get an estimated project price!")
async def estimate(interaction: discord.Interaction, project_type: str):
    prices = {"Website": "$500 - $5000", "AI Tool": "$1000 - $10000", "Mobile App": "$2000 - $15000"}
    embed = discord.Embed(title="💰 Project Price Estimate", description=f"**{project_type}** costs around {prices.get(project_type, 'Custom Pricing')}", color=BOT_COLOR)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="faq", description="Get answers to common questions!")
async def faq(interaction: discord.Interaction):
    faqs = ["How long does a project take? - Depends on complexity!", "Do you offer discounts? - Check /discounts"]
    embed = discord.Embed(title="📌 Frequently Asked Questions", description="\n".join(faqs), color=BOT_COLOR)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="motivate", description="Get a motivational quote!")
async def motivate(interaction: discord.Interaction):
    categories = ["Success", "Perseverance", "Innovation"]
    options = [discord.SelectOption(label=c, description=f"Quotes about {c}") for c in categories]
    select = discord.ui.Select(placeholder="Choose a category", options=options)
    
    async def callback(interaction):
        quotes = {"Success": "Success is not final, failure is not fatal...", "Perseverance": "Push yourself, because no one else will..."}
        embed = discord.Embed(title=f"💡 {interaction.data['values'][0]} Quote", description=quotes[interaction.data['values'][0]], color=BOT_COLOR)
        await interaction.response.send_message(embed=embed)

    select.callback = callback
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.send_message("Select a category:", view=view)


@bot.tree.command(name="services", description="See the services I offer!")
async def services(interaction: discord.Interaction):
    embed = discord.Embed(title="🌟 My Services", color=BOT_COLOR)
    embed.add_field(name="💻 Web Development", value="Building responsive, high-quality websites", inline=False)
    embed.add_field(name="🤖 AI & Automation", value="Smart AI solutions & automation tools", inline=False)
    embed.add_field(name="📡 Real-Time Apps", value="WebRTC & WebSockets integration", inline=False)
    embed.add_field(name="🎨 UI/UX Design", value="Crafting stunning and user-friendly interfaces", inline=False)
    embed.set_image(url="https://discordbanners.vercel.app/static/img/Thumbnail.png") 
    embed.set_footer(text="Need a project? Use /contact to reach out!")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="portfolio", description="Check out my recent projects!")
async def portfolio(interaction: discord.Interaction):
    embed = discord.Embed(title="🔗 My Portfolio", color=BOT_COLOR)
    embed.add_field(name="🔹 NextSeek", value="[🔗 Live Demo](https://yourportfolio.com/nextseek)", inline=False)
    embed.add_field(name="🔹 iSnippetsCrafter", value="[🔗 GitHub Repo](https://github.com/yourrepo)", inline=False)
    embed.add_field(name="🔹 Stackfolio", value="[🔗 Live Preview](https://yourportfolio.com/stackfolio)", inline=False)
    embed.set_image(url="https://discordbanners.vercel.app/static/img/portfolio.png")
    embed.set_footer(text="More projects coming soon!")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="contact", description="Reach out to me for a project!")
async def contact(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📩 Contact Me",
        description="📌 Click the buttons below to contact me directly!",
        color=BOT_COLOR
    )
    embed.add_field(name="📧 Gmail", value="`santhoshraj@gmail.com`", inline=False)
    embed.add_field(name="📜 Discord", value="`Santhosh#1234`", inline=False)
    embed.set_thumbnail(url="https://discordbanners.vercel.app/static/img/Thumbnail.png")  
    view = discord.ui.View()

    discord_button = discord.ui.Button(
        label="💬 Message on Discord", 
        style=discord.ButtonStyle.primary, 
        url="https://discord.com/users/1322240935773605979"  
    )

    portfolio_button = discord.ui.Button(
        label="🌍 Visit My Portfolio", 
        style=discord.ButtonStyle.link, 
        url="https://santhoshraj-portfolio.vercel.app/"
    )

    view.add_item(discord_button)
    view.add_item(portfolio_button)
    
    await interaction.response.send_message(embed=embed, view=view)


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed = discord.Embed(
            title="✨ Welcome to My Freelancer Hub! ✨",
            description=f"🎉 Hello {member.mention}! I'm **Santhosh Raj**, a passionate full-stack developer! 🚀\n\n"
                        "💡 Check out my work with `/portfolio`\n"
                        "📩 Need a project done? Use `/contact`\n"
                        "🌟 Enjoy your stay here!",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_image(url="https://media.giphy.com/media/l41YtZOb9EUABnuqA/giphy.gif")
        
        await channel.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "hello" in message.content.lower():
        await message.channel.send(f'✨ Hello {message.author.mention}! Welcome to **Santhosh’s Freelancer Bot**! Need help? Try `/services` 🚀')

    if "thanks" in message.content.lower():
        await message.channel.send(f'🌟 You’re welcome, {message.author.mention}! Glad to help!')
    if "awesome" in message.content.lower():
        await message.add_reaction("\U0001F525")
    if "cool" in message.content.lower():
        await message.add_reaction("\U0001F60E")
    if "great job" in message.content.lower():
        await message.add_reaction("\U0001F44C")
    
    await bot.process_commands(message)

bot.run(TOKEN)
