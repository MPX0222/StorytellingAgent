from colorama import init, Fore, Back, Style
init()  # Initialize colorama

class UIHelper:
    @staticmethod
    def format_title(text: str) -> str:
        """Format game title"""
        return f"{Fore.CYAN}=== {text} ==={Style.RESET_ALL}"
    
    @staticmethod
    def format_dialogue_header(agent_name: str) -> str:
        """Format dialogue header"""
        return (
            f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n"
            f"{Fore.YELLOW}[Dialogue with {agent_name}]{Style.RESET_ALL}\n"
        )
    
    @staticmethod
    def format_dialogue_prompt(agent_name: str) -> str:
        """Format dialogue prompt"""
        return (
            f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n"
            f"{Fore.YELLOW}[In dialogue with {agent_name}]{Style.RESET_ALL}\n"
            f"What would you like to say? {Fore.GREEN}(type 'exit' to end conversation){Style.RESET_ALL}"
        )
    
    @staticmethod
    def format_agent_response(response: str, is_action: bool = False) -> str:
        """Format agent response"""
        if is_action:
            return f"{Fore.CYAN}*{response.strip('*')}*{Style.RESET_ALL}"
        return f"{Fore.WHITE}{response}{Style.RESET_ALL}"
    
    @staticmethod
    def format_time(time: str, cycle: int = 0) -> str:
        """Format time display"""
        time_str = f"{Fore.YELLOW}Time: {time}{Style.RESET_ALL}"
        if cycle > 0:
            time_str += f" {Fore.RED}[Time Loop #{cycle}]{Style.RESET_ALL}"
        return time_str
    
    @staticmethod
    def format_game_prompt(prompt: str) -> str:
        """Format game prompt"""
        return f"{Fore.GREEN}{prompt}{Style.RESET_ALL}"
        
    @staticmethod
    def format_warning(text: str) -> str:
        """Format warning messages"""
        return f"{Fore.RED}{text}{Style.RESET_ALL}"
        
    @staticmethod
    def format_event(text: str) -> str:
        """Format event messages"""
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
        
    @staticmethod
    def format_game_prompt(prompt: str) -> str:
        return f"{Fore.GREEN}{prompt}{Style.RESET_ALL}" 