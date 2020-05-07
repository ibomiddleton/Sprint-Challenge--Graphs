from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


traversal_path = []

# The graph should be a dictionary
mapDictionary = {}
graph = mapDictionary

def bfs(starting_room_id):
    q = Queue()
    q.enqueue([starting_room_id])

    visited = set()

    while q.size() != 0:
        path = q.dequeue()
        current_room = path[-1]
    
        visited.add(current_room)
    
        for direction in graph[current_room]:
            if graph[current_room][direction] is '?':
                return path
            
            if graph[current_room][direction] not in visited:
                new_path = list(path)
                new_path.append(graph[current_room][direction])
                q.enqueue(new_path)

def dfs(starting_room):

    reverse_directions = {'n':'s', 's':'n', 'e':'w', 'w':'e'} # Reverse the directions

    counting_rms = 0

    while len(graph) != len(room_graph):
        current_room = player.current_room
        room_id = current_room.id
        room_dict = {}
        
        if room_id not in graph:
            for i in current_room.get_exits(): # Repeat to find the possible exits.
                room_dict[i] = '?'
            
            if traversal_path:
                prevRoom = reverse_directions[traversal_path[-1]]
                room_dict[prevRoom] = counting_rms

            graph[room_id] = room_dict
        
        else:
            room_dict = graph[room_id]    


        possible_exits = list()

        for direction in room_dict:
            if room_dict[direction] is '?':
 
                possible_exits.append(direction)
                
        if len(possible_exits) != 0:
            random.shuffle(possible_exits)
           
            direction = possible_exits[0]
            
            traversal_path.append(direction) # Append the direction of the traversal_path.
            
            player.travel(direction) # Move the player by the travel().
            
            room_move = player.current_room
              
            graph[current_room.id][direction] = room_move.id # Current room.id and direction of the graph is set equal to room_move.id.
            
        else:
            next_room = bfs(room_id) # Else use bfs to search for the next possible rooms and exits by using room_id.
            
            
            if next_room is not None and len(next_room) != 0:
                # For loop: Then repeat the length of the room to gain access to the room's id.
                for i in range(len(next_room)-1):
                    # Repeat the graph's next_room at the index to access the direction.
                    for direction in graph[next_room[i]]:
                        # If the next_room[i] and direction of the graph is equal to next_room[i + 1]:
                        if graph[next_room[i]][direction] == next_room[i + 1]:
                            
                            traversal_path.append(direction)

                            player.travel(direction)
            else:
                break
        
dfs(room_graph)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")