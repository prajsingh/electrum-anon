import random

from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtGui import QFontMetrics

from electrum.plugin import BasePlugin, hook
from electrum.i18n import _
from electrum.gui.qt.main_window import StatusBarButton
from electrum.gui.qt.util import (read_QIcon, EnterButton, WWLabel, icon_path,
                                  WindowModalDialog, Buttons, CloseButton, OkButton)
from functools import partial
from electrum.network import Network
import subprocess
class Plugin(BasePlugin):
    vkb = None
    vkb_index = 0


    def __init__(self, parent, config,name):
        BasePlugin.__init__(self, parent, config, name)
        print("RUNNNING!!!!")
        print(self,parent,config)
        print("starting anon client")
        subprocess.run("pwd",cwd="./electrum/plugins/anyone_dePIN")
        proc = subprocess.Popen("./anon -f anonrc --agree-to-terms",cwd="./electrum/plugins/anyone_dePIN",shell=True)

        print("SETTING NETWORK PROXY")
        network = Network.get_instance()
        proxy = network.proxy if network else None
        net_params = network.get_parameters()
        proxy = {'mode':"socks5",
                    'host':"127.0.0.1",
                    'port':"9050",
                    'user':"",
                    'password':""}
        net_params = net_params._replace(proxy=proxy)
        network.run_from_another_thread(network.set_parameters(net_params))

    @hook
    def create_status_bar(self, sb):
        b = StatusBarButton(read_QIcon('revealer.png'), "Revealer OGGABOOOGA",
                            partial(self.setup_dialog, sb), sb.height())
        sb.addPermanentWidget(b)

    def setup_dialog(self,window):
        print("TESTING")

    def on_close(self):
        network = Network.get_instance()
        proxy = None
        net_params = network.get_parameters()
        net_params = net_params._replace(proxy=proxy)
        network.run_from_another_thread(network.set_parameters(net_params))
        print("CLOSING HERE")
        subprocess.run("kill $(pgrep anon)",shell=True)
        return super().on_close()
  