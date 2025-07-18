import cv2
import mediapipe as mp
import socket


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands

# Set the minimum confidence for detecting and tracking hands
# Value ranges from 0 to 1 and you can increase them for better accuracy
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize utility to draw landmarks on the frame
mp_draw = mp.solutions.drawing_utils


# TCP Connection Setup
TCP_IP = "127.0.0.1"
TCP_PORT = 65432
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket_obj.connect((TCP_IP, TCP_PORT))
    print("Connected to Godot")
except Exception as e:
    print("Connection failed: " + e.strerror)

# Start video capture
cap = cv2.VideoCapture(0)

print("Capturing video...")


# Main loop
while True:
    # Read frames from the video capture
    success, frame = cap.read()

    # Break the loop if capture fails
    if not success:
        print("Capture failed")
        break

    # Process the frame to get the hand landmarks
    results = hands.process(frame)

    finger_count = 0
    # True if hand landmarks are detected
    if results.multi_hand_landmarks:
        # Loop through each hand
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Landmark ids of finger tips
            # 4 - Thumb, 8 - Index, 12 - Middle, 16 - Ring, 20 - Little
            tip_ids = [4, 8, 12, 16, 20]

            finger_states = []
            for tip_id in tip_ids:
                finger_tip = hand_landmarks.landmark[tip_id]

                # Base landmark for the finger is the one before the tip
                finger_base = hand_landmarks.landmark[tip_id - 1]

                # Check if the finger is the thumb
                if tip_id == 4:
                    # We check if the x coordinate of the tip is less than the x coordinate of the base
                    # As the thumb opens horizontally, when tip's x is less than base's x, the thumb is open
                    # True is added to the list if the thumb is open
                    finger_states.append(finger_tip.x > finger_base.x)
                else:
                    # For other fingers, we check if the y coordinate of the tip is less than the y coordinate of the base
                    # As other fingers open vertically, when tip's y is less than base's y, the finger is open
                    # True is added to the list if the finger is open
                    finger_states.append(finger_tip.y < finger_base.y)

            # Count number of open fingers
            finger_count = finger_states.count(True)

    # Send the finger count to Godot
    socket_obj.send(str(finger_count).encode())

    # Display the current detected finger on the frame
    cv2.putText(frame, "Fingers: " + str(finger_count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the video frame
    cv2.imshow("Fingers", frame)

    # Break the loop if ESC key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        print("ESC key pressed. Exiting...")
        break

# Release the video capture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
socket_obj.close()

print("Program ended")
