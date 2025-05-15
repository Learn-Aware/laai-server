import json


class System_Instruction:

    @staticmethod
    def load_instructions():
        """Load instructions from a JSON file."""
        try:
            with open("core/prompt/instruction.json", "r") as file:
                instructions = json.load(file)
            return instructions
        except FileNotFoundError:
            print("Error: The instructions JSON file is missing.")
            return {}
        except json.JSONDecodeError:
            print("Error: Failed to decode the JSON file.")
            return {}

    def system_instruction(scenario):
        instructions = System_Instruction.load_instructions()
        # print(instructions)
        if scenario in instructions:
            instruction_data = instructions[scenario]
            description = instruction_data.get(
                "description", "No description available."
            )
            steps = instruction_data.get("steps", [])

            # Format the output based on the instructions
            formatted_instructions = f"{description}\n"
            formatted_instructions += "\n".join([f"* {step}" for step in steps])

            return formatted_instructions
        else:
            return f"No instructions found for scenario '{scenario}'."
