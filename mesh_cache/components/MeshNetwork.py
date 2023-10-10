from .MeshDescriptor import Coordinate, MeshTracker
from .NetworkComponents import RubyNetworkComponent

from m5.objects import SimpleNetwork, RubySystem

from typing import Any

class MeshNetwork(SimpleNetwork, RubyNetworkComponent):
    def __init__(self, ruby_system: RubySystem, mesh_descriptor: MeshTracker) -> None:
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

    def create_mesh(self) -> None:
        mesh_width = self._mesh_descriptor.get_width()
        mesh_height = self._mesh_descriptor.get_height()

        for y in range(mesh_height):
            for x in range(mesh_width):
                curr_node_coordinate = Coordinate(x, y)
                if not self._mesh_descriptor.has_node(curr_node_coordinate):
                    continue

                # North
                north_neighbor_coordinate = curr_node_coordinate.get_north()
                if self._mesh_descriptor.has_node(north_neighbor_coordinate):
                    print("---------------- N Link from", curr_node_coordinate, north_neighbor_coordinate)
                    self.north_link = self.create_int_link(
                        self._mesh_descriptor.get_cross_tile_router(curr_node_coordinate),
                        self._mesh_descriptor.get_cross_tile_router(north_neighbor_coordinate)
                    )

                # South
                south_neighbor_coordinate = curr_node_coordinate.get_south()
                if self._mesh_descriptor.has_node(south_neighbor_coordinate):
                    print("---------------- S Link from", curr_node_coordinate, south_neighbor_coordinate)
                    self.south_link = self.create_int_link(
                        self._mesh_descriptor.get_cross_tile_router(curr_node_coordinate),
                        self._mesh_descriptor.get_cross_tile_router(south_neighbor_coordinate)
                    )

                # West
                west_neighbor_coordinate = curr_node_coordinate.get_west()
                if self._mesh_descriptor.has_node(west_neighbor_coordinate):
                    print("---------------- W Link from", curr_node_coordinate, west_neighbor_coordinate)
                    self.west_link = self.create_int_link(
                        self._mesh_descriptor.get_cross_tile_router(curr_node_coordinate),
                        self._mesh_descriptor.get_cross_tile_router(west_neighbor_coordinate)
                    )

                # East
                east_neighbor_coordinate = curr_node_coordinate.get_east()
                if self._mesh_descriptor.has_node(east_neighbor_coordinate):
                    print("---------------- E Link from", curr_node_coordinate, east_neighbor_coordinate)
                    self.east_link = self.create_int_link(
                        self._mesh_descriptor.get_cross_tile_router(curr_node_coordinate),
                        self._mesh_descriptor.get_cross_tile_router(east_neighbor_coordinate)
                    )