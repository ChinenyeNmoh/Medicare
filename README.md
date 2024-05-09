# Medicare

![Homepage](tempsnip.png)

## Project Overview

Medicare is a hospital appointment system enabling seamless registration and booking for patients seeking consultations with doctors. Leveraging Python and Flask for backend development, alongside MySQL for data storage, the system offers a user-friendly interface developed with HTML, Bootstrap CSS, and jQuery. Deployed on Digital Ocean with Nginx and Gunicorn, the application ensures scalability and security. Integration of Certbot encryption certification and Datadog monitoring further enhances reliability and performance.

### Built With

- python
- flask
- HTML
- CSS
- Mysql
- jQuery
- jinja

## Getting Started

To get started with this project, follow the steps below:

### Prerequisites
- Set your mail  credentials  in the `.env` file.

### Installation

1. Clone the repository.
   ```sh
   git clone https://github.com/ChinenyeNmoh/Medicare.git
   ```
2. Install the required packages.
	```sh
	pip install -r requirements.txt
	```
3. Configure your .env file with your mysql username and password credentials and also your mail password
	```sh
	SQL_USERNAME=MYSQL_USERNAME
    SQL_PASS=MYSQL_PASSWORD
    MAIL_PASSWORD=GOOGLE_APP_PASSWORD

	```
### Start the application for development.
   ```sh
   python3 run.py
   ```

### Contributing
We welcome contributions from the community. If you have suggestions to make this project better, please create a pull request or open an issue with the "enhancement" tag. Don't forget to star the project if you find it useful!

License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
- Chinenye Nmoh [Github](https://github.com/ChinenyeNmoh/) / [Linkedin](https://www.linkedin.com/in/chinenye-nmoh-88479699/) / [Email](chinenyeumeaku@gmail.com) 

