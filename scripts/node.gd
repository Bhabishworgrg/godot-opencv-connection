extends Node

var tcp_server : TCPServer = TCPServer.new()
var client : StreamPeerTCP
const PORT : int = 65432
var received_data : String

func _ready():
	# Check if server started
	if tcp_server.listen(PORT) != OK:
		print("Server failed to start")
	else:
		print("Server started on port " + str(PORT))

@warning_ignore("unused_parameter")
func _process(delta):
	# Connect to python server
	if tcp_server.is_connection_available() and client == null:
		client = tcp_server.take_connection()
		print("Python connected")

	
	if client and client.get_available_bytes() > 0:
		received_data = client.get_utf8_string(client.get_available_bytes())
		handle_data(received_data)

func handle_data(finger_count: String):
	match int(finger_count):
		0:
			$ColorRect.color = Color(0,0,0)
		1:
			$ColorRect.color = Color(1,0,0)
		2:
			$ColorRect.color = Color(0,1,0)
		3:
			$ColorRect.color = Color(0,0,1)
		4:
			$ColorRect.color = Color(1,1,0)
		5:
			$ColorRect.color = Color(1,0,1)
