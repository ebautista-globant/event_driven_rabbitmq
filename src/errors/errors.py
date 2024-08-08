import sys
import traceback
from contextlib import contextmanager

from kombu.exceptions import MessageStateError
from logging import getLogger


class AppBaseError(Exception):
    def __init__(self, message="", code=None, obj=None, additional=None):
        #frame = sys._getframe(1)
        #module = frame.f_locals.get("self").__class__.__module__
        #func = frame.f_code.co_name

        #self.instance = "{}: {}".format(module, func)
        #self.func = frame.f_code.co_name
        self.message = message
        self.code = code
        self.obj = obj
        self.additional = additional

        super(AppBaseError, self).__init__(message)

    def __str__(self):
        return self.message


class RequestError(AppBaseError):
    pass


class FormattedWarning(AppBaseError):
    pass


class RequeueError(AppBaseError):
    pass


class AuthorizationError(AppBaseError):
    pass


class QueueErrorHandle:
    logger = getLogger("QueueErrorHandler")

    def __init__(self, instance):
        self.requeue = 0
        self.reject = 0
        self.instance = instance

    def log_error(self, error):
        if issubclass(error.__class__, AppBaseError):
            self.logger.error(
                error.message,
                extra={
                    "object": error.obj,
                    "type": error.type,
                    "instance": error.instance,
                    "backtrace": traceback.format_exc().splitlines(),
                }
            )
        else:
            self.logger.error(
                error,
                extra={
                    "type": self.instance.__class__.__name__,
                    "backtrace": traceback.format_exc().splitlines(),

                }
            )
        raise error

    def process_message(self, message):
        if self.reject > 0:
            requeue = True if self.requeue > 0 else False
            message.reject(requeue=requeue)
        else:
            try:
                message.ack()
            except MessageStateError:
                self.logger.warning("Already ack message")
            self.logger.debug("ack OK")

    @contextmanager
    def handle_errors(self):
        try:
            yield
        except RequeueError as e:
            if e.message != "":
                self.log_error(e)
            self.requeue += 1
            self.reject += 1
        except FormattedWarning:
            pass
        except AppBaseError as e:
            self.log_error(e)
            self.reject += 1
        except Exception as e:
            self.log_error(e)
            self.reject += 1
