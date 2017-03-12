import logging

from wxpy.api.bot import Bot
from wxpy.api.chats import Chat

logger = logging.getLogger(__name__)


def get_receiver(receiver=None):
    if isinstance(receiver, Chat):
        return receiver
    elif isinstance(receiver, Bot):
        return receiver.file_helper
    elif receiver is None:
        bot = Bot()
        return bot.file_helper
    else:
        raise TypeError('expected Chat, Bot or None')


class WeChatLoggingHandler(logging.Handler):
    def __init__(self, receiver=None):
        """
        可向指定微信聊天对象发送日志的 Logging Handler

        :param receiver:
            | 当为 `None` 时，将启动一个新的机器人，并发送到该机器人的"文件传输助手"
            | 当为 :class:`聊天对象 <Chat>` 时，将发送到该聊天对象
            | 当为 :class:`机器人 <Bot>` 时，将发送到该机器人的"文件传输助手"
        """

        super(WeChatLoggingHandler, self).__init__()
        self.receiver = get_receiver(receiver)

    def emit(self, record):
        # noinspection PyBroadException
        try:
            self.receiver.send(self.format(record))
        except:
            # Todo: 将异常输出到屏幕
            pass


def get_wechat_logger(receiver=None, name=None, level=logging.WARNING):
    """
    获得一个可向指定微信聊天对象发送日志的 Logger

    :param receiver:
        | 当为 `None` 时，将启动一个新的机器人，并发送到该机器人的"文件传输助手"
        | 当为 :class:`聊天对象 <Chat>` 时，将发送到该聊天对象
        | 当为 :class:`机器人 <Bot>` 时，将发送到该机器人的"文件传输助手"
    :param name: Logger 名称，默认为调用层的 `__name__`
    :param level: Logger 等级，默认为 `logging.INFO`
    :return: Logger
    """

    _logger = logging.getLogger(name=name)
    _logger.setLevel(level=level)
    _logger.addHandler(WeChatLoggingHandler(receiver=receiver))

    return _logger
