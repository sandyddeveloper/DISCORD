import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

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



# 1️⃣ About Me Command (Fixed)
@bot.tree.command(name="about_me", description="Learn more about me!")
async def about_me(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

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


# 2️⃣ Custom User Profiles
user_profiles = {}

@bot.tree.command(name="set_profile", description="Set your user profile!")
async def set_profile(interaction: discord.Interaction, bio: str, skills: str, interests: str):
    user_profiles[interaction.user.id] = {"bio": bio, "skills": skills, "interests": interests}
    await interaction.response.send_message("✅ Profile updated successfully!", ephemeral=True)

@bot.tree.command(name="view_profile", description="View your profile!")
async def view_profile(interaction: discord.Interaction):
    profile = user_profiles.get(interaction.user.id)
    if not profile:
        await interaction.response.send_message("❌ No profile found! Use `/set_profile` to create one.", ephemeral=True)
        return

    embed = discord.Embed(title=f"{interaction.user.name}'s Profile", color=BOT_COLOR)
    embed.add_field(name="📝 Bio", value=profile["bio"], inline=False)
    embed.add_field(name="💻 Skills", value=profile["skills"], inline=False)
    embed.add_field(name="🎯 Interests", value=profile["interests"], inline=False)
    embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else "")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# 3️⃣ XP & Leveling System
user_xp = {}

@bot.tree.command(name="xp", description="Check your XP & Level!")
async def check_xp(interaction: discord.Interaction):
    xp = user_xp.get(interaction.user.id, 0)
    level = xp // 100
    await interaction.response.send_message(f"🌟 **{interaction.user.name}** - XP: {xp}, Level: {level}", ephemeral=True)

def add_xp(user_id, amount):
    user_xp[user_id] = user_xp.get(user_id, 0) + amount

# 4️⃣ Daily Challenges
daily_challenges = ["Build a simple REST API", "Design a personal portfolio", "Find 3 freelancing clients", "Learn a new CSS trick!"]

@bot.tree.command(name="daily_challenge", description="Get a new challenge!")
async def daily_challenge(interaction: discord.Interaction):
    challenge = random.choice(daily_challenges)
    add_xp(interaction.user.id, 20)  # Reward XP
    await interaction.response.send_message(f"🔥 **Today's Challenge:** {challenge} (+20 XP)", ephemeral=True)

# 5️⃣ Tech Quiz Game
quiz_questions = {
    "What does HTML stand for?": ["Hyper Text Markup Language", "High Tech Machine Learning", "Hyper Transfer Machine Logic"],
    "Which language is used for backend development?": ["Python", "HTML", "CSS"],
    "What is React?": ["A JavaScript Library", "A Database", "A Backend Framework"]
}

@bot.tree.command(name="quiz", description="Answer a random tech quiz question!")
async def quiz(interaction: discord.Interaction):
    question, options = random.choice(list(quiz_questions.items()))
    correct_answer = options[0]
    random.shuffle(options)

    select = discord.ui.Select(placeholder=question, options=[discord.SelectOption(label=opt) for opt in options])

    async def callback(interaction):
        if interaction.data['values'][0] == correct_answer:
            add_xp(interaction.user.id, 50)
            response = "✅ Correct! (+50 XP)"
        else:
            response = f"❌ Wrong! The correct answer was **{correct_answer}**."

        await interaction.response.send_message(response, ephemeral=True)

    select.callback = callback
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.send_message("🧠 **Tech Quiz Time!** Choose the correct answer:", view=view, ephemeral=True)


# 7️⃣ Fun Games (Rock Paper Scissors)
@bot.tree.command(name="rps", description="Play Rock Paper Scissors!")
async def rps(interaction: discord.Interaction, choice: str):
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)

    result = "It's a draw!" if choice == bot_choice else (
        "You win!" if (choice == "rock" and bot_choice == "scissors") or 
                     (choice == "paper" and bot_choice == "rock") or 
                     (choice == "scissors" and bot_choice == "paper") else "You lose!"
    )

    await interaction.response.send_message(f"🤖 Bot chose **{bot_choice}**. {result}", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    bot.user_xp[message.author.id] = bot.user_xp.get(message.author.id, 0) + 10
    await bot.process_commands(message)


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


if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=8080)
    bot.run(TOKEN)
