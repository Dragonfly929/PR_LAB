from player import Player
import xml.etree.ElementTree as ET
from datetime import datetime
import base64
import proto.player_pb2
import player_pb2
import google.protobuf
from google.protobuf import descriptor as _descriptor


# C:\Users\zaica\PycharmProjects\PR_LABS_TASKS-main (1)\PR_LABS_TASKS-main


class PlayerFactory:
    def to_json(self, players):
        '''
        This function should transform a list of Player objects into a list with dictionaries.
        '''
        player_list = []
        for player in players:
            player_dict = {
                "nickname": player.nickname,
                "email": player.email,
                "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                "xp": player.xp,
                "class": player.cls
            }
            player_list.append(player_dict)
        return player_list

    def from_json(self, list_of_dict):
        '''
        This function should transform a list of dictionaries into a list with Player objects.
        '''
        players = []
        for player_dict in list_of_dict:
            players.append(Player(
                player_dict["nickname"],
                player_dict["email"],
                player_dict["date_of_birth"],
                player_dict["xp"],
                player_dict["class"]
            ))
        return players

    def from_xml(self, xml_string):
        players = []
        root = ET.fromstring(xml_string)
        for player_elem in root.findall('player'):
            player_data = {}
            for elem in player_elem:
                player_data[elem.tag] = elem.text
            player_class = player_data.get("class", "Unknown")
            date_of_birth_str = str(player_data["date_of_birth"])
            players.append(Player(
                player_data["nickname"],
                player_data["email"],
                date_of_birth_str,
                int(player_data["xp"]),
                player_class
            ))
        return players

    def to_xml(self, list_of_players):
        '''
        This function should transform a list with Player objects into an XML string.
        '''
        root = ET.Element('data')
        for player in list_of_players:
            player_elem = ET.SubElement(root, 'player')
            for key, value in player.__dict__.items():
                if key == "date_of_birth":
                    value = value.strftime("%Y-%m-%d")
                if key == "cls":
                    key = "class"
                ET.SubElement(player_elem, key).text = str(value)

        xml_string = ET.tostring(root, encoding="unicode")
        return xml_string

    def from_protobuf(self, binary):
        '''
        This function should transform a binary protobuf string into a list with Player objects.
        '''
        player_messages = []

        player_msg = player_pb2.Player()

        while binary:
            player_size = player_msg.ParseFromString(binary)
            player_messages.append(player_msg)

            binary = binary[player_size:]

        players = []
        for player_msg in player_messages:
            player = Player(
                player_msg.nickname,
                player_msg.email,
                player_msg.date_of_birth,
                player_msg.xp,
                player_msg.cls
            )
            players.append(player)

        return players

    def to_protobuf(self, list_of_players):
        '''
        This function should transform a list with Player objects into a binary protobuf string.
        '''
        player_messages = []

        for player in list_of_players:
            player_msg = player_pb2.Player()
            player_msg.nickname = player.nickname
            player_msg.email = player.email
            player_msg.date_of_birth = player.date_of_birth
            player_msg.xp = player.xp
            player_msg.cls = player.cls

            player_messages.append(player_msg)

        binary_data = b''.join([p.SerializeToString() for p in player_messages])

        return binary_data
