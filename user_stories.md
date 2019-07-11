keys
=====
*) Responder: logged a volunteer with first aid training that responds to calls to provide medical help.
*) Patient: a person in need of medical help who calls the responder
*) Guest: logged out user
*) Medical help:
*) Profile: the res main information page, it contains:  
*) Status is the responders availability at a given time, can be red-inactive, yellow-unactivated unless urgent, green-active.

user stories
============
RESPONDER:
11) I can sign up 
17) I can log in/out
14) I can check off what I can help with, i.e cpr, carry epi pen 
15)I can select multiple tags about my credentials
I can get notification if a call is made
23) I can set the status of my availability on my schedule each week
I can change my status at any time
I can choose to respond
I can see who is asking for help
I can see the patients location and directions to them
I cancel a call if I want
I can turn off notifications
I can sign out of the app if I don't want to be part of it anymore


PATIENT:
12) I can sign up to use the app
I can remain signed in as long as I dont log out
16) I can add current medical information to my profile
21) I can call for help by pressing a button related to my condition or other(call emergency contact)
I can see when a responder agrees to my call
I can see who the responder is
I can see a live map of where the responder is
I can cancel call for help if I'd like


P.S
=====
Legally: can the responder break in?
Filters out responders within 10 km: https://developers.google.com/maps/documentation/embed/get-api-key
Calls 911 when emergency button is activated
Pre-existing conditions
sms api: https://www.swiftsmsgateway.com/
responsive
seperate backend as api
models and views-sends json
https://twitter.com/hashtag/silentcallprocedure?f=realtime&src=hash


Iteration 1:
Data models ✓
11✓ 12✓ 17 14✓ 15 16

Iteration 2:
Iteration 3:
Iteration 4:

details:
=========
11) 2 pages: front-page and sign-up page {details?} 
12) sign-page for the patient {details?} 
21) auto dials 911 and sends text to emergency contact

CSS:
====
body font family:
normal text:
header text:

New ideas:
===========
email activation

