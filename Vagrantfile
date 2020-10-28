Vagrant.configure("2") do |config|
config.vm.define 'one' do |one| 
  one.vm.box = "ubuntu/bionic64"
  one.vm.network "forwarded_port", guest: 80, host: 8080
  one.vm.provision "shell", inline: <<-SHELL
     apt-get update
    apt-get install -y apache2 python3-pip
   SHELL
end
end
