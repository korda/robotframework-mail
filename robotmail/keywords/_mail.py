from keywordgroup import KeywordGroup
import imaplib
import time
from bs4 import BeautifulSoup

class _MailKeywords(KeywordGroup):

	def __init__(self):
		i = 0

	def open_mailbox(self, server, user, pwd, ssl=False, port=993):
		"""
		Connect to mailbox using given arguments.
		"""
		if ssl:
			self.mailbox = imaplib.IMAP4_SSL(server, port)
		else:
			self.mailbox = imaplib.IMAP4(server, port)
		self.mailbox.login(user, pwd)
		self.mailbox.select()

	def close_mailbox(self):
		self.mailbox.close()

	def get_unread_email(self, email=None):
		"""
		Gets unread mails send to mailbox from `email`. If `email` is 'None'
		it gets all unread emails.

		Returns list of numbers, you can use them to retrive data from emails with
		other keywords.
		"""
		if email is None:
			r, item = self.mailbox.search(None, 'UNSEEN')
		else:
			r, item = self.mailbox.search(None, 'UNSEEN', 'FROM', email)

		item = item[0].split()

		return item

	def wait_for_mail(self, timeout=60,email=None):
		"""
		Waits until unread email(s) show up. Note that it will exit at once if there is a
		unread email already in mailbox.

		It will return number of first (ussualy oldest) unread mail.

		If it will reach `timeout` (`timeout` is in seconds) before unread email shows up it fails.

		It will check for new emails every 20 seconds. (However if left timeout is lower than 20 seconds
		it will wait for value of timeout)


		If `email` is given it checks from  emails send to mailbox from `email`. If `email` is 'None'
		it checks for all unread emails.
		"""
		
		timeout = int(timeout)

		while (timeout >= 20):
			if email is None:
				r, item = self.mailbox.search(None, 'UNSEEN')
			else:
				r, item = self.mailbox.search(None, 'UNSEEN', 'FROM', email)
			if len(item[0].split()) > 0:
				return item[0]
			time.sleep(20)
			timeout = timeout - 20

		if timeout > 0:
			time.sleep(timeout)

		if email is None:
			r, item = self.mailbox.search(None, 'UNSEEN')
		else:
			r, item = self.mailbox.search(None, 'UNSEEN', 'FROM', email)

		if len(item[0].split()) > 0:
			return item[0]

		raise AssertionError("No mail found")       



	def mark_email_as_read(self, email=None):
		"""
		Marks email(s) as read.

		If `email` is number it marks email with that number as read, if `email` is 'None' then it marks all unread emails as read,otherwise
		it searches for emails recived from `email` and marks them as read.

		"""
		if email is None:
			r, item = self.mailbox.search(None, 'UNSEEN')
			item = item[0].split()
			for num in item:
				self.mailbox.store(num,'+FLAGS','\Seen')
		elif isinstance(email, int):
			self.mailbox.store(email,'+FLAGS','\Seen')
		else:
			r, item = self.mailbox.search(None, 'UNSEEN', 'FROM', email)
			item = item[0].split()
			for num in item:
				self.mailbox.store(num,'+FLAGS','\Seen')


	def get_all_links_from_email(self, email):
		"""
		Parses email in search of links and returns
		list of found links.

		It marks email as read in the proccess.
		"""
		links = []
		soup = BeautifulSoup(self.mailbox.fetch(email, '(BODY[TEXT])')[1][0][1].decode("quoted-printable"))
		for link in soup.find_all('a'):
			links.append(link.get('href'))

		return links
