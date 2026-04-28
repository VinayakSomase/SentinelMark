import cv2
import numpy as np
import uuid
import os
import json
import shutil

# Convert trap ID to binary (32 bits)

def id_to_binary(trap_id):
    numeric = abs(hash(trap_id)) % (2**32)
    return format(numeric, '032b')

# Embed binary into frame (LSB)

def embed_id(frame, binary_id):
    h, w, _ = frame.shape
    idx = 0

    for i in range(h):
        for j in range(w):
            if idx < len(binary_id):
                frame[i, j][0] = (frame[i, j][0] & 254) | int(binary_id[idx])
                idx += 1
            else:
                return frame
    return frame


# Main Honeypot Generator

def generate_honeypot_variants(input_video_path, output_folder):

   
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder, exist_ok=True)

    
    if not os.path.exists(input_video_path):
        print("❌ Input video not found")
        return

    variants = []

    modifications = [
        {"name": "hue_shift",   "desc": "Hue shift +10"},
        {"name": "brightness",  "desc": "Brightness +15"},
        {"name": "crop",        "desc": "Crop 3% edges"},
    ]

    for mod in modifications:
        trap_id = "TRAP-" + str(uuid.uuid4())[:6].upper()
        binary_id = id_to_binary(trap_id)

        cap = cv2.VideoCapture(input_video_path)

        if not cap.isOpened():
            print("❌ Error opening input video")
            return

        
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or fps is None:
            fps = 30

        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        
        if w == 0 or h == 0:
            print("❌ Invalid video dimensions")
            return

        output_path = f"{output_folder}/{trap_id}_{mod['name']}.avi"

        #  Windows compatible codec
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

        if not out.isOpened():
            print("❌ VideoWriter failed to open")
            return

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame is None:
                continue

            #  VISUAL MODIFICATIONS 
            if mod["name"] == "hue_shift":
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.int32)
                hsv[:, :, 0] = (hsv[:, :, 0] + 10) % 180
                frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

            elif mod["name"] == "brightness":
                frame = np.clip(frame.astype(np.int32) + 15, 0, 255).astype(np.uint8)

            elif mod["name"] == "crop":
                pad_h = int(h * 0.03)
                pad_w = int(w * 0.03)
                cropped = frame[pad_h:h-pad_h, pad_w:w-pad_w]
                frame = cv2.resize(cropped, (w, h))

            # INVISIBLE WATERMARK 
            frame = embed_id(frame, binary_id)

            # VISIBLE MICRO TEXT 
            cv2.putText(frame, trap_id, (10, h - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                        (0, 0, 0), 1, cv2.LINE_AA)

            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()

        variants.append({
            "trap_id": trap_id,
            "modification": mod["desc"],
            "file": output_path,
            "frames": frame_count,
            "status": "active"
        })

        print(f"✅ Created trap: {trap_id} ({mod['desc']})")

    
    metadata_path = os.path.join(output_folder, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(variants, f, indent=4)

    print(f"\n📁 Metadata saved: {metadata_path}")

    return variants



if __name__ == "__main__":
    variants = generate_honeypot_variants("test.avi", "honeypots")

    print("\n🎯 Generated Honeypot Variants:")
    for v in variants:
        print(f"{v['trap_id']} → {v['modification']}")