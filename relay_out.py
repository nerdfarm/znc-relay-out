# pylint: disable=import-error,invalid-name,bare-except,unused-argument,no-self-use
""" Python ZNC module for passing IRC messages to mosquitto """

import re

import znc
import paho.mqtt.publish as publish


def _contains_required_args(args, required_args):
    """ Validates the arg string from ZNC contains required arg keys """
    return len([x for x in required_args if x in args]) == len(required_args)


def _parse_args(args, required_args):
    """ Parse args according to required args """
    module_args = {}
    split_args = []
    for index, token in enumerate([x for x in re.split("=|--", args.strip()) if x.strip()]):
        if token:
            if index % 2 == 0:
                split_args.append("--" + token.strip())
            else:
                split_args.append(token.strip())
    for arg in required_args:
        index = split_args.index(arg)
        if index > -1:
            value = split_args[index + 1]
            if value and value not in required_args:
                module_args[arg] = value.strip()
    return module_args


def _is_valid_module_args(parsed_args, required_args):
    """ Validate that parsed args have required args, and no values are None or empty strings """
    return len([x for x in required_args if x not in parsed_args.keys()]) == 0 and \
           len([x for x in parsed_args.values() if not x]) == 0


class relay_out(znc.Module):
    """ ZNC module with mosquitto publishing on IRC channel messages """

    description = "Relay messages from IRC to obs"
    module_types = [znc.CModInfo.UserModule]

    _PARAM_KEYS = {
        "_TOPIC_KEY": "--topic",
        "_HOST_KEY": "--host",
        "_PORT_KEY": "--port",
        "_QOS_KEY": "--qos",
        "_CLIENT_ID_KEY": "--client-id",
        "_NETWORK_NAME_KEY": "--network-name",
        "_CHANNEL_KEY": "--channel"
    }

    def __init__(self):
        self._client = None
        self._client_process = None
        self._module_args = {}

    def OnLoad(self, args, message):
        """
        Initialize client with this callback to avoid module loading issues with incomplete initialization
        """
        try:
            message.s = str(message.s) + "\n"
            if not _contains_required_args(args, list(relay_out._PARAM_KEYS.values())):
                message.s = "Missing required args, found: {}, required: {}".format(
                    args, str(list(relay_out._PARAM_KEYS.values())))
                return False
            message.s = str(message.s) + "Passed required arg check\n"
            parsed_args = _parse_args(args, list(relay_out._PARAM_KEYS.values()))
            message.s = str(message.s) + "Parsed module args\n"
            if not _is_valid_module_args(parsed_args, list(relay_out._PARAM_KEYS.values())):
                message.s = "Invalid module args, found: {}, required: {}".format(
                    str(parsed_args), str(list(relay_out._PARAM_KEYS.values())))
                return False
            message.s = str(message.s) + "Passed module arg check\n"
            self._module_args = parsed_args
            message.s = str(message.s) + "Module args: " + str(self._module_args) + "\n"
            return True
        except Exception as exception:
            # Catch all to ensure any exception will prevent the module from loading
            message.s = str(message.s) + "Failed to load module: \n" + str(exception)
            return False

    def OnChanMsg(self, nick, channel, message):
        """ Publish channel messages """
        if str(channel.GetName()).lower() == self._get_param("_CHANNEL_KEY").lower():
            self._publish_message("<{}> {}".format(str(nick.GetNick()), message))
        return znc.CONTINUE

    def OnChanAction(self, nick, channel, message):
        """ Publish /me actions """
        if str(channel.GetName()).lower() == self._get_param("_CHANNEL_KEY").lower():
            self._publish_message("* {} {}".format(str(nick.GetNick()), message))
        return znc.CONTINUE

    def _publish_message(self, message):
        """ Publish messages if ZNC user not attached """
        if not self.GetUser().IsUserAttached():
            publish.single(
                self._get_param("_TOPIC_KEY"),
                hostname=self._get_param("_HOST_KEY"),
                port=int(self._get_param("_PORT_KEY")),
                payload=message,
                qos=int(self._get_param("_QOS_KEY")),
                client_id=self._get_param("_CLIENT_ID_KEY"),
                retain=False
            )

    def OnModCommand(self, command):
        """ No commands yet """
        return znc.CONTINUE

    def GetWebMenuTitle(self):
        """ Title for web UI """
        return "relay_out IRC to mosquitto mq"

    def _get_param(self, key):
        """ Helper to get a module parameter """
        return self._module_args[relay_out._PARAM_KEYS[key]]
