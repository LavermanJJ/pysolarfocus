# Async Solarfocus API

The `pysolarfocus` library now includes async support for non-blocking operations, making it ideal for integration with async frameworks like Home Assistant, FastAPI, or asyncio-based applications.

## Quick Start

```python
import asyncio
from pysolarfocus import AsyncSolarfocusAPI, Systems, ApiVersions

async def main():
    # Create async API instance
    api = AsyncSolarfocusAPI(
        ip="192.168.1.100",
        system=Systems.VAMPAIR,
        api_version=ApiVersions.V_25_030
    )
    
    # Initialize components (required for async API)
    await api.initialize()
    
    # Connect to the system
    if await api.connect():
        # Update all components in parallel
        await api.update(parallel=True, optimized=True)
        
        # Access component data
        print(api.heating_circuits[0])
        print(api.heatpump)
        
        # Disconnect when done
        await api.disconnect()

# Run the async function
asyncio.run(main())
```

## Key Features

### 1. Non-blocking Operations
All operations are async and won't block the event loop:

```python
# These operations don't block
await api.connect()
await api.update()
await api.update_heating()
```

### 2. Parallel Updates
Update multiple components simultaneously for better performance:

```python
# Update all components in parallel (default)
await api.update(parallel=True)

# Update specific components in parallel
await api.update_partial(["heating_circuits", "buffers"], parallel=True)
```

### 3. Optimized Updates
Use optimized update methods that bypass some overhead:

```python
# Standard update (uses sync component wrapper)
await api.update(parallel=True, optimized=False)

# Optimized update (direct async modbus operations)
await api.update(parallel=True, optimized=True)
```

### 4. Connection Management
Enhanced connection handling with automatic reconnection:

```python
api = AsyncSolarfocusAPI(
    ip="192.168.1.100",
    auto_reconnect=True,          # Enable auto-reconnection
    connection_timeout=10.0       # Connection timeout in seconds
)

# Check connection health
health = api.get_connection_health()
print(f"Connected: {health['is_connected']}")
print(f"Backoff: {health['connection_backoff']}s")
```

### 5. Health Monitoring
Monitor component and connection health:

```python
# Check if all components are healthy
if api.is_healthy():
    print("All components working correctly")
else:
    print(f"Failed components: {api.get_failed_components()}")
```

## API Comparison

| Operation | Sync API | Async API |
|-----------|----------|-----------|
| Connect | `api.connect()` | `await api.connect()` |
| Update | `api.update()` | `await api.update()` |
| Partial Update | Not available | `await api.update_partial([...])` |
| Parallel Updates | No | Yes (default) |
| Health Check | Limited | `api.get_connection_health()` |
| Auto-reconnect | No | Yes (configurable) |

## Integration Examples

### Home Assistant
```python
import asyncio
from homeassistant.core import HomeAssistant
from pysolarfocus import AsyncSolarfocusAPI

class SolarfocusDataCoordinator:
    def __init__(self, hass: HomeAssistant, api: AsyncSolarfocusAPI):
        self.hass = hass
        self.api = api
    
    async def async_update_data(self):
        """Update data from Solarfocus system"""
        if not self.api.is_connected:
            await self.api.connect()
        
        # Update only specific components for efficiency
        await self.api.update_partial([
            "heating_circuits", 
            "buffers", 
            "heatpump"
        ], parallel=True, optimized=True)
        
        return {
            "heating_circuit": self.api.heating_circuits[0],
            "buffer": self.api.buffers[0],
            "heatpump": self.api.heatpump
        }
```

### FastAPI
```python
from fastapi import FastAPI
from pysolarfocus import AsyncSolarfocusAPI

app = FastAPI()
api = AsyncSolarfocusAPI(ip="192.168.1.100")

@app.on_event("startup")
async def startup():
    await api.initialize()
    await api.connect()

@app.get("/heating-status")
async def get_heating_status():
    await api.update_heating()
    return {
        "temperature": api.heating_circuits[0].supply_temperature.scaled_value,
        "mode": api.heating_circuits[0].mode.value
    }

@app.on_event("shutdown")
async def shutdown():
    await api.disconnect()
```

## Performance Benefits

The async implementation provides several performance improvements:

1. **Non-blocking I/O**: Modbus operations don't block the event loop
2. **Parallel Updates**: Multiple components can be updated simultaneously
3. **Optimized Modbus Operations**: Direct async modbus calls avoid threading overhead
4. **Connection Pooling**: Better connection management with automatic reconnection
5. **Selective Updates**: Update only the components you need

## Backward Compatibility

The async API is fully compatible with the existing sync API. You can use both in the same application:

```python
from pysolarfocus import SolarfocusAPI, AsyncSolarfocusAPI

# Sync API (existing code continues to work)
sync_api = SolarfocusAPI(ip="192.168.1.100")
sync_api.connect()
sync_api.update()

# Async API (new functionality)
async_api = AsyncSolarfocusAPI(ip="192.168.1.100")
await async_api.initialize()
await async_api.connect()
await async_api.update()
```

## Error Handling

The async API provides enhanced error handling:

```python
try:
    await api.connect()
    await api.update()
except Exception as e:
    print(f"Error: {e}")
    
    # Check what failed
    failed_components = api.get_failed_components()
    if failed_components:
        print(f"Failed components: {failed_components}")
    
    # Check connection health
    health = api.get_connection_health()
    print(f"Connection health: {health}")
```

## Migration Guide

To migrate from sync to async API:

1. **Replace imports:**
   ```python
   # Old
   from pysolarfocus import SolarfocusAPI
   
   # New  
   from pysolarfocus import AsyncSolarfocusAPI
   ```

2. **Add async/await:**
   ```python
   # Old
   api = SolarfocusAPI(ip="192.168.1.100")
   api.connect()
   api.update()
   
   # New
   api = AsyncSolarfocusAPI(ip="192.168.1.100")
   await api.initialize()  # New requirement
   await api.connect()
   await api.update()
   ```

3. **Use new features:**
   ```python
   # Parallel updates
   await api.update(parallel=True)
   
   # Partial updates
   await api.update_partial(["heating_circuits"])
   
   # Health monitoring
   if not api.is_healthy():
       print("System issues detected")
   ```
