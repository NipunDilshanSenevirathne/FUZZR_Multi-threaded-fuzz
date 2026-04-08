#!/bin/bash
# Dorkmaster v3.0 — Installer
# Author: Nipun Dilshan

R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'
C='\033[0;36m'; W='\033[1;37m'; NC='\033[0m'

echo -e "${R}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   Dorkmaster v3.0 — Installer | Author: Nipun Dilshan           ║"
echo "║   Pattern + AI Verification | Multi-Model Rotation              ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Warn about sudo
if [ "$EUID" -eq 0 ] && [ -z "$SUDO_USER" ]; then
    echo -e "${Y}[!] Running as root without SUDO_USER. Config will go to root's home.${NC}"
    echo -e "${Y}    Recommended: run without sudo → bash install.sh${NC}"
    echo ""
fi

echo -e "${C}[1/3]${NC} Python dependencies..."
pip3 install requests colorama urllib3 --break-system-packages -q 2>/dev/null \
  || pip3 install requests colorama urllib3 -q \
  || sudo pip3 install requests colorama urllib3 --break-system-packages -q
echo -e "${G}[+] Done${NC}"

echo -e "${C}[2/3]${NC} Permissions..."
chmod +x "$DIR/dorkmaster.py"
echo -e "${G}[+] Done${NC}"

echo -e "${C}[3/3]${NC} Alias..."
ALIAS="alias dorkmaster='python3 ${DIR}/dorkmaster.py'"
for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$RC" ] && ! grep -q "alias dorkmaster=" "$RC"; then
        echo "$ALIAS" >> "$RC"
        echo -e "${G}[+] Alias → $RC${NC}"
    fi
done
sudo ln -sf "$DIR/dorkmaster.py" /usr/local/bin/dorkmaster 2>/dev/null \
  && echo -e "${G}[+] /usr/local/bin/dorkmaster created${NC}" \
  || echo -e "${Y}[~] System command skipped — alias works fine${NC}"

echo ""
echo -e "${G}[+] System install done. Running key setup wizard...${NC}"
echo ""
echo -e "${Y}NOTE: Running wizard as real user (not root) for correct config path.${NC}"
echo ""

if [ -n "$SUDO_USER" ]; then
    su - "$SUDO_USER" -c "python3 '$DIR/dorkmaster.py' --install"
else
    python3 "$DIR/dorkmaster.py" --install
fi

echo ""
echo -e "${W}Run scans:${NC}  ${C}python3 dorkmaster.py${NC}"
echo -e "${W}Update keys:${NC} ${C}python3 dorkmaster.py --install${NC}"
echo -e "${Y}Reload shell: source ~/.zshrc${NC}"
