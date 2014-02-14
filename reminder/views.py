from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import reminder.models as rm
from django.conf import settings
from django.template import loader, Context

import re
import random
import string

def index(request):
	context = {}
	return render(request, "index.html", context)

def email_validates(email):
	return re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

def email_confirmation(request):
	code = request.GET['confirmation_code']
	accounts = rm.Account.objects.filter(confirmation_code__exact=code)
	if accounts:
		account = accounts[0]
		account.confirmed = True
		account.save()
		
		request.session['account'] = account.id

		return redirect('enterpass')
	else:
		return HttpResponse("Don't know what you're talking about.")


def submit(request):
	email = request.POST['email']
	if not email_validates(email):
		return HttpResponse("Your email '%s' is no good" % email)

	try:
		account = rm.Account.objects.get(email__exact=email)
		hashes = account.passhash_set
		context = {"account": account}

		request.session['account'] = account.id

		return redirect("testpass")

	except rm.Account.DoesNotExist:
		# first-time user

		confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
		account = rm.Account(email=email, confirmed=False, confirmation_code=confirmation_code)
		account.save()

		subject = "Welcome to %s" % settings.APP_NAME
		ffrom = "darko.bodnaruk@zemanta.com"
		to = [email]
		# html_content = "Go to our <a href=\"%s?confirmation_code=%s\">passphrase entry</a> page to input your passphrase." % (request.build_absolute_uri('email_confirmation'), confirmation_code)
		template = loader.get_template("email_confirmation.html")
		url = request.build_absolute_uri('email_confirmation') + "?confirmation_code=" + confirmation_code
		context = Context({"url": url, "imgurl": request.build_absolute_uri('/static/reminder/img/unlock.svg')})
		html_content = template.render(context)
		# html_content = render(request, "email_confirmation.html", context)
		text_content = html_content
		message = EmailMultiAlternatives(subject, text_content, ffrom, to)
		message.attach_alternative(html_content, "text/html")
		message.send()
		# send_mail(message, html, ffrom, to)
		return HttpResponse("Thanks %s, expect an email" % email)

def enterpass(request):
	try:
		account = rm.Account.objects.get(id=request.session['account'])
	except:
		return HttpResponse("Eh?")

	if request.method == 'GET':
		context = {}
		return render(request, "enterpass.html", context)

	elif request.method == 'POST':
		hashname = request.POST['hashname']
		hhash = request.POST['hhash']

		passhash = rm.PassHash(account=account, name=hashname, hhash=hhash, hashtype=settings.HASH_TYPE)
		passhash.save()

		return HttpResponse("hashname: %s, hhash: %s" % (hashname, hhash))

def testpass(request):
	account = rm.Account.objects.get(id=request.session['account'])

	context = {"account": account}
	return render(request, "testpass.html", context)
