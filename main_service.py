#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

from time import sleep
import argparse
import json
import os.path
import pathlib2 as pathlib

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from google.assistant.library.device_helpers import register_device

from CamUtils.CamUtils import detect_smile, scan_qrcode

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

WARNING_NOT_REGISTERED = """
    This device is not registered. This means you will not be able to use
    Device Actions or see your device in Assistant Settings. In order to
    register this device follow instructions at:

    https://developers.google.com/assistant/sdk/guides/library/python/embed/register-device
"""

RICE_MENU = '/home/pi/WORKSPACE/YouSmileIServe/menu/rice_menu.txt'
NOODLE_MENU = '/home/pi/WORKSPACE/YouSmileIServe/menu/noodle_menu.txt'


def send_command(assistant_, query, delay=6.0):
    """ Send command to trigger certain events, then assistant listen to customer's speech """
    assistant_.send_text_query(query)
    sleep(delay)
    assistant_.start_conversation()


def fetch_menu(menu_file):
    """ Open menu file and return available meal options in text pattern """
    # wait for last conversation finished
    sleep(3.7)
    print('[CHECKING FOR AVAILABLE MEAL]')
    with open(menu_file) as f:
        menu_list = [item.strip() for item in f.readlines()]

    if len(menu_list) >= 2:
        return ' and '.join(menu_list) + ' are'
    else:
        return 'only ' + ' and '.join(menu_list) + ' is'


def fetch_recommendations(menu_file):
    """ Open menu file and return available meal options in text pattern """
    # wait for last conversation finished
    sleep(3.7)
    print('[CHECKING FOR AVAILABLE MEAL]')
    with open(menu_file) as f:
        menu_list = [item.strip() for item in f.readlines()]

    if len(menu_list) >= 2:
        menu_list = menu_list[:2]
        return ' and '.join(menu_list) + ' are'
    else:
        return 'only ' + ' and '.join(menu_list) + ' is'


def check_available_meal(assistant_, params_, meal_):
    """ Check available meal when customer ordering or asking for recommendation """
    if meal_ == 'rice':
        menu_file = RICE_MENU
    elif meal_ == 'noodle':
        menu_file = NOODLE_MENU

    query = str(params_['meal_{}'.format(meal_)])
    options = fetch_menu(menu_file)

    if query in options:
        send_command(assistant_, 'order confirmed, should notify customer to pay for the meal', 8.5)
    else:
        send_command(assistant_, '{} is not available, customer should try something other'.format(query), 6)


