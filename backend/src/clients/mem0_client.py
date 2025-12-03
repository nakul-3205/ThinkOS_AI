from mem0 import MemoryClient
import os
MEM0_API_KEY=os.getenv("MEM0_API_KEY")
mem0_client = MemoryClient(api_key=MEM0_API_KEY)
