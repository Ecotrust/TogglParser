# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.box_check_update = true

  config.vm.network "forwarded_port", guest: 8000, host: 8000 # django dev server
  config.vm.network "forwarded_port", guest: 80, host: 8080 # web server
  #config.vm.network "forwarded_port", guest: 8081, host: 8081 # web server
  #config.vm.network "forwarded_port", guest: 8889, host: 8889 # mapproxy
  #config.vm.network "forwarded_port", guest: 5432, host: 15432 # postgresql
  #config.vm.network :private_network, ip: "192.168.99.99"
  # config.vm.network 'private_network', ip: "192.168.99.99"

  config.vm.synced_folder "./", "/usr/local/apps/TogglParser"
  # config.vm.synced_folder "../ocs-wp", "/var/www/html"
end
