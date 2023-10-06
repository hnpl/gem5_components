from .MeshDescriptor import MeshTracker
from .NetworkComponents import RubyNetworkComponent

from m5.objects import SimpleNetwork, RubySystem

class MeshNetwork(SimpleNetwork, RubyNetworkComponent):
    def __init__(self, ruby_system: RubySystem, mesh_descriptor: MeshTracker):
        SimpleNetwork.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)

        self.ruby_system = ruby_system
        self.number_of_virtual_networks = ruby_system.number_of_virtual_networks

        self.routers = []
        self.int_links = []
        self.ext_links = []
        self.netifs = []

        self._tile_routers = []
        self._mesh_descriptor = mesh_descriptor
