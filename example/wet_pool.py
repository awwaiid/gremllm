#!/usr/bin/env python3
"""
Swimming Pool Simulator - Demonstrating wet mode with a fun water-themed example!

In wet mode, everything returns gremllm objects, creating an immersive experience
where even drops of water and splashes become "alive" and interactive.
"""

from gremllm import Gremllm


def main():
    print("🏊‍♀️ === SWIMMING POOL SIMULATOR === 🏊‍♂️")
    print("A perfect demonstration of WET mode - where everything stays WET!")
    print("In wet mode, even splashes and water drops become living objects!\n")

    print("--- DRY POOL (boring!) ---")
    dry_pool = Gremllm("swimming_pool")
    print(f"Created pool: {dry_pool}")

    # In dry mode, jumping returns boring plain values
    splash_height = dry_pool.cannonball()
    print(f"Cannonball splash height: {splash_height}")
    print(f"Type: {type(splash_height)} (just a number, how boring!)")
    print("Can't interact with the splash - it's just a dead value 😞\n")

    print("--- WET POOL (fun!) ---")
    wet_pool = Gremllm("swimming_pool", wet=True)
    print(f"Created wet pool: {wet_pool}")

    # In wet mode, everything becomes alive!
    splash = wet_pool.cannonball()
    print(f"Cannonball creates: {splash}")
    print(f"Type: {type(splash)} (it's ALIVE! 🌊)")

    if hasattr(splash, "_identity"):
        print(f"The splash is a living {splash._identity}!")

        # The splash itself can do things!
        echo = splash.create_ripples()
        print(f"Splash creates ripples: {echo}")

        if hasattr(echo, "_identity"):
            print(f"Even the ripples are alive: {echo._identity}")

    print("\n--- SWIMMING ADVENTURES ---")
    print("Let's go swimming and see what wet objects we create!")

    # Add a swimmer to our wet pool
    swimmer = wet_pool.add_swimmer("Alice")
    print(f"Added swimmer: {swimmer}")

    if hasattr(swimmer, "_identity"):
        print(f"Swimmer identity: {swimmer._identity}")

        # Swimmers can do actions that create more wet objects
        backstroke = swimmer.do_backstroke()
        print(f"Alice does backstroke: {backstroke}")

        if hasattr(backstroke, "_identity"):
            print(f"The backstroke motion: {backstroke._identity}")

    print("\n--- POOL CHEMISTRY (with verbose!) ---")
    print("Let's see the wet magic happening under the hood:")

    verbose_pool = Gremllm("swimming_pool", wet=True, verbose=True)
    print("\nAdding chlorine to the pool:")
    chemical = verbose_pool.add_chlorine(2.5)

    if hasattr(chemical, "_identity"):
        print(f"Chemical object: {chemical}")

    print("\n🌊 === WET MODE MAGIC === 🌊")
    print("In wet mode:")
    print("💧 Every drop of water is a living gremllm object")
    print("🌊 Splashes create ripples that create more objects")
    print("🏊 Swimmers create wakes, motions, and interactions")
    print("🧪 Even chemicals and cleaning become interactive")
    print("🔄 Objects inherit wetness - everything stays alive!")
    print("✨ Infinite emergent behavior from simple pool actions")
    print("\nDive in and explore the endless possibilities! 🏊‍♀️💦")
    print("\n💡 Try running this example yourself and experiment with:")
    print("   - Different pool activities: diving, floating, racing")
    print("   - Pool equipment: filters, heaters, lights")
    print("   - Water chemistry: pH testing, adding chemicals")
    print("   - Multiple swimmers interacting with each other")
    print("   - Everything becomes a living, interactive gremllm object!")


if __name__ == "__main__":
    main()
