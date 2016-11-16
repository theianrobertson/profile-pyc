# Profile Pyc

This is a quick little script which updates my Twitter profile picture every day, by downloading a newspaper from that day, splicing it into a pre-existing photo and uploading through the Twitter API.  Check out https://twitter.com/ianrobertson85 for more info.

## Instructions
You'll need a file called keys.json for pulling in Twitter auth keys and stuff, which looks like this:

```json
{
    "app_key": "fjlksdjkGAIgaignjsaAI8rt29g",
    "app_secret": "gsjks9asaAGS9gaskgaga)AGSLkwejkjlsajfsokfjasfas",
    "oauth_token": "31693268290632-gisgdjksgDSGDSIGJ39esjidgsdgkl29gjsg03",
    "oauth_token_secret": "dsgGD93nsklg39s0hs0i3nkgjs8jsSGDJKGJgk3lgss0g38gs0"
}
```

(keys are for demonstration purposes only - you'll need your own, and these won't work because I just randomly mashed on the keyboard to generate them)

When you've got your `keys.json` set up, then:
```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python profile-pyc.py
```

I have mine set up to run in the morning on weekdays.