import disnake
from disnake.ext import commands
import json
import os
import asyncio
import datetime

class Confession(commands.Cog):
    def __init__(self, bot, confession_channel_id, confession_create_channel_id, cfs_file="cfs.json"):
        self.bot = bot
        self.confession_channel_id = confession_channel_id
        self.confession_create_channel_id = confession_create_channel_id
        self.cfs_file = cfs_file
        self.load_cfs_data()
 
    command_prefix = "a."

    def load_cfs_data(self):
        if os.path.exists(self.cfs_file):
            with open(self.cfs_file, "r") as f:
                self.cfs_data = json.load(f)
        else:
            self.cfs_data = {"count": 0}
        self.cfs_count = self.cfs_data.get("count", 0)

    @commands.command(name="cfs", description=f"- Tạo confession\n- **Cách sử dụng**: nhập lệnh `{command_prefix}cfs + nội dung`")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create_confession(self, ctx, *, content=""):
        command_prefix = self.bot.command_prefix[0]
        if ctx.channel.id == self.confession_channel_id: 
            if not content:
                await ctx.message.delete()
                embed = disnake.Embed(description=f"**Cách sử dụng**: nhập lệnh `{command_prefix}cfs + nội dung`", color=0xfd5296)
                temp = await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await temp.delete()
            else:
                self.cfs_count += 1
                await ctx.message.delete()
                embed = disnake.Embed(title=f"CFS #{self.cfs_count}", description=content, timestamp=datetime.datetime.now(datetime.UTC), color=0xfd5296)
                embed.set_footer(text=f"Confession gửi bởi{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
                confession_channel = self.bot.get_channel(self.confession_channel_id)
                message = await confession_channel.send(embed=embed)
                thread = await message.create_thread(name=f"Trả lời CFS #{self.cfs_count}")
                await ctx.send(embed= disnake.Embed(title=f"✅ • Đã tạo Confessions **CFS #{self.cfs_count}**, tại {message.mention}", color=0x37faa2))
                self.cfs_data["count"] = self.cfs_count
                self.save_cfs_data()
        else: 
            await ctx.message.delete()
            crt_channel = f"https://discord.com/channels/{ctx.guild.id}/{self.confession_create_channel_id}"
            temp = await ctx.send(embed = disnake.Embed(description=f"**Bạn chỉ có thể tạo confessions ở kênh {crt_channel} .**",color=0xff0000))
            await asyncio.sleep(5)
            await temp.delete()

            return

    @commands.command(name="cfsan", description=f"- Tạo confession ẩn danh\n- **Cách sử dụng**: nhập lệnh `{command_prefix}cfsan + nội dung`")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create_anonymous_confession(self, ctx, *, content = None):
        if ctx.channel.id != self.confession_channel_id: 
            await ctx.message.delete()
            crt_channel = f"https://discord.com/channels/{ctx.guild.id}/{self.confession_create_channel_id}"
            temp = await ctx.send(embed = disnake.Embed(description=f"**Bạn chỉ có thể tạo confessions ở kênh {crt_channel} .**",color=0xff0000))
            await asyncio.sleep(5)
            await temp.delete()
            return
            
        if content is None: 
                await ctx.message.delete()
                embed = disnake.Embed(description=f"**Cách sử dụng**: nhập lệnh `{self.command_prefix}cfs + nội dung`", color=0xfd5296)
                temp = await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await temp.delete()
                return 
        
        self.cfs_count += 1
        await ctx.message.delete()
        embed = disnake.Embed(title=f"CFS #{self.cfs_count}", description=content, timestamp=datetime.datetime.now(datetime.UTC), color=0xfd5296) 
        embed.set_footer(text=f"Confession ẩn danh")
        confession_channel = self.bot.get_channel(self.confession_channel_id)
        message = await confession_channel.send(embed=embed)
        thread = await message.create_thread(name=f"Trả lời CFS #{self.cfs_count}")
        self.cfs_data["count"] = self.cfs_count
        self.save_cfs_data()

    def save_cfs_data(self):
        with open(self.cfs_file, "w") as f:
            json.dump(self.cfs_data, f)

def setup(bot, confession_channel_id, confession_create_channel_id, cfs_file="cfs.json"):
    bot.add_cog(Confession(bot, confession_channel_id, confession_create_channel_id, cfs_file))
