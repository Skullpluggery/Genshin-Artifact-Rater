Discord bot that rates an artifact against an optimal 5* artifact. Put the command and image in the same message.

```
-rate <image> [lvl=<level>] [<stat>=<weight> ...]
```

If you have any issues or want to use the bot in your private server, contact shrubin#1866 on discord.

#### Default Weights

ATK%, DMG%, Crit - 1
ATK, EM, Recharge - 0.5
Everything else - 0

### Options
#### Level
Compare to specified artifact level (default: 20)
```
-rate lvl=0
```

#### Weights
Set custom weights (valued between 0 and 1)
```
-rate atk=1 er=0 atk%=0.5
```
<stat> is any of HP, HP%, ATK, ATK%, ER (Recharge), EM, PHYS, CR (Crit Rate), CD (Crit Damage), ELEM (Elemental DMG%), Heal, DEF, DEF%

### Setup
```
python3.8 -m pip install -r requirements.txt
```

Store env variables for OCR Space and Discord in `.env`
```
DISCORD_TOKEN=<token>
OCR_SPACE_API_KEY=<key>
```

#### Run the bot
```
python3.8 bot.py
```

#### Run one-off
Edit `url` in `rate_artifact.py`
```
python3.8 rate_artifact.py
```
