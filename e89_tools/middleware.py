import traceback
import os
from django.http.request import RawPostDataException

class ErrorMonitorMiddleware(object):

	def process_exception(self,request,exception):
		try:
			fobj = open(os.path.expanduser('~') + '/Desktop/error_request.html','w')
			fobj.write(request.body)
			fobj.close()
		except RawPostDataException:
			pass

		error_stack = traceback.format_exc()

		fobj = open(os.path.expanduser('~') + '/Desktop/error_response.txt','w')
		fobj.write(error_stack)
		fobj.close()
