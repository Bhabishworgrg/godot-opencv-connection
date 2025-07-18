extends Node


@export
var PORT: int
var tcp_server: TCPServer = TCPServer.new()
var client: StreamPeerTCP
var received_data: String


func _ready() -> void:
	# Check if server started
	if tcp_server.listen(PORT) != OK:
		print("Server failed to start")
	else:
		print("Server started on port " + str(PORT))


func _process(_delta) -> void:
	# Connect to python server
	if tcp_server.is_connection_available() and client == null:
		client = tcp_server.take_connection()
		print("Python connected")

	
	if client and client.get_available_bytes() > 0:
		received_data = client.get_utf8_string(client.get_available_bytes())
		_handle_data(received_data)


func _handle_data(finger_count: String) -> void:
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
