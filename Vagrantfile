$set_flask_app = <<-'SCRIPT'
source ~/.profile
if [ -z "$FLASK_APP" ]; then
    echo "export FLASK_APP=flaskr" >> ~/.profile
fi
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end
  config.vm.provision "shell", inline: $set_flask_app, privileged: false
end