def process_event(event, assistant_):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
        assistant_(assistant.Assistant): Google assistant agent.
    """
    print("[EVENT]", event)

    # start new conversation automatically after each conversation turn
    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        assistant_.start_conversation()

    # notify customer if he/she pause for a significant amount of time
    if event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT:
        sleep(2)
        send_command(assistant_, 'customer stopped speaking', 4)

    # begin ordering session
    if event.type == EventType.ON_START_FINISHED:
        assistant_.send_text_query('customer start ordering')
        # assistant_.send_text_query('I want noodle')
        # assistant_.send_text_query('I want rice')
        # assistant_.send_text_query('customer need rice meal recommendation')
        # assistant_.send_text_query('customer need rice')
        # assistant_.send_text_query('we need gold')
        # assistant_.send_text_query('we need silver')
        # assistant_.send_text_query('I want beef noodle')
        # assistant_.send_text_query('customer finished payment')

    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in event.actions:
            print('Do command', command, 'with params', str(params))

            # scan QR code
            if command == 'com.smile.commands.MakeOrdering':
                is_finished = scan_qrcode()
                if is_finished:
                    sleep(2)
                    assistant_.send_text_query('customer finished payment')
                    sleep(5)

            # send 'meal is ready' after payment that followed by certain delay
            if command == 'com.smile.commands.FinishPayment':
                # send_command(assistant_, 'meal is ready', 8)
                # sleep(2)
                assistant_.send_text_query('meal is ready')
                sleep(5)

            # notify that the meal is ready, then quit current ordering session
            if command == 'com.smile.commands.MealReady':
                sleep(9)
                return True

            # check meal once customer ask for recommendation and order meal
            if command == 'com.smile.commands.CheckMeal':
                if str(params['meal_rice']) != '$meal_rice':
                    check_available_meal(assistant_, params, 'rice')
                elif str(params['meal_noodle']) != '$meal_noodle':
                    check_available_meal(assistant_, params, 'noodle')

            # customer ask for rice meal options
            if command == 'com.smile.commands.NeedRice':
                # rice_options = 'pork rice and chicken rice are'
                # rice_options = fetch_menu(RICE_MENU)
                # rice_options = fetch_recommendations(RICE_MENU)
                # print('customer need rice meal recommendation, '
                #                          '{} now available.'.format(rice_options))
                # send_command(assistant_, 'customer need rice meal recommendation, '
                #                          '{} now available.'.format(rice_options), 10)
                # send_command(assistant_, 'customer need rice meal recommendation', 5)
                send_command(assistant_, 'we need gold', 6)

            # customer ask for rice noodle options
            if command == 'com.smile.commands.NeedNoodle':
                # noodle_options = 'beef noodle and chicken noodle are'
                # noodle_options = fetch_menu(NOODLE_MENU)
                # noodle_options = fetch_recommendations(NOODLE_MENU)
                # send_command(assistant_, 'customer need noodle meal recommendation, '
                #                          '{} now available.'.format(noodle_options), 10)
                send_command(assistant_, 'we need silver', 6)

            # quit session manually
            if command == 'com.smile.commands.ConversationFinished':
                sleep(5)
                return True


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--device-model-id', '--device_model_id', type=str,
                        metavar='DEVICE_MODEL_ID', required=False,
                        help='the device model ID registered with Google')
    parser.add_argument('--project-id', '--project_id', type=str,
                        metavar='PROJECT_ID', required=False,
                        help='the project ID used to register this device')
    parser.add_argument('--device-config', type=str,
                        metavar='DEVICE_CONFIG_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'googlesamples-assistant',
                            'device_config_library.json'
                        ),
                        help='path to store and read device configuration')
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='path to store and read OAuth2 credentials')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + Assistant.__version_str__())

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    device_model_id = None
    last_device_id = None
    try:
        with open(args.device_config) as f:
            device_config = json.load(f)
            device_model_id = device_config['model_id']
            last_device_id = device_config.get('last_device_id', None)
    except FileNotFoundError:
        pass

    if not args.device_model_id and not device_model_id:
        raise Exception('Missing --device-model-id option')

    # Re-register if "device_model_id" is given by the user and it differs
    # from what we previously registered with.
    should_register = (
            args.device_model_id and args.device_model_id != device_model_id)

    device_model_id = args.device_model_id or device_model_id

    while True:
        with Assistant(credentials, device_model_id) as assistant:

            events = assistant.start()

            device_id = assistant.device_id
            print('device_model_id:', device_model_id)
            print('device_id:', device_id + '\n')

            # Re-register if "device_id" is different from the last "device_id":
            if should_register or (device_id != last_device_id):
                if args.project_id:
                    register_device(args.project_id, credentials,
                                    device_model_id, device_id)
                    pathlib.Path(os.path.dirname(args.device_config)).mkdir(
                        exist_ok=True)
                    with open(args.device_config, 'w') as f:
                        json.dump({
                            'last_device_id': device_id,
                            'model_id': device_model_id,
                        }, f)
                else:
                    print(WARNING_NOT_REGISTERED)

            # start smile detection for activating assistant
            is_smiled = detect_smile()
            # is_smiled = True
            # if smile is detected, start ordering session
            if is_smiled is True:
                assistant.set_mic_mute(False)
                for event in events:
                    is_over = process_event(event, assistant)
                    if is_over:
                        # Restart a new session of ordering
                        break


if __name__ == '__main__':
    main()
