echo "Installing Yeet..."

if [ -d "/opt/yeet" ]; then
    echo "Yeet is already installed"
    exit 1
fi

# Create yeet directory
sudo mkdir /opt/yeet
sudo chown $USER:$USER /opt/yeet

# Copy files
cp -r ./bin /opt/yeet/bin

# detect which shell is being used
if [ -n "$ZSH_VERSION" ]; then
    echo "export PATH=/opt/yeet/bin:$PATH" >> ~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
    echo "export PATH=/opt/yeet/bin:$PATH" >> ~/.bashrc
elif [ -n "$FISH_VERSION" ]; then
    echo "\n#yeet start\nset PATH /opt/yeet/bin $PATH\n#yeet" >> ~/.config/fish/config.fish
fi

# Reload shell
exec $SHELL

# Done
echo "Yeet has been installed successfully!"