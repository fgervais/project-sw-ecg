import asyncio
import numpy as np
import struct

from threading import Thread
from aiocoap import resource, Message, Context, Code

from interface import Dashboard


class DeviceLogic:
    def __init__(self):
        self.ecg_data = None
        self.battery_level = 100

    def process_ecg(self, payload: bytes):
        self.ecg_data = payload.decode()
        print(f"[DeviceLogic] ECG data updated: {self.ecg_data}")
        return f"ECG data received: {self.ecg_data}"

    def update_battery(self, payload: bytes):
        try:
            new_level = int(payload.decode())
            self.battery_level = max(0, min(new_level, 100))
            print(f"[DeviceLogic] Battery level updated: {self.battery_level}%")
            return f"Battery updated: {self.battery_level}%"
        except ValueError:
            return "Invalid battery value"


class ECGResource(resource.Resource):
    def __init__(self, dashboard: Dashboard):
        super().__init__()
        self.dashboard = dashboard

    async def render_post(self, request: Message):
        count = len(request.payload) // 4
        values = struct.unpack(f"!{count}i", request.payload)
        arr = np.array(values, dtype=np.int32)
        scaled = arr / (2**31)
        print(f"scaled = {scaled}")

        for val in scaled:
            self.dashboard.update_ecg_view(val)

        # response_text = self.device_logic.process_ecg(request.payload)
        return Message(code=Code.CHANGED)


class BatteryResource(resource.Resource):
    def __init__(self, device_logic: DeviceLogic):
        super().__init__()
        self.device_logic = device_logic

    async def render_post(self, request: Message):
        response_text = self.device_logic.update_battery(request.payload)
        return Message(code=Code.CONTENT, payload=response_text.encode())


class CoAPServer(Thread):
    def __init__(self, dashboard: Dashboard):
        super().__init__()
        self.loop = None
        self.context = None
        self.forever_future = None
        self.dashboard = dashboard

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._async_run())

    async def _async_run(self):
        # Build site with resources
        root = resource.Site()
        root.add_resource(['ecg'], ECGResource(self.dashboard))
        root.add_resource(['battery'], BatteryResource(self.dashboard))

        # Start CoAP context
        self.context = await Context.create_server_context(root, bind=("::", 5683))

        print("[CoAPServer] Server started on coap://localhost:5683")

        # Keep running until stopped
        self.forever_future = self.loop.create_future()
        try:
            await self.forever_future
        except asyncio.CancelledError:
            pass
        finally:
            await self.context.shutdown()
            print("[CoAPServer] Server stopped.")

    def stop(self):
        if self.loop and self.forever_future:
            def _stop():
                if not self.forever_future.done():
                    self.forever_future.cancel()
            self.loop.call_soon_threadsafe(_stop)
