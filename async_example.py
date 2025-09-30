"""Async example for pysolarfocus"""
import asyncio
from pysolarfocus import ApiVersions, AsyncSolarfocusAPI, Systems


async def main():
    """Main async example function"""
    # Example 1: Manual connection management
    await example_manual_connection()
    
    print("\n" + "="*80)
    print("Context Manager Example")
    print("="*80)
    
    # Example 2: Using async context manager (recommended)
    await example_context_manager()


async def example_manual_connection():
    """Example with manual connection management"""
    # Create the Async Solarfocus API client
    solarfocus = AsyncSolarfocusAPI(
        ip="10.10.10.237",  # adapt IP-Address
        system=Systems.VAMPAIR,  # change to Systems.THERMINATOR for biomass boiler systems
        api_version=ApiVersions.V_25_030,  # select Solarfocus version
        auto_reconnect=True,
        connection_timeout=10.0
    )

    # Initialize components (required for async API)
    await solarfocus.initialize()

    # Connect to the heating system
    if not await solarfocus.connect():
        print("Connecting to solarfocus failed.")
        return

    print("Connected successfully!")

    try:
        # Fetch the values (with parallel processing for better performance)
        print("Updating all components...")
        if not await solarfocus.update(parallel=True, optimized=True):
            print("Updating solarfocus failed.")
            return
        
        # Print the values
        await print_system_info(solarfocus)
        
    finally:
        # Always disconnect
        await solarfocus.disconnect()


async def example_context_manager():
    """Example using async context manager (recommended approach)"""
    # Using async context manager - automatically handles connection/disconnection
    async with AsyncSolarfocusAPI(
        ip="10.10.10.237",  # adapt IP-Address
        system=Systems.VAMPAIR,
        api_version=ApiVersions.V_25_030,
        auto_reconnect=True,
        connection_timeout=10.0
    ) as solarfocus:
        print("Connected using context manager!")
        
        # Fetch the values
        if await solarfocus.update(parallel=True, optimized=True):
            await print_system_info(solarfocus)
        else:
            print("Update failed!")


async def print_system_info(solarfocus: AsyncSolarfocusAPI):
    """Print system information"""
    # Print the values
    print(solarfocus)
    print(solarfocus.heating_circuits[0])
    print(solarfocus.boilers[0])
    print(solarfocus.buffers[0])

    # System-specific components
    if solarfocus.system in [Systems.THERMINATOR, Systems.ECOTOP]:
        print(solarfocus.biomassboiler)
    
    if solarfocus.system is Systems.VAMPAIR:
        print(solarfocus.heatpump)

    print(solarfocus.photovoltaic)

    if solarfocus.fresh_water_modules:
        print(solarfocus.fresh_water_modules[0])

    print(solarfocus.solar[0])

    if solarfocus.differential_modules:
        print(solarfocus.differential_modules[0])

    if solarfocus.circulations:
        print(solarfocus.circulations[0])

    # Demonstrate partial updates (more efficient for specific components)
    print("\n" + "="*50)
    print("PARTIAL UPDATE EXAMPLE")
    print("="*50)
    print("Updating only heating circuits and buffers...")
    success = await solarfocus.update_partial(
        ["heating_circuits", "buffers"], 
        parallel=True, 
        optimized=True
    )
    print(f"Partial update successful: {success}")

    # Show connection health
    health = solarfocus.get_connection_health()
    print(f"\nConnection Health: {health}")

    # Show component health
    print(f"System Health: {'Healthy' if solarfocus.is_healthy() else 'Issues detected'}")
    if not solarfocus.is_healthy():
        print(f"Failed components: {solarfocus.get_failed_components()}")

    # Demonstrate async setting operations
    print("\n" + "="*50)
    print("ASYNC SETTINGS EXAMPLE")
    print("="*50)
    
    # Example: Set heating circuit mode (if applicable)
    # Note: This would write to the actual system, so commented out for safety
    # from pysolarfocus import HeatingCircuitMode
    # success = await solarfocus.set_heating_circuit_mode(0, HeatingCircuitMode.ALWAYS_ON)
    # print(f"Set heating circuit mode: {success}")


def run_async_example():
    """Entry point for running the async example"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExample interrupted by user")
    except Exception as e:
        print(f"Error running async example: {e}")


if __name__ == "__main__":
    run_async_example()
