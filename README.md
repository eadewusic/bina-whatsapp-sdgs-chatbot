# Bina AI - WhatsApp SDGs ChatBot

The first of its kind! Bina is a WhatsApp chatbot designed to help users learn more about the United Nations Sustainable Development Goals (SDGs). The bot interacts with users by responding to their queries about the SDGs and provides relevant information and resources.

![image](https://github.com/user-attachments/assets/7467e78a-c5ea-47a4-9d93-2d748c907afc)

## Features

- Explains sustainability concepts clearly and concisely.
- Responds to user queries about the SDGs.
- Provides information on each of the 17 SDGs, including targets and indicators.
- Analyses user-submitted project ideas to identify relevant SDGs.
- Suggests relevant solutions aligned with the SDGs **(when prompted)**.
- Provides information about organisations working on specific SDGs **(when prompted)**.
- Logs conversations for debugging and future improvements.
- Offers additional resources for further learning **(when prompted)**.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
  - [For Users](#for-users)
  - [For Developers](#for-developers)
  - [Table of Contents](#table-of-contents)
  - [Get Started](#get-started)
  - [Step 1: Select Phone Numbers](#step-1-select-phone-numbers)
  - [Step 2: Send Messages with the API](#step-2-send-messages-with-the-api)
  - [Step 3: Configure Webhooks to Receive Messages](#step-3-configure-webhooks-to-receive-messages)
    - [Start your app](#start-your-app)
    - [Launch ngrok](#launch-ngrok)
    - [Integrate WhatsApp](#integrate-whatsapp)
    - [Testing the Integration](#testing-the-integration)
  - [Step 4: Understanding Webhook Security](#step-4-understanding-webhook-security)
    - [Verification Requests](#verification-requests)
    - [Validating Verification Requests](#validating-verification-requests)
    - [Validating Payloads](#validating-payloads)
  - [Step 5: Learn about the API and Build Your App](#step-5-learn-about-the-api-and-build-your-app)
  - [Step 6: Integrate AI into the Application](#step-6-integrate-ai-into-the-application)
  - [Step 7: Add a Phone Number](#step-7-add-a-phone-number)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Technologies Used

- Meta (formerly Facebook) Cloud API.
- Pure Python.
- Flask.
- Webhook events to receive messages in real-time.
- Gemini Pro to generate AI responses.
- Ngrok for tunnelling localhost to a public URL.

## Prerequisites

#### For Users:

1. Have a functional WhatsApp account.
2. Have access to the internet.
3. Be open-minded and ready to learn.
4. Chat away with Bina, take action and leave your footprint in the sands of Social Impact.

#### For Developers:

1. Python 3.7 or higher installed on your system.
2. A Meta developer account — If you don’t have one, you can [create a Meta developer account here](https://developers.facebook.com/).
3. A business app — If you don't have one, you can [learn to create a business app here](https://developers.facebook.com/docs/development/create-an-app/). If you don't see an option to create a business app, select **Other** > **Next** > **Business**.
4. Familiarity with Python.
5. Familiarity with Flask. See [tutorial1](https://youtu.be/6M3LzGmIAso?si=VX-kY5XK4sLtyd8n) and [tutorial2](https://youtu.be/Z1RJmh_OqeA?si=7By4IHLdgZaZFTM0)
6. Ngrok for tunnelling localhost to a public URL.

## Get Started

1. **Overview & Setup**: Begin your journey [here](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started).
2. **Locate Your Bots**: Your bots can be found [here](https://developers.facebook.com/apps/).
3. **WhatsApp API Documentation**: Familiarize yourself with the [official documentation](https://developers.facebook.com/docs/whatsapp).
4. **Helpful Guide**: Here's a [Python-based guide](https://developers.facebook.com/blog/post/2022/10/24/sending-messages-with-whatsapp-in-your-python-applications/) for sending messages.
5. **API Docs for Sending Messages**: Check out [this documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages).

## Step 1: Select Phone Numbers

- Make sure WhatsApp is added to your App.
- You begin with a test number that you can use to send messages to up to 5 numbers.
- Go to API Setup and locate the test number from which you will be sending messages.
- Here, you can also add numbers to send messages to. Enter your **own WhatsApp number**.
- You will receive a code on your phone via WhatsApp to verify your number.

## Step 2: Send Messages with the API

1. Obtain a 24-hour access token from the API access section.
2. It will show an example of how to send messages using a `curl` command which can be send from the terminal or with a tool like Postman.
3. Let's convert that into a [Python function with the request library](https://github.com/eadewusic/bina-whatsapp-sdgs-chatbot/blob/main/start/whatsapp_quickstart.py).
4. Create a `.env` files based on `example.env` and update the required variables.
5. You will receive a "Hello World" message (Expect a 60-120 second delay for the message).

Creating an access token that works longer then 24 hours

1. Create a [system user at the Meta Business account level](https://business.facebook.com/settings/system-users).
2. On the System Users page, configure the assets for your System User, assigning your WhatsApp app with full control. Don't forget to click the Save Changes button.
3. Now click `Generate new token` and select the app, and then choose how long the access token will be valid. You can choose 60 days or never expire.
4. Select all the permissions, as I was running into errors when I only selected the WhatsApp ones.
5. Confirm and copy the access token.

Now we have to find the following information on the **App Dashboard**:

- **APP_ID**: "<YOUR-WHATSAPP-BUSINESS-APP_ID>" (Found at App Dashboard)
- **APP_SECRET**: "<YOUR-WHATSAPP-BUSINESS-APP_SECRET>" (Found at App Dashboard)
- **RECIPIENT_WAID**: "<YOUR-RECIPIENT-TEST-PHONE-NUMBER>" (This is your WhatsApp ID, i.e., phone number. Make sure it is added to the account as shown in the example test message.)
- **VERSION**: "v18.0" (The latest version of the Meta Graph API)
- **ACCESS_TOKEN**: "<YOUR-SYSTEM-USER-ACCESS-TOKEN>" (Created in the previous step)

> You can only send a template type message as your first message to a user. That's why you have to send a reply first before we continue.

## Step 3: Configure Webhooks to Receive Messages

> Please note, this is the hardest part of this project. Took me 8 hours to figure this out.

#### Start your app

- Make you have a python installation or environment and install the requirements: `pip install -r requirements.txt`
- Run your Flask app locally by executing [run.py](https://github.com/eadewusic/bina-whatsapp-sdgs-chatbot/blob/main/run.py)

#### Launch ngrok

The steps below are taken from the [ngrok documentation](https://ngrok.com/docs/integrations/whatsapp/webhooks/).

> You need a static ngrok domain because Meta validates your ngrok domain and certificate!
> Once your app is running successfully on localhost, let's get it on the internet securely using ngrok!

1. If you're not an ngrok user yet, just sign up for ngrok for free.
2. Download the ngrok agent.
3. Go to the ngrok dashboard, click Your [Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken), and copy your Authtoken.
4. Follow the instructions to authenticate your ngrok agent. You only have to do this once.
5. On the left menu, expand Cloud Edge and then click Domains.
6. On the Domains page, click + Create Domain or + New Domain. (here everyone can start with [one free domain](https://ngrok.com/blog-post/free-static-domains-ngrok-users))
7. Start ngrok by running the following command in a terminal on your local desktop:

```
ngrok http 8000 --domain your-domain.ngrok-free.app
```

8. ngrok will display a URL where your localhost application is exposed to the internet (copy this URL for use with Meta).

#### Integrate WhatsApp

In the Meta App Dashboard, go to WhatsApp > Configuration, then click the Edit button.

1. In the Edit webhook's callback URL popup, enter the URL provided by the ngrok agent to expose your application to the internet in the Callback URL field, with /webhook at the end (i.e. https://myexample.ngrok-free.app/webhook).
2. Enter a verification token. This string is set up by you when you create your webhook endpoint. You can pick any string you like. Make sure to update this in your `VERIFY_TOKEN` environment variable.
3. After you add a webhook to WhatsApp, WhatsApp will submit a validation post request to your application through ngrok. Confirm your localhost app receives the validation get request and logs `WEBHOOK_VERIFIED` in the terminal.
4. Back to the Configuration page, click Manage.
5. On the Webhook fields popup, click Subscribe to the **messages** field. Tip: You can subscribe to multiple fields.
6. If your Flask app and ngrok are running, you can click on "Test" next to messages to test the subscription. You recieve a test message in upper case. If that is the case, your webhook is set up correctly.

#### Testing the Integration

Use the phone number associated to your WhatsApp product or use the test number you copied before.

1. Add this number to your WhatsApp app contacts and then send a message to this number.
2. Confirm your localhost app receives a message and logs both headers and body in the terminal.
3. Test if the bot replies back to you in upper case.
4. You have now successfully integrated the bot! 🎉
5. Now it's time to acutally build cool things with this.

## Step 4: Understanding Webhook Security

Below is some information from the Meta Webhooks API docs about verification and security. It is already implemented in the code, but you can reference it to get a better understanding of what's going on in [security.py](https://github.com/eadewusic/bina-whatsapp-sdgs-chatbot/blob/main/app/decorators/security.py)

#### Verification Requests

[Source](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#:~:text=process%20these%20requests.-,Verification%20Requests,-Anytime%20you%20configure)

Anytime you configure the Webhooks product in your App Dashboard, we'll send a GET request to your endpoint URL. Verification requests include the following query string parameters, appended to the end of your endpoint URL. They will look something like this:

```
GET https://www.your-clever-domain-name.com/webhook?
  hub.mode=subscribe&
  hub.challenge=1158201444&
  hub.verify_token=climiradi
```

The verify_token, `climiradi` in the case of this example, is a string that you can pick. It doesn't matter what it is as long as you store in the `VERIFY_TOKEN` environment variable.

#### Validating Verification Requests

[Source](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#:~:text=Validating%20Verification%20Requests)

Whenever your endpoint receives a verification request, it must:

- Verify that the hub.verify_token value matches the string you set in the Verify Token field when you configure the Webhooks product in your App Dashboard (you haven't set up this token string yet).
- Respond with the hub.challenge value.

#### Validating Payloads

[Source](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#:~:text=int-,Validating%20Payloads,-We%20sign%20all)

WhatsApp signs all Event Notification payloads with a SHA256 signature and include the signature in the request's X-Hub-Signature-256 header, preceded with sha256=. You don't have to validate the payload, but you should.

To validate the payload:

- Generate a SHA256 signature using the payload and your app's App Secret.
- Compare your signature to the signature in the X-Hub-Signature-256 header (everything after sha256=). If the signatures match, the payload is genuine.

## Step 5: Learn about the API and Build Your App

Review the developer documentation to learn how to build your app and start sending messages. [See documentation](https://developers.facebook.com/docs/whatsapp/cloud-api).

## Step 6: Integrate AI into the Application

> Please note, [OpenAI API](https://platform.openai.com/playground/assistants) is not free, it costs $5 as of August 1st, 2024. [Gemini API](https://ai.google.dev/gemini-api) is free but offers 60 requests per second. [Groq API](https://console.groq.com/playground) is also free but it allows for 20 requests per minute.

Now that we have an end to end connection, we can make the bot a little more clever then just shouting at us in upper case. All you have to do is come up with your own `generate_response()` function in [whatsapp_utils.py](https://github.com/eadewusic/bina-whatsapp-sdgs-chatbot/blob/main/app/utils/whatsapp_utils.py).

If you want a cookie cutter example to integrate either of these APIs, then watch these videos:

1. [OpenAI Assistants Tutorial](https://www.youtube.com/watch?v=0h1ry-SqINc)
2. Gemini API Tutorial: [With Jupyter Notebook](https://youtu.be/64Ldwi9YU4I?si=mWkUv98NeuNtP4Rd), [VS Code](https://youtu.be/UKQUWeYYrxE?si=d2yn0hORMzGX51gy), [Short Video](https://youtu.be/pTcunloZ-_o?si=sm7OUa61rrU3NZ8Y)
3. Groq Tutorial: [Video1](https://youtu.be/S53BanCP14c?si=m7XULjpq3A9nYiwo), [Video2](https://youtu.be/jScpBCBoGdU?si=zw-3yGzZ-jpzflCi)

## Step 7: Add a Phone Number

When you are ready to use your app for a production use case, you need to use your own phone number to send messages to your users.

To start sending messages to any WhatsApp number, add a phone number. To manage your account information and phone number, [see the Overview page.](https://business.facebook.com/wa/manage/home/) and the [WhatsApp docs](https://developers.facebook.com/docs/whatsapp/phone-numbers/).

If you want to use a number that is already being used in the WhatsApp customer or business app, you will have to fully migrate that number to the business platform. Once the number is migrated, you will lose access to the WhatsApp customer or business app. [See Migrate Existing WhatsApp Number to a Business Account for information](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/migrate-existing-whatsapp-number-to-a-business-account).

Once you have chosen your phone number, you have to add it to your WhatsApp Business Account. [See Add a Phone Number](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/add-a-phone-number).

When dealing with WhatsApp Business API and wanting to experiment without affecting your personal number, you have a few options:

1. Buy a New SIM Card
2. Virtual Phone Numbers
3. Dual SIM Phones
4. Use a Different Device
5. Temporary Number Services
6. Dedicated Devices for Development

**NOTICE!!!**: If your project is for a more prolonged or professional purpose, using a virtual phone number service or purchasing a new SIM card for a dedicated device is highly recommended. For quick tests, a temporary number might suffice, but always be cautious about security and privacy.
Remember that once a number is associated with WhatsApp Business API, it cannot be used with regular WhatsApp on a device unless you deactivate it from the Business API and re-verify it on the device :)

## Contributing

I welcome contributions to this project, **only after September 2024!** If you would like to contribute, please follow these guidelines:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Make your changes and commit them with descriptive messages.

4. Submit a pull request to the `main` branch.

## License

This project will be licensed under the MIT License in coming months.

## Contact

Follow my coding journey on YouTube: [youtube.com/@climiradiroberts](https://www.youtube.com/@climiradiroberts)

If you have any questions, feedback, or collaboration requests, please feel free to reach out to me at [e.adewusi@alustudent.com](mailto:e.adewusi@alustudent.com)

Click [Here](https://www.linktr.ee/climiradi) for my other links
