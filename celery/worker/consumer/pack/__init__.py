import threading

from celery.utils import noop
from celery.worker.consumer import consumer

OldConsumer = consumer.Consumer


class SelfConsumer(OldConsumer):
    def __init__(self, on_task_request, init_callback=noop, hostname=None, pool=None, app=None, timer=None,
                 controller=None, hub=None, amqheartbeat=None, worker_options=None, disable_rate_limits=False,
                 initial_prefetch_count=2, prefetch_multiplier=1, **kwargs):
        super().__init__(on_task_request, init_callback, hostname, pool, app, timer, controller, hub, amqheartbeat,
                         worker_options, disable_rate_limits, None, prefetch_multiplier, **kwargs)
        self.initial_prefetch_count = None
        self.prefetch_multiplier = None

        print('using self defined')

    def _update_prefetch_count(self, index=0):
        self.initial_prefetch_count = None
        self.prefetch_multiplier = None
        return self._update_qos_eventually(index)


class PackQoS(object):
    """Thread safe increment/decrement of a channels prefetch_count.

    Arguments:
        callback (Callable): Function used to set new prefetch count,
            e.g. ``consumer.qos`` or ``channel.basic_qos``.  Will be called
            with a single ``prefetch_count`` keyword argument.
        initial_value (int): Initial prefetch count value..

    Example:
        >>> from kombu import Consumer, Connection
        >>> connection = Connection('amqp://')
        >>> consumer = Consumer(connection)
        >>> qos = QoS(consumer.qos, initial_prefetch_count=2)
        >>> qos.update()  # set initial

        >>> qos.value
        2

        >>> def in_some_thread():
        ...     qos.increment_eventually()

        >>> def in_some_other_thread():
        ...     qos.decrement_eventually()

        >>> while 1:
        ...    if qos.prev != qos.value:
        ...        qos.update()  # prefetch changed so update.

    It can be used with any function supporting a ``prefetch_count`` keyword
    argument::

        >>> channel = connection.channel()
        >>> QoS(channel.basic_qos, 10)


        >>> def set_qos(prefetch_count):
        ...     print('prefetch count now: %r' % (prefetch_count,))
        >>> QoS(set_qos, 10)
    """

    prev = None

    def __init__(self, callback, initial_value):
        self.callback = callback
        self._mutex = threading.RLock()
        self.value = None

    def increment_eventually(self, n=1):
        """Increment the value, but do not update the channels QoS.

        Note:
            The MainThread will be responsible for calling :meth:`update`
            when necessary.
        """
        pass

    def decrement_eventually(self, n=1):
        """Decrement the value, but do not update the channels QoS.

        Note:
            The MainThread will be responsible for calling :meth:`update`
            when necessary.
        """
        pass

    def set(self, pcount):
        """Set channel prefetch_count setting."""
        pass

    def update(self):
        """Update prefetch count with current value."""
        pass
