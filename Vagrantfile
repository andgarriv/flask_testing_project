Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/jammy64"
    
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    
    # Sincronización de la carpeta de tu proyecto para que sea accesible desde la VM
    config.vm.synced_folder ".", "/home/vagrant/app", type: "virtualbox"
    
    # Copiar el archivo .env desde el directorio del proyecto en tu máquina local
    config.vm.provision "file", source: ".env", destination: "/home/vagrant/app/.env"
    
    config.vm.provision "shell", path: "provision.sh"
end