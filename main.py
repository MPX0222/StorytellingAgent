from agents.joey_agent import JoeyAgent
from agents.robert_agent import RobertAgent
from world.game_manager import GameManager
from config.settings import get_llm_config, get_game_settings
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

def display_status(game):
    """Display current game status"""
    print("\n" + "="*50)
    print(f"Time: {game.current_time}")
    print(f"Current Location: {game.player_state['location']}")
    print(f"Time Loop Cycle: {game.cycle_count}")
    
    if game.player_state["knowledge"]:
        print("\nDiscovered Information:")
        for info in game.player_state["knowledge"]:
            print(f"  • {info}")
    print("="*50)

def display_menu(actions):
    """Display available actions menu"""
    print("\nAvailable Actions:")
    print("-"*20)
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")
    print(f"{len(actions) + 1}. Quit Game")
    print("-"*20)

async def handle_conversation(game, target, chosen_action):
    """Handle conversation with NPCs"""
    print(f"\nStarting conversation with {target.title()}...")
    print("(Type 'exit' to end conversation)")
    
    while True:
        message = input("\nYou: ").strip()
        if message.lower() == 'exit':
            print("\nEnding conversation...")
            break
            
        responses = await game.process_player_action(message, target)
        
        # Display responses
        for agent_id, response in responses.items():
            if agent_id == "narrative":
                print(f"\n[Narrative] {response}")
            else:
                print(f"\n{agent_id.title()}: {response}")

async def main():
    # Initialize game
    game = GameManager()
    
    # Create and register agents
    joey = JoeyAgent()
    robert = RobertAgent()
    
    game.register_agent("joey", joey)
    game.register_agent("robert", robert)
    
    # Introduction
    print("\n" + "="*50)
    print("Welcome to Sharp School".center(50))
    print("="*50)
    print("\nYou are a 20-year-old Labor class student...")
    print("Your goal is to pass the exam and change your fate.")
    print("\nPress Enter to begin...")
    input()
    
    # Game loop
    while game.game_state == "running":
        display_status(game)
        
        # Get and display available actions
        actions = game.get_available_actions()
        display_menu(actions)
        
        # Get player choice
        try:
            choice = input("\nEnter your choice (number): ").strip()
            
            # Handle quit
            if choice == str(len(actions) + 1):
                print("\nAre you sure you want to quit? (yes/no)")
                if input().lower().startswith('y'):
                    game.game_state = "quit"
                    print("\nThanks for playing!")
                    break
                continue
                
            choice = int(choice)
            if 1 <= choice <= len(actions):
                chosen_action = actions[choice - 1]
                
                # Handle different types of actions
                if "Talk" in chosen_action:
                    target = "joey" if "Joey" in chosen_action or "door" in chosen_action else "robert"
                    await handle_conversation(game, target, chosen_action)
                    
                else:
                    print(f"\nExecuting: {chosen_action}")
                    responses = await game.process_player_action(chosen_action)
                    
                    if responses.get("narrative"):
                        print(f"\n[Narrative] {responses['narrative']}")
                    
                    # Display any ambient dialogue from NPCs
                    for agent_id, response in responses.items():
                        if agent_id.endswith("_ambient"):
                            npc_name = agent_id.replace("_ambient", "").title()
                            print(f"\n{npc_name}: {response}")
                
            else:
                print("\nInvalid choice. Please select a number from the menu.")
                
        except ValueError:
            print("\nInvalid input. Please enter a number.")
            
        # Add a small pause between turns
        print("\nPress Enter to continue...")
        input()

if __name__ == "__main__":
    asyncio.run(main()) 