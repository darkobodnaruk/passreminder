from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
import reminder.models as rm
from django.conf import settings

import re

def index(request):
	context = {}
	return render(request, "index.html", context)

def email_validates(email):
	return re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

def submit(request):
	email = request.POST['email']
	if not email_validates(email):
		return HttpResponse("Your email '%s' is no good" % email)

	try:
		account = rm.Account.objects.get(email__exact=email)
		hashes = account.passhash_set
		context = {"account": account}

		return render(request, "testpass.html", context)

	except rm.Account.DoesNotExist:
		# first-time user
		account = rm.Account(email=email)
		account.save()

		send_mail(
			"Welcome to %s" % settings.APP_NAME, 
			"Go to our <a href=\"#\">passphrase entry</a> page to input your passphrase.", 
			"darko.bodnaruk@zemanta.com", 
			[account.email]
		)
		return HttpResponse("Thanks %s, expect an email" % email)

def testpass(request):
	hashname = request.POST['hashname']
	hhash = request.POST['hhash']

	passhash = rm.PassHash(name=hashname, hhash=hhash)
	passhash.save()

	return HttpResponse("hashname: %s, hhash: %s" % (hashname, hhash))
