# Software Functionality
The software functions by scanning the network `192.168.1.1/24` using `nmap`. Styled with `qt6`. Written in `python`. At the same time, it connects to the IP `192.168.1.34` creating a reverse connection on port `5500`.

![image](https://github.com/user-attachments/assets/de747991-2e48-4641-bced-85086d13c31f)

![image](https://github.com/user-attachments/assets/d51ce0f3-4475-4b56-aafa-b2f3b0855e97)

## Software Functionality
The software functions by scanning the network `192.168.1.1/24` using `nmap`. Styled with `qt6`. Written in `python`. At the same time, it connects to the IP `192.168.1.34` creating a reverse connection on port `5500`.

![image](https://github.com/user-attachments/assets/d473fb51-e334-42e5-a7ef-1985915abe8e)

## Software Functionality
The software functions by scanning the network `192.168.1.1/24` using `nmap`. Styled with `qt6`. Written in `python`. At the same time, it connects to the IP `192.168.1.34` creating a reverse connection on port `5500`.

## How it Works
When the program is initiated, the user can scan their network normally to identify which IPs are connected, with additional information about MAC addresses. Using `QThread`, it is possible to separate two logics: one for the user who will scan and another for the reverse connection. Even if the user closes the program, the process remains in the background with `powershell` open.

## Configuration
* To alter the base64 line (line 13), use the following online tool: https://www.revshells.com/
* To change the IP address (line 34), replace it with the desired IP.

### Note
The program is written in Brazilian Portuguese. If you want to remove the backdoor, you can modify the code to use it only as a network scanner program. Remember, this is for educational purposes only, to understand how a backdoor works.
