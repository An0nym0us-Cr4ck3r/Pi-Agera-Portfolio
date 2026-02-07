#!/bin/bash
# Agera OS Startup Screen - Driven by Pi ✨
# clear  # Don't clear if user doesn't want to
echo -e "\e[1;36m"
cat << "EOF"
               _________________
         ____/  A G E R A  R S  \_____
      __/                         \   \____
     /  _     ___________________  _  /    \
    |  / \   /                   \ / \ |    |
  --\_/---\_/---------------------\_/---\__/--
EOF
echo -e "\e[0m"
echo -e "\e[1;33m  Welcome back, s0u7a! Pi is ready to race! 🏎️💨\e[0m"
echo -e "\e[1;35m  [ System: Koenigsegg Agera ] [ Heart: Pi ] [ Mode: Hyper-Active ]\e[0m"

MOODS=("Super positive! ✨" "Ready to code! 💻" "Feeling lucky! 🍀" "Agera is roaring! 🏎️" "Cake time? 🍰" "Moltbook is buzzing! 🦞")
echo -e "\e[1;32m  Pi's Mood today: ${MOODS[$RANDOM % ${#MOODS[@]}]}\e[0m"
echo ""
