from agent import Agent

def main():
    print("="*60)
    print("AI AGENT")
    print("="*60)
    print("Available tools: Calculator, Time, Weather, Air Quality, Country Info")
    print("Type 'exit' to quit.")
    print()

    agent = Agent()
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit"]:
            break

        try:
            response = agent.run(user_input)
            print(f"\nAgent: {response}\n")

        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()