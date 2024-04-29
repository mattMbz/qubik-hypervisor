# Models
from django.contrib.auth.models import User
from app_hypervisor.models import VirtualMachine, NginxLocations


class NginxHandler:

    def __init__(self) -> None:
        pass


    def createNginxLocation(self, username, ip_address, app_name, vmname):

        virtual_machine = VirtualMachine.objects.get(name=vmname)

        nginx_config = f"""
        location /{username}/{app_name} {{
            rewrite ^/{username}/{app_name}(.*) $1 break;
            proxy_pass http://{ip_address};
        }}
        """

        # update "/etc/nginx/sites-available/username.conf" file
        nginx_conf_file = f"/etc/nginx/sites-available/{username}.conf"
        try:
            with open(nginx_conf_file, 'a') as f:
                f.write(nginx_config)
        except IOError as e:
            print(e)

        print(nginx_config)

        # write this config in the database
        NginxLocations.objects.create(location_config=nginx_config, virtual_machine=virtual_machine)


    def deleteNginxLocation(self, vm_id, username):

        # delete this config from database
        virtual_machine = VirtualMachine.objects.get(id=vm_id)
        nginx_locations = NginxLocations.objects.get(virtual_machine=virtual_machine)
        nginx_locations.delete()

        # update the "/etc/ngin/sites-available/" file
        user = User.objects.get(username=username)
        updated_nginx_locations = NginxLocations.objects.filter(virtual_machine__user=user)


        nginx_conf_file = f"/etc/nginx/sites-available/{username}.conf"
        
        try:
            with open(nginx_conf_file, 'w') as f:
                pass
        except IOError as e:
            print(e)

        for location in updated_nginx_locations:
            try:
                with open(nginx_conf_file, 'a') as f:
                    f.write(location.location_config)
            except IOError as e:
                print(e)
