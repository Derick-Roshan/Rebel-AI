
import asyncio
from backend.memory.facts import extract_facts


async def main():
    message = """
    My name is Roshan.
    I completed BE Computer Science in 2025.
    I am learning AWS and DevOps.
    My career goal is to become a Cloud Engineer.
    """

    facts = await extract_facts(message)

    print("\nExtracted Personal Facts:")
    for fact in facts:
        print(fact)


asyncio.run(main())

