echo "Installing Yeet..."

if [ -d "/opt/yeet" ]; then
    echo "Yeet is already installed"
    exit 1
fi

touch /usr/bin/yeet
chmod +x /usr/bin/yeet
curl -L "https://github.com/sby051/yeet/blob/main/bin/yeet?raw=true" > /usr/bin/yeet

# Done
echo "Yeet has been installed successfully! Please restart your terminal."