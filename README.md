IoT-Based Penalty Kick Simulator

This project consists of the design and development of a simplified penalty simulator based on Internet of Things (IoT) principles, created by students at the Autonomous University of Baja California. The system uses a Raspberry Pi as the central platform to manage the control logic and the interaction between hardware and software.

The most important aspects of the project are:

Game Mechanics: The system represents the process of taking a penalty kick with two main physical elements: a DC motor that simulates the ball being shot and a servomotor that moves a character (the goalkeeper) to attempt to block the shot.

Activation and Control: The user can trigger the shot in two ways: through a physical button connected to the system or remotely via a web interface that uses the MQTT protocol to send the signal.

Goalkeeper Automation: Upon receiving the shot command, the servomotor automatically chooses a random direction (left, center, or right) to try to stop the ball, adding an element of challenge and dynamism to the simulation.

Technologies Used: To build the Python code, libraries such as Flask (for the web interface), RPi.GPIO (for physical pin control), and Paho MQTT (for remote communication) were used.

The model was built with accessible materials like cardboard and wood, alongside electronic components (L293D chips, resistors, and wires) soldered onto a perfboard. The authors conclude that the project was successful in achieving an effective integration of hardware and software.
