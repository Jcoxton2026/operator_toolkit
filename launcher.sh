#!/bin/bash
echo -e "\033[1;36mOperator Toolkit v4 — AI Red Team Terminal\033[0m"
echo "[1] Natural Language Recon"
echo "[2] Crawl Target"
echo "[3] Dork Search"
echo "[4] Quit"
read -p "Choose: " opt
case $opt in
  1) python3 kernel.py ;;
  2) python3 modules/crawler.py ;;
  3) python3 modules/dorker.py ;;
  *) exit ;;
esac
