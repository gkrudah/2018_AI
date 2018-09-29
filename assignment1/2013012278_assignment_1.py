import queue
import sys
import heapq

mazeinfo = []
startrow = 0
exitrow = 0
keycol = 0
keyrow = 0


#read maze size
def readmazeinfo(f):
	global mazeinfo
	mazeinfo = []
	line = f.readline()
	line = line.split(" ")

	for data in line:
		data = int(data)
		mazeinfo.append(data)

'''
find start, key, exit location for heuristic
return 0 when success
return -1 when fail
'''
def find(maze):
	global startrow
	global exitrow
	global keycol
	global keyrow

	for i in range(mazeinfo[2]):
		if maze[0][i] == 3:
			startrow = i
			#print("startrow=", startrow)

		if maze[mazeinfo[1] - 1][i] == 4:
			exitrow = i
			#print("exitrow=", exitrow)

	for i in range(mazeinfo[1]):
		if i == 0:
			continue

		for j in range(mazeinfo[2]):
			if maze[i][j] == 6:
				keycol = i
				keyrow = j
				#print("key=", keycol, keyrow)
				break

	if startrow == 0 or exitrow == 0 or keycol == 0 or keyrow == 0:
		return -1
	else:
		return 0

'''
solve maze by bfs
path priority is EWSN
return 0 when success
return -1 when fail
p.s kinda wrong because number 5 replace tiles that be searched not shortest path tiles
'''
def bfs(maze):
	global mazeinfo
	global startrow
	global keycol
	global keyrow
	totalnode = 0
	movex = [1, -1, 0, 0]
	movey = [0, 0, 1, -1]
	visit_key = [[0] * int(mazeinfo[2]) for _ in range(int(mazeinfo[1]))]
	visit_exit = [[0] * int(mazeinfo[2]) for _ in range(int(mazeinfo[1]))]

	q = queue.Queue()
	q.put((0, startrow))

	#find key
	while q:
		x, y = q.get()
		totalnode += 1

		if maze[x][y] == 6:
			maze[x][y] = 5
			print("key_length=", visit_key[x][y])
			print("key_time=", totalnode)
			break

		for i in range(4):
			nx = x + movex[i]
			ny = y + movey[i]

			if 1 <= nx < mazeinfo[1] and 1 <= ny < mazeinfo[2]:
				if visit_key[nx][ny] == 0 and maze[nx][ny] != 1 and maze[nx][ny] != 3:
					visit_key[nx][ny] = visit_key[x][y] + 1

					if maze[nx][ny] != 6 and maze[nx][ny] != 4:
						maze[nx][ny] = 5

					q.put((nx, ny))

	q.queue.clear()
	q.put((keycol, keyrow))
	visit_exit[keycol][keyrow] = visit_key[x][y]

	#find exit
	while q:
		x, y = q.get()
		totalnode += 1

		if maze[x][y] == 4:
			for k in maze:
				print(k)
			print("---")
			print("length=", visit_exit[x][y])
			print("time=", totalnode)
			return 0

		for i in range(4):
			nx = x + movex[i]
			ny = y + movey[i]

			if 1 <= nx < mazeinfo[1] and 1 <= ny < mazeinfo[2]:
				if visit_exit[nx][ny] == 0 and maze[nx][ny] != 1 and maze[nx][ny] != 3:
					visit_exit[nx][ny] = visit_exit[x][y] + 1

					if maze[nx][ny] != 4:
						maze[nx][ny] = 5

					q.put((nx, ny))

	return -1

'''
4 functions below are heuristic functions 
'''
def distance_key(locationcol, locationrow, spentnode):
	global keycol
	global keyrow

	return abs(locationcol - keycol) + abs(locationrow - keyrow) + spentnode


def distance_key_greed(locationcol, locationrow):
	global keycol
	global keyrow

	return abs(locationcol - keycol) + abs(locationrow - keyrow)


def distance_exit(locationcol, locationrow, spentnode):
	global mazeinfo
	global exitrow

	return abs(mazeinfo[1] - 1 - locationcol) + abs(locationrow - exitrow) + spentnode


def distance_exit_greed(locationcol, locationrow):
	global mazeinfo
	global exitrow

	return abs(mazeinfo[1] - 1 - locationcol) + abs(locationrow - exitrow)

