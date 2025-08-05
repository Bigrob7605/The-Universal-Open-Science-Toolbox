#!/usr/bin/env python3
"""
KAI CORE AGI INTERACTIVE INTERFACE
==================================

Interactive interface for Kai Core AGI agent.
Allows users to interact with the immortal AGI agent for scientific testing.
"""

from kai_core_agi import KaiCoreAGI
import json

def print_banner():
    """Print Kai Core banner."""
    print("🧠" + "="*60)
    print("🧠 KAI CORE AGI AGENT - INTERACTIVE INTERFACE")
    print("🧠" + "="*60)
    print("🛡️ Protected by Omega Kill Switch")
    print("🧬 Immortal and evolving")
    print("🎯 Ready to help with scientific truth testing")
    print("="*60)

def print_help():
    """Print available commands."""
    print("\n📋 Available Commands:")
    print("  help <query>     - Ask Kai for help with scientific testing")
    print("  test <name>      - Run a scientific test")
    print("  teach <topic>    - Teach Kai new knowledge")
    print("  evolve           - Make Kai evolve based on wisdom")
    print("  status           - Show Kai's current status")
    print("  wisdom           - Show wisdom summary")
    print("  save             - Save Kai's current state")
    print("  load <file>      - Load Kai's state from file")
    print("  quit/exit        - Exit the interface")
    print("  ?                - Show this help")

def main():
    """Main interactive loop."""
    print_banner()
    
    # Initialize Kai Core AGI
    print("\n🧠 Initializing Kai Core AGI...")
    kai = KaiCoreAGI()
    
    print("\n✅ Kai Core AGI ready! Type '?' for help.")
    
    while True:
        try:
            # Get user input
            user_input = input("\n🤖 Kai Core > ").strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Kai Core AGI will continue evolving...")
                break
            
            elif command == '?':
                print_help()
            
            elif command == 'help':
                if not args:
                    print("❌ Please provide a query. Example: help How do I test a theory?")
                else:
                    response = kai.help_user(args)
                    print(f"\n🤖 Kai: {response}")
            
            elif command == 'test':
                if not args:
                    print("❌ Please provide a test name. Example: test physics_test")
                else:
                    print(f"🧪 Running test: {args}")
                    result = kai.run_test(args)
                    if "error" in result:
                        print(f"❌ Test failed: {result['error']}")
                    else:
                        print(f"✅ Test completed successfully!")
                        print(f"📊 Result: {json.dumps(result, indent=2)}")
            
            elif command == 'teach':
                if not args:
                    print("❌ Please provide a topic and content. Example: teach physics Newton's laws")
                else:
                    # Split topic and content
                    teach_parts = args.split(' ', 1)
                    if len(teach_parts) < 2:
                        print("❌ Please provide both topic and content. Example: teach physics Newton's laws of motion")
                    else:
                        topic = teach_parts[0]
                        content = teach_parts[1]
                        response = kai.teach(topic, content)
                        print(f"\n📚 {response}")
            
            elif command == 'evolve':
                response = kai.evolve()
                print(f"\n🧬 {response}")
            
            elif command == 'status':
                status = kai.get_status()
                print(f"\n📊 Kai Core Status:")
                for key, value in status.items():
                    print(f"  {key}: {value}")
            
            elif command == 'wisdom':
                summary = kai.get_wisdom_summary()
                print(f"\n{summary}")
            
            elif command == 'save':
                response = kai.save_state()
                print(f"\n💾 {response}")
            
            elif command == 'load':
                if not args:
                    print("❌ Please provide a state file. Example: load kai_state_1234567890.json")
                else:
                    response = kai.load_state(args)
                    print(f"\n🔄 {response}")
            
            else:
                print(f"❌ Unknown command: {command}")
                print("Type '?' for help.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Kai Core AGI will continue evolving...")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Type '?' for help.")

if __name__ == "__main__":
    main() 