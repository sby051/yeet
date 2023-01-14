echo "Installing Yeet..."

if [ -d "/opt/yeet" ]; then
    echo "Yeet is already installed"
    exit 1
fi

sudo mkdir /usr/bin/yeet
sudo touch /usr/bin/yeet/yeet
curl -L "https://github.com/sby051/yeet/blob/main/bin/yeet?raw=true" > /usr/bin/yeet/yeet

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