import asyncio
import json
import logging
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaPlayer, MediaRelay
import socketio

class WebRTCHandler:
    """Handles real-time communication for live agent features"""
    
    def __init__(self):
        self.pcs = set()
        self.sio = socketio.AsyncServer(cors_allowed_origins='*')
        self.setup_handlers()
        print("✅ WebRTC Handler Ready for Live Interaction")
    
    def setup_handlers(self):
        @self.sio.event
        async def connect(sid, environ):
            print(f"🔌 Client connected: {sid}")
        
        @self.sio.event
        async def disconnect(sid):
            print(f"🔌 Client disconnected: {sid}")
        
        @self.sio.event
        async def offer(sid, data):
            print(f"📞 Received offer from {sid}")
            # Handle WebRTC offer
            await self.handle_offer(sid, data)
        
        @self.sio.event
        async def voice_command(sid, data):
            print(f"🎤 Voice command: {data.get('command')}")
            # Process voice commands in real-time
            await self.process_voice_command(sid, data)
    
    async def handle_offer(self, sid, data):
        """Handle WebRTC offer for real-time media"""
        offer = RTCSessionDescription(sdp=data['sdp'], type=data['type'])
        
        # Create peer connection
        config = RTCConfiguration([
            RTCIceServer(urls=['stun:stun.l.google.com:19302'])
        ])
        pc = RTCPeerConnection(configuration=config)
        self.pcs.add(pc)
        
        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print(f"ICE connection state: {pc.iceConnectionState}")
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.pcs.discard(pc)
        
        await pc.setRemoteDescription(offer)
        
        # Create answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        
        # Send answer back
        await self.sio.emit('answer', {
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type
        }, room=sid)
    
    async def process_voice_command(self, sid, data):
        """Process voice commands in real-time"""
        command = data.get('command', '').lower()
        
        if 'stop' in command or 'cancel' in command:
            await self.sio.emit('command_response', {
                'action': 'stop',
                'message': 'Stopping generation...'
            }, room=sid)
        
        elif 'new story' in command:
            await self.sio.emit('command_response', {
                'action': 'new_story',
                'message': 'Creating new story...'
            }, room=sid)
        
        elif 'generate' in command:
            await self.sio.emit('command_response', {
                'action': 'generate',
                'message': 'Generating comic...'
            }, room=sid)
        
        elif 'read' in command or 'narrate' in command:
            await self.sio.emit('command_response', {
                'action': 'narrate',
                'message': 'Starting narration...'
            }, room=sid)
    
    async def broadcast_progress(self, progress, message):
        """Broadcast generation progress to all connected clients"""
        await self.sio.emit('progress', {
            'progress': progress,
            'message': message
        })
    
    async def close(self):
        """Close all peer connections"""
        for pc in self.pcs:
            await pc.close()
        self.pcs.clear()

# Create singleton instance
webrtc_handler = WebRTCHandler()
