import docker
from docker.models.containers import Container, ContainerCollection
from docker import APIClient

print("")
print("---")

class MinecraftServer:
  def __init__(self, container: Container):
    self.__container = container
    self.name = container.name
    self.status = self.get_status() 
    self.players = self.get_players()
    
  def get_status(self):
    status = self.__container.stats()
    return status
    
  def get_players(self):
    players = self.__container.exec_run("rcon-cli list")
    return players
  
  
client = docker.from_env()

container = client.containers.get("minecraft-server-mc-1")

server = MinecraftServer(container)

status: dict[any, any] = container.stats(stream = False)

def read_status(status):
  if type(status) == dict[any,any]:
    read_status(status)
  else:
    for key, value in status.items():
      print(f"{key}: {value}")
      
read_status(status)
