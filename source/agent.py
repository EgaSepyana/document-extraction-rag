"""
# Multi-Agent System using Google Gemini LLM

# Install required packages:
# pip install google-generativeai
# """

# import google.generativeai as genai
# from typing import List, Dict, Any, Optional
# from dataclasses import dataclass, field
# import json
# import time

# # Configure your API key
# # Get your API key from: https://makersuite.google.com/app/apikey
# GOOGLE_API_KEY = ""
# genai.configure(api_key=GOOGLE_API_KEY)


# @dataclass
# class Message:
#     """Represents a message between agents"""
#     sender: str
#     receiver: str
#     content: str
#     timestamp: float = field(default_factory=time.time)
#     metadata: Dict[str, Any] = field(default_factory=dict)


# class Agent:
#     """Base AI Agent class using Google Gemini"""
    
#     def __init__(
#         self,
#         name: str,
#         role: str,
#         system_prompt: str,
#         model_name: str = "gemini-2.5-flash"
#     ):
#         self.name = name
#         self.role = role
#         self.system_prompt = system_prompt
#         self.model = genai.GenerativeModel(model_name)
#         self.message_history: List[Message] = []
#         self.memory: List[Dict[str, str]] = []
        
#     def process_message(self, message: Message) -> str:
#         """Process incoming message and generate response"""
#         # Add message to history
#         self.message_history.append(message)
        
#         # Build context from memory
#         context = self._build_context()
        
#         # Create prompt with system instructions and context
#         full_prompt = f"""You are {self.name}, a {self.role}.

# {self.system_prompt}

# Previous context:
# {context}

# Incoming message from {message.sender}:
# {message.content}

# Respond as {self.name}:"""
        
#         # Generate response using Gemini
#         response = self.model.generate_content(full_prompt)
#         response_text = response.text
        
#         # Store in memory
#         self.memory.append({
#             "role": "user",
#             "parts": [message.content]
#         })
#         self.memory.append({
#             "role": "model",
#             "parts": [response_text]
#         })
        
#         return response_text
    
#     def _build_context(self, max_messages: int = 5) -> str:
#         """Build context from recent message history"""
#         recent_messages = self.message_history[-max_messages:]
#         context_lines = []
#         for msg in recent_messages:
#             context_lines.append(f"{msg.sender}: {msg.content}")
#         return "\n".join(context_lines) if context_lines else "No previous context"
    
#     def send_message(self, receiver: str, content: str) -> Message:
#         """Create a message to send to another agent"""
#         return Message(sender=self.name, receiver=receiver, content=content)


# class MultiAgentOrchestrator:
#     """Orchestrates communication between multiple agents"""
    
#     def __init__(self):
#         self.agents: Dict[str, Agent] = {}
#         self.message_queue: List[Message] = []
        
#     def register_agent(self, agent: Agent):
#         """Register an agent with the orchestrator"""
#         self.agents[agent.name] = agent
#         print(f"Registered agent: {agent.name} ({agent.role})")
        
#     def send_message(self, message: Message):
#         """Send a message from one agent to another"""
#         if message.receiver not in self.agents:
#             raise ValueError(f"Receiver {message.receiver} not found")
        
#         receiver_agent = self.agents[message.receiver]
#         response_text = receiver_agent.process_message(message)
        
#         print(f"\n--- {message.sender} -> {message.receiver} ---")
#         print(f"Message: {message.content}")
#         print(f"Response: {response_text}")
        
#         return response_text
    
#     def broadcast_message(self, sender: str, content: str):
#         """Broadcast a message to all agents except sender"""
#         responses = {}
#         for agent_name, agent in self.agents.items():
#             if agent_name != sender:
#                 message = Message(sender=sender, receiver=agent_name, content=content)
#                 response = self.send_message(message)
#                 responses[agent_name] = response
#         return responses
    
#     def conversation_chain(self, messages: List[tuple]):
#         """Execute a chain of conversations between agents"""
#         responses = []
#         for sender, receiver, content in messages:
#             message = Message(sender=sender, receiver=receiver, content=content)
#             response = self.send_message(message)
#             responses.append(response)
#         return responses


# # Example Usage
# def main():
#     # Initialize orchestrator
#     orchestrator = MultiAgentOrchestrator()
    
#     # Create specialized agents
#     researcher = Agent(
#         name="Researcher",
#         role="Research Specialist",
#         system_prompt="""You are a research specialist who gathers and analyzes information.
#         You provide detailed, factual responses based on the latest knowledge.
#         Focus on accuracy and thoroughness."""
#     )
    
#     writer = Agent(
#         name="Writer",
#         role="Content Writer",
#         system_prompt="""You are a creative content writer who transforms information
#         into engaging, well-structured content. You focus on clarity, flow, and readability."""
#     )
    
#     critic = Agent(
#         name="Critic",
#         role="Quality Reviewer",
#         system_prompt="""You are a quality reviewer who evaluates content critically.
#         You identify improvements, check for accuracy, and suggest refinements."""
#     )
    
#     # Register agents
#     orchestrator.register_agent(researcher)
#     orchestrator.register_agent(writer)
#     orchestrator.register_agent(critic)
    
#     # Example 1: Simple conversation
#     print("\n" + "="*60)
#     print("EXAMPLE 1: Simple Agent-to-Agent Conversation")
#     print("="*60)
    
#     msg1 = Message(
#         sender="User",
#         receiver="Researcher",
#         content="What are the key benefits of multi-agent AI systems?"
#     )
#     research_response = orchestrator.send_message(msg1)
    
#     # Writer creates content based on research
#     msg2 = Message(
#         sender="Researcher",
#         receiver="Writer",
#         content=f"Based on my research: {research_response}\n\nPlease write a brief article about this."
#     )
#     article = orchestrator.send_message(msg2)
    
#     # Critic reviews the article
#     msg3 = Message(
#         sender="Writer",
#         receiver="Critic",
#         content=f"Here's my article: {article}\n\nPlease review and provide feedback."
#     )
#     review = orchestrator.send_message(msg3)
    
#     # Example 2: Conversation chain
#     print("\n" + "="*60)
#     print("EXAMPLE 2: Collaborative Problem Solving")
#     print("="*60)
    
#     chain = [
#         ("User", "Researcher", "Research the concept of emergent behavior in AI agents"),
#         ("Researcher", "Writer", "Create a simple explanation of the research findings"),
#         ("Writer", "Critic", "Review this explanation for accuracy and clarity"),
#     ]
    
#     orchestrator.conversation_chain(chain)
    
#     # Example 3: Broadcast
#     print("\n" + "="*60)
#     print("EXAMPLE 3: Broadcasting to All Agents")
#     print("="*60)
    
#     orchestrator.broadcast_message(
#         "User",
#         "What are your thoughts on the future of AI collaboration?"
#     )


# if __name__ == "__main__":
#     # Make sure to set your API key before running
#     if GOOGLE_API_KEY == "your-api-key-here":
#         print("Please set your Google API key in the GOOGLE_API_KEY variable")
#         print("Get your key from: https://makersuite.google.com/app/apikey")
#     else:
#         main()