# Civis Services Flask Demo

This repository shows you how to host a web application in Civis Platform.  The example provided here is a simple Flask app.  This app queries the service for data in JSON format to display on the page.

## Requirements

To host your modified service on Civis Platform, you will need a Github account.  See [this article](https://civis.zendesk.com/hc/en-us/articles/115003734992-Version-Control#ConnectingPlatformtoGithub/Bitbucket) in the Civis Help Center if you have not yet connected your Github account to Civis.

To make changes to and run this application, you will need `git` and Docker installed on your machine.  Civis uses Docker to host web applications, so using Docker locally is the most reliable way to develop and troubleshoot your application.  You can follow the instructions [here](https://docs.docker.com/get-docker/) to install Docker on your machine.

## Getting Started

### Testing out the service in Civis Platform

First, let's run this Github repo (the one you are reading right now) as a service in Civis.

1. Go to https://platform.civisanalytics.com/spa/#/services/new to create a new Service.
   1. Find the "Git Connection" fields.
      1. Repository: `https://github.com/civisanalytics/civis-services-flask.git`
      1. Branch: `main`
   1. Find the "Docker" fields.
      1. Image name: `civisanalytics/civis-services-flask`
    2. Leave all other fields blank or with their default values.
1. Click `Start Deployment` to run the service.
1. Keep track of this service so you can find it later.  You can bookmark it, give it a distinctive name so you can find it in the Platform search bar, or add it to a project.

Once the service has started up, you should see a "Your service is running!" message in the preview window.  You can also view the logs for the service by clicking [`Deployment History`](https://civis.zendesk.com/hc/en-us/articles/360001335031-Civis-Service-Deployment#DeploymentHistory).

Click `Stop Deployment` to shut down the service and stop using compute resources.  If you forget to shut down the service, it will sleep automatically after one hour of inactivity.

### Running the service locally

Next, let's run the service on your own machine.

1. Clone this git repo.
1. Start Docker on your machine if it is not already running.
1. From the directory you cloned into, run `docker-compose up --build -V`.
1. See your web app locally at http://localhost:3838/ in your web browser.  You should see the same application you saw in Civis, though with slightly different information (we'll fix that later).
1. Use `CTRL-C` to stop the web server.

Every time you make a change to the code, you should stop `docker-compose` and start it again.  Subsequent runs will start up much faster.

## Customizing the Environment

### Add a local API key

You might have noticed one or two differences between the applications running in Civis and locally.  Applications running in Civis have an API key automatically provided in the `CIVIS_API_KEY` environment variable.  This Flask app uses that key to retrieve the username of the owner of the service.  If the last item in the response has `name: null` then you don't have this variable set locally.  This is normal.

We recommend setting this value in a `.env` file.  `docker-compose` will automatically read this file and it will be ignored by `git`.

1. Generate a Civis API key by following the instructions [here](https://civis.zendesk.com/hc/en-us/articles/216341583-Generating-an-API-Key).
1. Create a `.env` file in the same directory as this README.
1. Add a line to the `.env` file with:
   ```
   CIVIS_API_KEY=<the API key you just generated>
   ```
1. Run the service locally (same steps as above)

You should now see your Civis username on the page.

### Choose your favorite fruit

The API response from the service includes an `is_favorite` attribute for each of the fruits, but the value should be `false` for every fruit.  The app can be configured with a favorite fruit using a different environment variable.

First, we'll set this variable locally.

1. Add a line to the `.env` file with:
   ```
   FLASK_DEMO_FAVORITE_FRUIT_PASSWORD=<your choice of: Strawberry, Watermelon, Grapefruit, or your username>
   ```
1. Restart the local service (`CTRL-C` to stop it and then `docker-compose up --build -V` to restart it)

You should now see that the fruit you selected is marked as a favorite!

Next, we'll configure the service running in Civis to receive this environment variable. To do this, we will first create a Civis Credential and then attach that credential to the service.

1. Go to https://platform.civisanalytics.com/spa/#/credentials.
   1. Click `Create Credential`
      1. Name: `Flask Demo Favorite Fruit`
      1. Type: `Custom`
      2. Username: `fruit` (for this example the username will not be used)
      1. For the password, enter the same value you choose for your favorite fruit locally: Strawberry, Watermelon, etc.
      1. Leave all other fields blank or with their default values.
      1. Click `Save`
1. Go to the service you created previously.  If you can't find it, you can go to https://platform.civisanalytics.com/spa/#/services and find it in the list of all services you have access to.
   1. Find the "Security and Access" fields.
      1. Click in the "Credentials" box and select the `Flask Demo Favorite Fruit` credential.  This will make the username and password of the credential available to the service through environment variables.
   1. Click `Start Deployment` to start the service.  If the service is still running from the last time you started it, click `Stop Deployment` and wait for the page to update, then click `Start Deployment` to restart it.

You should again see that the fruit you selected is marked as a favorite!  If not, try refreshing the page to make sure you are not looking at an old version of the service.

### Modifying the code

You should now be comfortable running the service locally and in Civis Platform.  To make further changes, fork this Github repo into your own account and create a new service in Civis connected to your forked repo.  As you push changes to Github, you will see them reflected in the service when you stop and restart it.

If you want to host multiple applications in a single repository, you can set the Git Path Directory on the service to select between them. The entrypoint of this docker image will `cd` to that directory and attempt to run `start_service.sh`.  For other custom configurations, you may want to build a custom docker image.

## Additional Notes

### Updating your service

Instead of clicking `Stop Deployment`, you could instead click on `Update Deployment`. This will redeploy your service with no downtime, i.e., your old application will still be available while your new version is starting up.  This is a great option for your production applications, but during development it can be unclear whether you are looking at an old or new version of the app.  We recommend stopping and starting the service while testing out changes.

### Adding packages

If you would like to upgrade your packages or install new packages, please add to the `requirements.txt` file at the root of this repo.  You can also modify the `start_service.sh` script if you need to install libraries or more complex dependencies.

### The Civis API key

In Platform, the `CIVIS_API_KEY` variable belongs to **the user who owns the service, not the user making the request to the service.**  Be careful about making requests on behalf of users, as this might pose a security risk.


### Front end changes

This example application does not attempt to set up a fully featured front end. It uses a simple HTML and Javascript file.  The frontend lives in the `dist` folder.  The `index.html` file uses `main.js` to call the `/fruits` endpoint and update the page.

You can use React, Angular, or any other Javascript framework in your service. Just make sure that your root API endpoint (/) returns the initial landing page for your app.  If not, Platform will consider your app to be down and continuously attempt to restart it.

**NOTE**: Browsers will often cache HTML and Javascript files by name. Therefore, we recommend having the Javascript file(s) named using a commit hash or similar to prevent caching.


### Accessing your service from inside Civis Platform

You can access your service's API easily using a Civis API key.  All applications running in Civis are automatically provided with an API key, so you can use this key to access a running service without needing an additional authentication token.  To provide or revoke access to the service, click `Share` on the service page to modify permissions.

In the example below, we will hit the API of a Platform service from a Platform notebook.  Make sure your service is running before trying out this example.  In production code, you would want to catch this sort of error, deal with timeouts, etc.

1. Go to https://platform.civisanalytics.com/spa/#/notebooks/new?language=python3 and click `Start Server` to start up a new Jupyter notebook.
1. Direct access to the service expires after five minutes.  We recommend using the `cachetools` package to re-authenticate with the service every 2 minutes.  Run the following code in your notebook:
   ```
   !pip install cachetools
   ```
1. In the next cell, store your service ID in a variable so it can be reused:
   ```
   SERVICE_ID = <your service ID>
   ```
1. Now add code for making an authenticated request to the service:
   ```
   import requests
   import cachetools.func

   @cachetools.func.ttl_cache(ttl=120)
   def _service_session(service_id):
       session = requests.Session()
       service = client.services.get(service_id)
       auth_url = service['current_deployment']['displayUrl']
       base_url = service['current_url']
       session.get(auth_url)
       return [session, base_url]

   def service_request(service_id, endpoint):
       session, base_url = _service_session(service_id)
       resp = session.get(base_url + endpoint)
       return resp
   ```
1. You should now be able to access the API for the service:
   ```
   service_request(SERVICE_ID, "/api/health").text
   ```
   should return the result:
   ```
   'The ID of this service is: ...'
   ```

   The fruits API endpoint:
   ```
   service_request(SERVICE_ID, "/api/fruits/").json()
   ```
   should match the result shown on the service page.


### Accessing your service from outside of Civis Platform

You can also access your service's API from outside of Platform. This is not recommended, but sometimes necessary to allow access from other systems.

In order to do this, you must generate a service token for your service.  See https://civis.zendesk.com/hc/en-us/articles/360004026012-Advanced-Deployments#ServiceTokenAuthentication for more information.  You must be signed into Civis to view that documentation.  You can revoke the service token to revoke access to the service.
