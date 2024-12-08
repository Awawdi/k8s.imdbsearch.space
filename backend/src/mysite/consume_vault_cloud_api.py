
from vault_cloud_api import Users, VaultAPI

class ConsumeVaultCloudAPI:
    def __init__(self):
        """
        Constructor
        """
        self._vm_user, self._vm_password = VaultAPI.get_instance().get_credentials(Users.VM_WARE_USER)