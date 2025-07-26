import wave
import math
import struct

def generate_shoot_sound():
    # Parameters for gun shot sound
    duration = 0.2  # seconds
    sample_rate = 44100  # samples per second
    amplitude = 32000  # volume
    
    # Generate gun shot sound (sharp attack, noise, quick decay)
    with wave.open('shoot.wav', 'w') as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        for i in range(int(duration * sample_rate)):
            time_factor = i / (duration * sample_rate)
            
            # Very sharp attack, quick decay
            if time_factor < 0.02:  # First 2% - sharp attack
                envelope = time_factor * 50  # Sharp rise
            else:
                envelope = math.exp(-10 * time_factor)  # Exponential decay
            
            # Mix of noise and low frequency components
            noise = random.uniform(-1, 1)
            bass = math.sin(2.0 * math.pi * 120 * i / sample_rate)  # Low frequency boom
            mid = math.sin(2.0 * math.pi * 400 * i / sample_rate)   # Mid frequency
            
            # Combine components with different weights
            value = (0.7 * noise + 0.2 * bass + 0.1 * mid) * envelope * amplitude
            
            # Clip the value to prevent distortion
            value = max(min(int(value), 32767), -32767)
            data = struct.pack('<h', value)
            wav_file.writeframes(data)

def generate_explosion_sound():
    # Parameters for explosion sound
    duration = 0.3  # seconds
    sample_rate = 44100  # samples per second
    amplitude = 32000  # volume

    # Generate explosion sound (white noise with decay)
    with wave.open('explosion.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(int(duration * sample_rate)):
            decay = 1.0 - (i / (duration * sample_rate))
            value = int(amplitude * decay * (2 * random.random() - 1))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)

def generate_refuel_sound():
    # Parameters for refuel sound
    duration = 0.2  # seconds
    frequency = 440.0  # Hz (A4 note)
    sample_rate = 44100
    amplitude = 32000

    # Generate refuel sound (rising pitch)
    with wave.open('refuel.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(int(duration * sample_rate)):
            # Increase frequency over time
            current_frequency = frequency * (1 + i / (duration * sample_rate))
            value = int(amplitude * math.sin(2.0 * math.pi * current_frequency * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)

if __name__ == '__main__':
    import random
    print("Generating sound effects...")
    generate_shoot_sound()
    generate_explosion_sound()
    generate_refuel_sound()
    print("Sound effects generated successfully!") 