'''
solve maze by heuristic A* function
give priortiy (how far + how much spent)
return 0 when success
return -1 when fail
p.s kinda wrong because number 5 replace tiles that be searched not shortest path tiles
'''
def heuristic(maze):
	global mazeinfo
	global startrow
	global exitrow
	global keycol
	global keyrow
	totalnode = 0
	movex = [1, -1, 0, 0]
	movey = [0, 0, 1, -1]
	visit_key = [[0] * int(mazeinfo[2]) for _ in range(int(mazeinfo[1]))]
	visit_exit = [[0] * int(mazeinfo[2]) for _ in range(int(mazeinfo[1]))]

	q = []
	heapq.heappush(q, (distance_key(0, startrow, 0), 0, startrow))

	#find key
	while q:
		h, x, y = heapq.heappop(q)
		totalnode += 1

		if maze[x][y] == 6:
			maze[x][y] = 5
			print("key_length=", visit_key[x][y])
			print("key_time=", totalnode)
			break

		for i in range(4):
			nx = x + movex[i]
			ny = y + movey[i]

			if 1 <= nx < mazeinfo[1] and 1 <= ny < mazeinfo[2]:
				if visit_key[nx][ny] == 0 and maze[nx][ny] != 1 and maze[nx][ny] != 3:
					visit_key[nx][ny] = visit_key[x][y] + 1

					if maze[nx][ny] != 6 and maze[nx][ny] != 4:
						maze[nx][ny] = 5

					heapq.heappush(q, (distance_key(nx, ny, visit_key[nx][ny]), nx, ny))

	q = []
	heapq.heappush(q, (distance_exit(keycol, keyrow, visit_key[x][y]), keycol, keyrow))
	visit_exit[keycol][keyrow] = visit_key[x][y]

	#find exit
	while q:
		h, x, y = heapq.heappop(q)
		totalnode += 1

		if maze[x][y] == 4:
			for k in maze:
				print(k)
			print("---")
			print("length=", visit_exit[x][y])
			print("time=", totalnode)
			return 0

		for i in range(4):
			nx = x + movex[i]
			ny = y + movey[i]

			if 1 <= nx < mazeinfo[1] and 1 <= ny < mazeinfo[2]:
				if visit_exit[nx][ny] == 0 and maze[nx][ny] != 1 and maze[nx][ny] != 3:
					visit_exit[nx][ny] = visit_exit[x][y] + 1

					if maze[nx][ny] != 4:
						maze[nx][ny] = 5

					heapq.heappush(q, (distance_exit(nx, ny, visit_exit[nx][ny]), nx, ny))

	return -1

'''
solve maze by heuristic greed function
give priortiy (how far)
replace shortest path tiles by using tree
make nodes can search by their location (location in 2d array == node.data)
this code uses this algorithm actually
return 0 when success
return -1 when fail
'''
def heuristic_greed(maze, filename):
	global mazeinfo
	global startrow
	global exitrow
	global keycol
	global keyrow
	totalnode = 0
	movex = [1, -1, 0, 0]
	movey = [0, 0, 1, -1]
	visit_key = [[0] * int(mazeinfo[2]) for _ in range(int(mazeinfo[1]))]
	visit_exit = [[0] * int(mazeinfo[2]) for _ in range(int(mazeinfo[1]))]

	q = []
	heapq.heappush(q, (distance_key_greed(0, startrow), 0, startrow))
	nodes_key = []
	for i in range(mazeinfo[1] * mazeinfo[2]):
		nodes_key.append(Node((0, 0)))
	mazetree = Tree()
	mazetree.insert(None, nodes_key[startrow])

	#find key
	while q:
		h, x, y = heapq.heappop(q)
		parent = nodes_key[(x * mazeinfo[2] + y)]
		totalnode += 1

		if maze[x][y] == 6:
			#print("key_length=", visit_key[x][y])
			#print("key_time=", totalnode)
			break

		for i in range(4):
			nx = x + movex[i]
			ny = y + movey[i]

			if 1 <= nx < mazeinfo[1] and 1 <= ny < mazeinfo[2]:
				if visit_key[nx][ny] == 0 and maze[nx][ny] != 1 and maze[nx][ny] != 3:
					visit_key[nx][ny] = visit_key[x][y] + 1

					if maze[nx][ny] != 4:
						node = nodes_key[(nx * mazeinfo[2]) + ny]
						node.data = (nx, ny)
						mazetree.insert(parent, node)

					heapq.heappush(q, (distance_key_greed(nx, ny), nx, ny))

	q = []
	heapq.heappush(q, (distance_exit_greed(keycol, keyrow), keycol, keyrow))
	visit_exit[keycol][keyrow] = visit_key[x][y]

	nodes_exit = []
	for i in range(mazeinfo[1] * mazeinfo[2]):
		nodes_exit.append(Node((0, 0)))

	#find exit
	while q:
		h, x, y = heapq.heappop(q)
		if x == keycol and y == keyrow:
			parent = nodes_key[(x * mazeinfo[2] + y)]
		else:
			parent = nodes_exit[(x * mazeinfo[2] + y)]
		totalnode += 1

		if maze[x][y] == 4:
			'''
			for k in maze:
				print(k)
			print("---")
			print("length=", visit_exit[x][y])
			print("time=", totalnode)
			'''
			printmaze(nodes_exit, maze, visit_exit[x][y], totalnode, filename)

			return 0

		for i in range(4):
			nx = x + movex[i]
			ny = y + movey[i]

			if 1 <= nx < mazeinfo[1] and 1 <= ny < mazeinfo[2]:
				if visit_exit[nx][ny] == 0 and maze[nx][ny] != 1 and maze[nx][ny] != 3:
					visit_exit[nx][ny] = visit_exit[x][y] + 1

					node = nodes_exit[(nx * mazeinfo[2]) + ny]
					node.data = (nx, ny)
					mazetree.insert(parent, node)

					heapq.heappush(q, (distance_exit_greed(nx, ny), nx, ny))

	return -1


