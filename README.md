# kelvin
## The New Kelvin Site 2.0, using Python Django.

### How it works.
The main files that need to be cared about that are python related are kelvin/website/urls.py and kelvin/website/views.py, which is where all the urls are defined, and pages are rendered.

All the content is in the "app" folder, kelvin/website. template/ includes all of the HTML for the site and static/ includes all of the CSS, JS and images.

---

To run a basic development server, python3 is required to be installed.
From here:
 - Create a directory for your virual environment such as ~/envs
 - Set up a virtual environment using `virtualenv -p python3 kelvin`
 - Activate it using `source ~/envs/kelvin/bin/activate`
 - Create a directory for your code such as /dev/kelvin
 - Clone the repository using `git clone git@github.com:ExogenesisBen/kelvin.git` (this will require that your GitHub account has access to the repository, that the old/current Webmaster can give you, and also that you have set-up SSH keys between your computer and your GitHub account).
 - Run `pip install -r requirements.txt` from inside the kelvin folder. (Make sure your virtual environment is active!)
 - Use the command `python manage.py runserver` to run the server
 - Go to 127.0.0.1:8000 in your browser of choice to access the site.

Adding your own machines local IP address to kelvin/kelvin/settings.py ALLOWED_HOSTS and running `python manage.py runserver 0.0.0.0` allows you to access the website from any device on your network at your machines local IP :8000.

---

To put the site into production, ensure all changes are commited and pushed, and then enter pythonanywhere, open a bash console, and git pull, and then go to the web tab, and reload the server. Ensure DEBUG in kelvin/kelvin/settings.py is False in production.
