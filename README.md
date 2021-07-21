# About The Project

This article aims to document the case study in the recruitment process by neuro.net. In this study, respectively:

- The coordinates of the address entered by the user, which is transferred to a flask application via HTTP request, are determined.
- It is determined whether the entered address is in MKAD or not. 
- If the entered address is in MKAD, the application responds as "The address you entered is located inside the MKAD" and this answer is written to both the log file and the terminal.
- If the entered address is not in the MKAD, the distance between the coordinates of the address entered by the user and the coordinates of the MKAD is found, and this distance is written to both the log file and the terminal.
---
**NOTE**

Python 3.9 was used in this study.

---


## Installation
Required modules for Flask application(server-side)
```bash
pip install flask
pip install geopy
pip install requests
```
The required module for the user to communicate with the application via http request(user-side)
```bash
pip install requests
```
## Usage

```python
import requests
response = requests.post("http://mekinci.pythonanywhere.com", data={"address":"<address>"})
print(response.text)
```
The address to be processed should be entered in the <address> field. The web address of the log file created after the actions taken is below.

[Log file](https://mekinci.pythonanywhere.com/static/neuro_case.log)
## Test
Below is the image of the tests and the log file made by entering some addresses into the application.

![alt text](https://github.com/metinekinci/neuro_case/blob/main/terminal_ss.PNG?raw=true)
  
