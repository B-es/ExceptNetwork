from winreg import HKEY_CURRENT_USER, OpenKeyEx, REG_SZ, SetValueEx, KEY_ALL_ACCESS

class ProxyExceptionAdderer:

    location = HKEY_CURRENT_USER

    key_path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'

    def save_proxy_exeptoins(self, exeptoins:[str])->None:

        try:
            key = OpenKeyEx(self.location, self.key_path, 0, KEY_ALL_ACCESS)
            new_value = self.__get_new_value(exeptoins)
            SetValueEx(key,'ProxyOverride', None, REG_SZ, new_value)

        except Exception as e:
            print(f"Ошибка {e}")

    def __get_new_value(self, exeptoins:[str])->str:
        return ';'.join(exeptoins)