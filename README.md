# PIPCUT

### Overview

The application is a URL shortener web application built using Flask, a Python web framework. It allows users to create shortened URLs and track the number of visits to those URLs. Users can register an account, log in, and access their personalized dashboard to manage their shortened URLs. The application also provides analytics for each shortened URL.
## Key Features:

1. URL Shortening: Users can input lengthy URLs and generate shortened versions that are easier to share and remember.

2. Customizable URLs: Users have the option to customize the shortened URLs to reflect their brand or preferred keywords, making them more recognizable and memorable.

3. Link Analytics: The application will track and provide insightful analytics on the usage and performance of the shortened URLs, including click-through rates, geographic data, and referral sources.

4. QR Code Generation: The system will generate QR codes for each shortened URL, allowing users to easily share them in printed materials or mobile devices.

5. Link History: Users will have access to a comprehensive history of their shortened URLs, including creation dates, original URLs, and usage statistics.

6. Secure and Scalable: The application will prioritize data security, implement proper authentication mechanisms, and ensure scalability to handle a large volume of requests.

7. User Management: The system will provide user registration and authentication functionalities, allowing users to manage their shortened URLs and access personalized features.



## Get a copy
It is believed that you have python installed already. Open CMD or terminal
1. Clone this repo

2. Open the directory
```sh
cd pipcut
```
3. Create Virtual Environment
```sh
python -m venv <your-venv-name>
```
4. Activate virtual environment on CMD or Powershell
```sh
<your-venv-name>\Scripts\activate
```
On gitbash terminal
```sh
source <your-venv-name>/Scripts/activate.csh
```
5. Install project packages
```sh
pip install -r requirements.txt
```
6. Set environment variable
```sh
set FLASK_APP=url_shortenenr
```
On gitbash terminal
```sh
export FLASK_APP=url_shortener
```
7. Create database
```sh
flask shell
```
```sh
db.create_all()
quit()
```
8. Run program
```sh
flask run
```
<hr>





