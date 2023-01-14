echo "Installing Yeet..."

if [ -d "/opt/yeet" ]; then
    echo "Yeet is already installed"
    exit 1
fi

# Create yeet directory
sudo mkdir /opt/yeet
sudo chown $USER:$USER /opt/yeet

# Create bin directory
mkdir /opt/yeet/bin
curl -L "https://github.com/sby051/yeet/blob/main/bin/yeet?raw=true" > /opt/yeet/bin/yeet

# determine shell
if [ -n "$ZSH_VERSION" ]; then
    echo "export PATH=\$PATH:/opt/yeet/bin" >> ~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
    echo "export PATH=\$PATH:/opt/yeet/bin" >> ~/.bashrc
elif [ -n "$FISH_VERSION" ]; then
    echo "set -x PATH \$PATH /opt/yeet/bin" >> ~/.config/fish/config.fish
else
    echo "Yeet only supports bash, fish and zsh"
    exit 1
fi

# Done
echo "Yeet has been installed successfully! Please restart your terminal."