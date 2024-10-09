import asyncio

# Define an async function
async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)  # Simulate a non-blocking delay
    print(f"Task {name} finished after {delay} seconds")

# Define the main async function
async def main():
    # Create multiple async tasks
    tasks = [
        task("A", 2),
        task("B", 3),
        task("C", 1)
    ]
    
    # Use asyncio.gather to await all tasks to finish
    await asyncio.gather(*tasks)

# Run the main function
asyncio.run(main())