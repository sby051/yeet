echo "Installing Yeet..."

if [ -d "/opt/yeet" ]; then
    echo "Yeet is already installed"
    exit 1
fi

touch /usr/bin/yeet
chmod +x /usr/bin/yeet
curl -L "https://github.com/sby051/yeet/blob/main/bin/yeet?raw=true" > /usr/bin/yeet

# split the shell path to get the shell name
shell_name=${SHELL[-1]}

# add yeet to path in the shell config file
if [ "$shell_name" = "bash" ]; then
    echo "export PATH=\$PATH:/usr/bin" >> ~/.bashrc
elif [ "$shell_name" = "zsh" ]; then
    echo "export PATH=\$PATH:/usr/bin" >> ~/.zshrc
elif [ "$shell_name" = "fish" ]; then
    echo "set -x PATH \$PATH /usr/bin" >> ~/.config/fish/config.fish
fi

# Done
echo "Yeet has been installed successfully! Please restart your terminal."