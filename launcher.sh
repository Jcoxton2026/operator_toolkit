
#!/bin/bash
clear
echo "== Red Team Toolkit =="
echo "1. Run API Key Scanner"
echo "2. Run Ultra Scraper"
echo "3. Run JS Network Logger"
echo "4. Run Search Engine Dorker"
echo "5. Run Universal Scraper (Natural Language)"
echo "6. Exit"
read -p "Choose: " opt

case $opt in
  1) python3 api_key_scanner.py ;;
  2) python3 ultra_scraper.py ;;
  3) python3 js_network_logger.py ;;
  4) python3 search_engine_dorker.py ;;
  5) read -p "What should I scrape? (e.g. scrape emails from github.com): " cmd; python3 universal_scraper.py "$cmd" ;;
  6) exit ;;
esac
