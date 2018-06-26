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
import logging

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from google.assistant.library.device_helpers import register_device

from .CamUtils.CamUtils import detect_smile, scan_qrcode

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

def fetch_menu(menu_path):
    with open(menu_path) as f:
        menu_list = [item.strip() for item in f.readlines()]
        if len(menu_list) >= 2:
            return ' and '.join(menu_list) + ' are'
        else:
            return 'only' + ' and '.join(menu_list) + ' is'

def on_make_order():
    # write status
    pass


def on_finished_payment():
    # set timer
    pass


def on_meal_ready():
    # write status; camera open for smile detection
    pass


# def scan_qrcode():
#     # write status; camera open
#     pass


def check_available_meal():
    # fetch data
    pass


def process_event(event, assistant_):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
        assistant_(assistant.Assistant): Google assistant agent.
        cam: cam
    """
    print("[EVENT]", event)
    logging.getLogger(__name__).info("[EVENT] " + str(event))

    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print("ON_CONVERSATION_TURN_STARTED")
        logging.getLogger(__name__).debug("ON_CONVERSATION_TURN_STARTED")

    if event.type == EventType.ON_MEDIA_STATE_IDLE:
        print("ON_MEDIA_STATE_IDLE")
        logging.getLogger(__name__).debug("ON_MEDIA_STATE_IDLE")

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        assistant_.start_conversation()
        print("ON_CONVERSATION_TURN_FINISHED")
        logging.getLogger(__name__).debug("ON_CONVERSATION_TURN_FINISHED")

    if event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT:
        print("ON_CONVERSATION_TURN_TIMEOUT ")
        logging.getLogger(__name__).debug("ON_CONVERSATION_TURN_TIMEOUT")
        sleep(2)
        assistant_.send_text_query('customer stopped speaking')
        sleep(4)
        assistant_.start_conversation()

    if event.type == EventType.ON_START_FINISHED:
        print("ON_START_FINISHED")
        logging.getLogger(__name__).debug("ON_START_FINISHED")
        assistant_.send_text_query('customer start ordering')

    if event.type == EventType.ON_DEVICE_ACTION:
        
        print("ON_DEVICE_ACTION")
        logging.getLogger(__name__).debug("ON_DEVICE_ACTION")
        for command, params in event.actions:
            print('Do command', command, 'with params', str(params))
            logging.getLogger(__name__).info('Do command' + str(command) +
                                             'with params' + str(params))

            if command == 'com.smile.commands.MealReady':
                on_meal_ready()
            if command == 'com.smile.commands.FinishPayment':
                assistant_.send_text_query('meal is ready')
                sleep(9)
                assistant_.start_conversation()
            if command == 'com.smile.commands.MakeOrdering':
                on_make_order()
                is_finished = scan_qrcode()
                if is_finished:
                    assistant_.send_text_query('customer finished payment')
                    sleep(6)

            if command == 'com.smile.commands.MealReady':
                sleep(10)
                return True
            
            if command == 'com.smile.commands.CheckMeal':
                if str(params['meal_rice']) == '$meal_rice':
                    sleep(4)
                    with open('/home/pi/.config/YouSmileIServe/menu/noodle_menu.txt'):
                        print('[FILE OPENED]')
                        noodle_options = fetch_menu('/home/pi/.config/YouSmileIServe/menu/noodle_menu.txt')
                    if str(params['meal_noodle']) in noodle_options:
                        assistant_.send_text_query('order confirmed, should notify customer to pay for the meal')
                        sleep(6.5)
                        assistant_.start_conversation()
                    else:
                        assistant_.send_text_query('{} is not available, customer should try something other'
                                                   .format(str(params['meal_noodle'])))
                        sleep(6.5)
                        assistant_.start_conversation()
                if str(params['meal_noodle']) == '$meal_noodle':
                    sleep(4)
                    with open('/home/pi/.config/YouSmileIServe/menu/rice_menu.txt'):
                        print('[FILE OPENED]')
                        rice_options = fetch_menu('/home/pi/.config/YouSmileIServe/menu/rice_menu.txt')
                    if str(params['meal_rice']) in rice_options:
                        assistant_.send_text_query('order confirmed, should notify customer to pay for the meal')
                        sleep(6.5)
                        assistant_.start_conversation()
                    else:
                        assistant_.send_text_query('{} is not available, customer should try something other'
                                                   .format(str(params['meal_rice'])))
                        sleep(6.5)
                        assistant_.start_conversation()
            

            if command == 'com.smile.commands.NeedRice':
                logging.getLogger(__name__).info(" start commands.NeedRice")
                # print("[INFO] start commands.NeedRice")
                # rice_options = 'pork rice and chicken rice are'
                rice_options = fetch_menu('/home/pi/.config/YouSmileIServe/menu/rice_menu.txt')
                assistant_.send_text_query('customer need rice meal recommendation, '
                                           '{} now available.'.format(rice_options))
                sleep(6)
                assistant_.start_conversation()

            if command == 'com.smile.commands.NeedNoodle':
                logging.getLogger(__name__).info(" start commands.NeedNoodle")
                noodle_options = fetch_menu('/home/pi/.config/YouSmileIServe/menu/noodle_menu.txt')
                # rice_options = 'beef noodle and chicken noodle are'
                assistant_.send_text_query('customer need noodle meal recommendation, '
                                           '{} now available.'.format(noodle_options))
                sleep(6)
                assistant_.start_conversation()
                
            if command == 'com.smile.commands.ConversationFinished':
                sleep(6)
                return True


def run_cli():
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="It is a robot that it can hlep people to order what you want")
    
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

    parser.add_argument('-d', '--debug', action='store_true',
                        help="Print debug level information")
    
    parser.add_argument('-l', '--list', action='store_true',
                        help="List menu that you can order")    

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        
    if args.list:
        print("The menu is:")
        print("   " + str(fetch_menu('/home/pi/.config/YouSmileIServe/menu/rice_menu.txt'))[:-3])
        print("   " + str(fetch_menu('/home/pi/.config/YouSmileIServe/menu/noodle_menu.txt'))[:-3])
        print("\n")

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
            logging.getLogger(__name__).debug('device_model_id:' + str(device_model_id))
            logging.getLogger(__name__).debug('device_id:' + str(device_id) + '\n')
            # print('device_model_id:', device_model_id)
            # print('device_id:', device_id + '\n')

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
                    logging.getLogger(__name__).warning(WARNING_NOT_REGISTERED)
                    # print(WARNING_NOT_REGISTERED)

            # start smile detection for activating assistant
            is_smiled = detect_smile()
            if is_smiled is True:
                assistant.set_mic_mute(False)
                for event in events:
                    is_over = process_event(event, assistant)
                    if is_over:
                        break
    logging.getLogger(__name__).info("Service is Over")               
    logging.shutdown()


if __name__ == '__main__':
    run_cli()

