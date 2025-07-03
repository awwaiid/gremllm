# Wet Pool Example Output

```
🏊‍♀️ === SWIMMING POOL SIMULATOR === 🏊‍♂️
A perfect demonstration of WET mode - where everything stays WET!
In wet mode, even splashes and water drops become living objects!

--- DRY POOL (boring!) ---
Created pool: <bound method Gremllm.__repr__ of 'Swimming pool object in tranquil state.'>
Cannonball splash height: Splash! The cannonball has been executed.
Type: <class 'str'> (just a number, how boring!)
Can't interact with the splash - it's just a dead value 😞

--- WET POOL (fun!) ---
Created wet pool: SwimmingPool object with no custom repr
Cannonball creates: None
Type: <class 'gremllm.core.Gremllm'> (it's ALIVE! 🌊)
The splash is a living none!
Splash creates ripples: None

--- SWIMMING ADVENTURES ---
Let's go swimming and see what wet objects we create!
Added swimmer: <Gremlin says: Error executing code: argument of type 'Gremllm' is not iterable>

--- POOL CHEMISTRY (with verbose!) ---
Let's see the wet magic happening under the hood:

Adding chlorine to the pool:
[GREMLLM swimming_pool.add_chlorine] Generated code:
==================================================
self._context['chlorine_level'] = self._context.get('chlorine_level', 0) + 2.5
result = Gremllm('number', wet=True, verbose=True)
result.value = self._context['chlorine_level']
==================================================
[GREMLLM number.value] Generated code:
==================================================
_context['value'] = 2.5
result = _context['value']
==================================================
[GREMLLM number.__repr__] Generated code:
==================================================
result = Gremllm('str', wet=True, verbose=True)
result.content = str(self._context.get('value'))
==================================================
[GREMLLM str.content] Generated code:
==================================================
_context['content'] = 2.5
result = _context['content']
==================================================
[GREMLLM str.__repr__] Generated code:
==================================================
result = Gremllm('attr', wet=True, verbose=True)
result.content = str(self.__repr__())
==================================================
[GREMLLM str.__repr__] Generated code:
==================================================
result = Gremllm('text', wet=True, verbose=True)
result.content = self.__repr__()
==================================================
[GREMLLM str.__repr__] Generated code:
==================================================
result = '__repr__'
==================================================
[GREMLLM text.content] Generated code:
==================================================
self._context['content'] = repr
result = None
==================================================
[GREMLLM text.__repr__] Generated code:
==================================================
result = _context.get('content')
==================================================
[GREMLLM attr.content] Generated code:
==================================================
import sys
_context['content'] = repr
result = _context['content']
==================================================
[GREMLLM attr.__repr__] Generated code:
==================================================
result = _context.get('__repr__')
==================================================
Chemical object: None

🌊 === WET MODE MAGIC === 🌊
In wet mode:
💧 Every drop of water is a living gremllm object
🌊 Splashes create ripples that create more objects
🏊 Swimmers create wakes, motions, and interactions
🧪 Even chemicals and cleaning become interactive
🔄 Objects inherit wetness - everything stays alive!
✨ Infinite emergent behavior from simple pool actions

Dive in and explore the endless possibilities! 🏊‍♀️💦

💡 Try running this example yourself and experiment with:
   - Different pool activities: diving, floating, racing
   - Pool equipment: filters, heaters, lights
   - Water chemistry: pH testing, adding chemicals
   - Multiple swimmers interacting with each other
   - Everything becomes a living, interactive gremllm object!
```