#change maze and print total output to file
def printmaze(nodes, maze, length, time, filename):
	global mazeinfo
	global startrow
	global exitrow
	global keycol
	global keyrow

	node = nodes[(mazeinfo[2] * (mazeinfo[1] - 1)) + exitrow]

	while True:
		parent = node.parent
		if parent is None:
			break
		x, y = parent.data
		maze[x][y] = 5
		node = parent

	#cause initial data is (0, 0)
	maze[0][0] = 1

	f = open(filename, 'w')

	for i in range(mazeinfo[1]):
		for j in range(mazeinfo[2]):
			maze[i][j] = str(maze[i][j])

	for i in maze:
		f.write(" ".join(i))
		f.write("\n")

	f.write("---\n")
	f.write("length=%d\n" % length)
	f.write("time=%d" % time)

	f.close()


#solve first_floor maze
def first_floor():
	global mazeinfo
	f = open("first_floor.txt", 'r')#put file name which you want
	readmazeinfo(f)
	maze = []

	for line in f:
		maze.append(line.split())

	for i in range(mazeinfo[1]):
		for j in range(mazeinfo[2]):
			maze[i][j] = int(maze[i][j])

	if find(maze):
		print("WRONG MAZE")
		sys.exit()

	#if bfs(maze):
	#if heuristic(maze):
	if heuristic_greed(maze, "first_floor_output.txt"):
		print("NO KEY or NO EXIT")
		sys.exit()

	f.close()

#solve second_floor maze
def second_floor():
	global mazeinfo
	f = open("second_floor.txt", 'r')#put file name which you want
	readmazeinfo(f)
	maze = []

	for line in f:
		maze.append(line.split())

	for i in range(mazeinfo[1]):
		for j in range(mazeinfo[2]):
			maze[i][j] = int(maze[i][j])

	if find(maze):
		print("WRONG MAZE")
		sys.exit()

	#if bfs(maze):
	#if heuristic(maze):
	if heuristic_greed(maze, "second_floor_output.txt"):
		print("NO KEY or NO EXIT")
		sys.exit()

	f.close()

#solve third_floor maze
def third_floor():
	global mazeinfo
	f = open("third_floor.txt", 'r')#put file name which you want
	readmazeinfo(f)
	maze = []

	for line in f:
		maze.append(line.split())

	for i in range(mazeinfo[1]):
		for j in range(mazeinfo[2]):
			maze[i][j] = int(maze[i][j])

	if find(maze):
		print("WRONG MAZE")
		sys.exit()

	#if bfs(maze):
	#if heuristic(maze):
	if heuristic_greed(maze, "third_floor_output.txt"):
		print("NO KEY or NO EXIT")
		sys.exit()

	f.close()

#solve fourth_floor maze
def fourth_floor():
	global mazeinfo
	f = open("fourth_floor.txt", 'r')#put file name which you want
	readmazeinfo(f)
	maze = []

	for line in f:
		maze.append(line.split())

	for i in range(mazeinfo[1]):
		for j in range(mazeinfo[2]):
			maze[i][j] = int(maze[i][j])

	if find(maze):
		print("WRONG MAZE")
		sys.exit()

	#if bfs(maze):
	#if heuristic(maze):
	if heuristic_greed(maze, "fourth_floor_output.txt"):
		print("NO KEY or NO EXIT")
		sys.exit()

	f.close()

#solve fifth_floor maze
def fifth_floor():
	global mazeinfo
	f = open("fifth_floor.txt", 'r')#put file name which you want
	readmazeinfo(f)
	maze = []

	for line in f:
		maze.append(line.split())

	for i in range(mazeinfo[1]):
		for j in range(mazeinfo[2]):
			maze[i][j] = int(maze[i][j])

	if find(maze):
		print("WRONG MAZE")
		sys.exit()

	#if bfs(maze):
	#if heuristic(maze):
	if heuristic_greed(maze, "fifth_floor_output.txt"):
		print("NO KEY or NO EXIT")
		sys.exit()

	f.close()

'''
Tree node
make parent to find each node's parent
'''
class Node(object):
	def __init__(self, data):
		self.data = data
		self.parent = self.child1 = self.child2 = self.child3 = None

'''
3 branch factor tree
exit program when behave wrong
'''
class Tree(object):
	def __init__(self):
		self.root = None

	def insert(self, parent, node):
		if parent is None:
			self.root = node
		else:
			if parent.child1 is None:
				parent.child1 = node
			elif parent.child2 is None:
				parent.child2 = node
			elif parent.child3 is None:
				parent.child3 = node
			else:
				print("Wrong Tree")
				sys.exit()

			node.parent = parent


def main():
	first_floor()
	second_floor()
	third_floor()
	fourth_floor()
	fifth_floor()


if __name__ == "__main__":
	main()
