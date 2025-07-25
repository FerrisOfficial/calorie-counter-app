#!/bin/bash
# Skrypt instalacji dla WSL

echo "=== Instalacja środowiska do budowania APK w WSL ==="

# Aktualizacja systemu
sudo apt update && sudo apt upgrade -y

# Instalacja podstawowych narzędzi
sudo apt install -y python3-pip python3-dev build-essential git unzip

# Instalacja Java 8 (wymagane dla Android SDK)
sudo apt install -y openjdk-8-jdk

# Ustawienie JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc

# Instalacja zależności dla buildozer
sudo apt install -y autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalacja Cython i buildozer
pip3 install --user cython buildozer

# Dodanie ścieżki pip do PATH
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc

# Przeładowanie bashrc
source ~/.bashrc

echo ""
echo "=== Instalacja zakończona! ==="
echo "Teraz możesz uruchomić:"
echo "  buildozer android debug"
echo ""
echo "Pierwsze budowanie może zająć 30-60 minut"
