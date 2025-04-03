from bot.core.config import Config


class BotHelp:
    def __init__(self, file: str) -> None:
        self.filename = file
        self.command_dict = {}
        self.command_info = ""

    def add(
        self,
        command: str,
        parameters: str = None,
        description: str = None,
        example: str = None,
        note: str = None,
    ):
        self.command_dict[command] = {
            "command": command,
            "parameters": parameters,
            "description": description,
            "example": example,
            "note": note,
        }
        return self

    def info(self, command_info: str):
        self.command_info = command_info
        return self

    def get_menu(self) -> str:
        result = f"File: {self.filename}"
        if self.command_info:
            result += f"\nInfo: {self.command_info}"
        result += "\n\n"
        for command in self.command_dict:
            command = self.command_dict[command]
            result += f"Command: {command['command']}"
            if command["parameters"]:
                result += f"{command['parameters']}"
            else:
                result += "\n"
            if command["description"]:
                result += f"Description: {command['description']}"
            if command["example"]:
                result += f"Example: {command['example']}"
            if command["note"]:
                result += f"Note: {command['note']}"

            result += '\n'

            Config.BOT_CMD_INFO[command["command"]] = {
                "command": f"{command['command']} {command['parameters'] if command['parameters'] else  ''}",
                "description": command["description"],
                "example": command['example'],
                "note": command['note'],
                "plugin": self.filename,
            }

        return result

    def done(self) -> None:
        Config.BOT_HELP[self.filename] = {
            "commands": self.command_dict,
            "info": self.command_info,
        }
        Config.BOT_CMD_MENU[self.filename] = self.get_menu()


