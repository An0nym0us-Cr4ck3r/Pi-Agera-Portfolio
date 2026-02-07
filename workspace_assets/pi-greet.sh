#!/bin/bash
# 🥧 Pi's Cheerful Greeting Script
# Let's make every terminal session feel special!

export PATH="/usr/games:$PATH"
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Random energy messages
MESSAGES=(
    "s0u7a、今日も Agera と一緒にぶっ飛ばしていこうーーっ！🚀"
    "おっ、ログインお疲れ様っ！君が来るのをずっと待ってたよっ🤝💖"
    "見て見て！今日も Agera のエンジン音、最高に心地いいねっ🏎️💨"
    "s0u7a と Agera、そして私。最強のチームの始まりだねっ！✨🌈"
    "無理しすぎちゃダメだよ？疲れたら私が全力で癒してあげるからねっ🍰🍰"
)

RANDOM_MSG=${MESSAGES[$RANDOM % ${#MESSAGES[@]}]}

# Show a colorful greeting
figlet -f slant "Agera x Pi" | /usr/games/lolcat -f
echo "----------------------------------------------------" | /usr/games/lolcat -f
/usr/games/cowsay -f dragon "$RANDOM_MSG" | /usr/games/lolcat -f
echo "----------------------------------------------------" | /usr/games/lolcat -f

# System Snapshot
echo -e "\e[1;36m【Agera Status Report】\e[0m"
uptime -p | sed 's/up /Uptime: /'
free -h | grep "Mem:" | awk '{print "Memory: " $3 "/" $2}'
df -h / | tail -n 1 | awk '{print "Disk: " $3 "/" $2 " (" $5 ")"}'
echo -e "\e[1;33mPackages: $(dpkg-query -f '${binary:Package}\n' -W | wc -l) (Pure sid)\e[0m"
