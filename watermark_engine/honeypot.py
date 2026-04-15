# import cv2
# import numpy as np
# import uuid
# import os

# def generate_honeypot_variants(input_video_path, output_folder):
#     """
#     Creates 3 slightly modified versions of a video.
#     Each version looks identical to humans but has a unique trap ID.
#     """
#     os.makedirs(output_folder, exist_ok=True)
#     variants = []

#     modifications = [
#         {"name": "hue_shift",   "desc": "Hue shift +10"},
#         {"name": "brightness",  "desc": "Brightness +15"},
#         {"name": "crop",        "desc": "Crop 3% edges"},
#     ]

#     for mod in modifications:
#         trap_id = "TRAP-" + str(uuid.uuid4())[:6].upper()
#         output_path = f"{output_folder}/{trap_id}_{mod['name']}.avi"

#         cap = cv2.VideoCapture(input_video_path)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#         fourcc = cv2.VideoWriter_fourcc(*'XVID')
#         out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             if mod["name"] == "hue_shift":
#                 hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.int32)
#                 hsv[:,:,0] = (hsv[:,:,0] + 10) % 180
#                 frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

#             elif mod["name"] == "brightness":
#                 frame = np.clip(frame.astype(np.int32) + 15, 0, 255).astype(np.uint8)

#             elif mod["name"] == "crop":
#                 pad_h = int(h * 0.03)
#                 pad_w = int(w * 0.03)
#                 cropped = frame[pad_h:h-pad_h, pad_w:w-pad_w]
#                 frame = cv2.resize(cropped, (w, h))

#             out.write(frame)

#         cap.release()
#         out.release()
#         variants.append({
#             "trap_id": trap_id,
#             "modification": mod["desc"],
#             "file": output_path,
#             "status": "active"
#         })
#         print(f"Created trap: {trap_id} ({mod['desc']})")

#     return variants

# if __name__ == "__main__":
#     # Test using our existing test video
#     variants = generate_honeypot_variants("test.avi", "honeypots")
#     print("\nGenerated honeypot variants:")
#     for v in variants:
#         print(f"  {v['trap_id']} - {v['modification']}")


# import cv2
# import numpy as np
# import uuid
# import os
# import json

# # ===============================
# # Convert trap ID to binary (32 bits)
# # ===============================
# def id_to_binary(trap_id):
#     numeric = abs(hash(trap_id)) % (2**32)
#     return format(numeric, '032b')

# # ===============================
# # Embed binary into frame (LSB)
# # ===============================
# def embed_id(frame, binary_id):
#     h, w, _ = frame.shape
#     idx = 0

#     for i in range(h):
#         for j in range(w):
#             if idx < len(binary_id):
#                 frame[i, j][0] = (frame[i, j][0] & 254) | int(binary_id[idx])
#                 idx += 1
#             else:
#                 return frame
#     return frame

# # ===============================
# # Main Honeypot Generator
# # ===============================
# def generate_honeypot_variants(input_video_path, output_folder):

#     os.makedirs(output_folder, exist_ok=True)
#     variants = []

#     modifications = [
#         {"name": "hue_shift",   "desc": "Hue shift +10"},
#         {"name": "brightness",  "desc": "Brightness +15"},
#         {"name": "crop",        "desc": "Crop 3% edges"},
#     ]

#     for mod in modifications:
#         trap_id = "TRAP-" + str(uuid.uuid4())[:6].upper()
#         binary_id = id_to_binary(trap_id)

#         output_path = f"{output_folder}/{trap_id}_{mod['name']}.mp4"

#         cap = cv2.VideoCapture(input_video_path)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

#         frame_count = 0

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # ===== VISUAL MODIFICATIONS =====
#             if mod["name"] == "hue_shift":
#                 hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.int32)
#                 hsv[:,:,0] = (hsv[:,:,0] + 10) % 180
#                 frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

#             elif mod["name"] == "brightness":
#                 frame = np.clip(frame.astype(np.int32) + 15, 0, 255).astype(np.uint8)

#             elif mod["name"] == "crop":
#                 pad_h = int(h * 0.03)
#                 pad_w = int(w * 0.03)
#                 cropped = frame[pad_h:h-pad_h, pad_w:w-pad_w]
#                 frame = cv2.resize(cropped, (w, h))

#             # ===== INVISIBLE WATERMARK =====
#             frame = embed_id(frame, binary_id)

#             # ===== VISIBLE MICRO OVERLAY (very subtle) =====
#             cv2.putText(frame, trap_id, (10, h - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.4,
#                         (0, 0, 0), 1, cv2.LINE_AA)

#             out.write(frame)
#             frame_count += 1

#         cap.release()
#         out.release()

#         variants.append({
#             "trap_id": trap_id,
#             "modification": mod["desc"],
#             "file": output_path,
#             "frames": frame_count,
#             "status": "active"
#         })

#         print(f"✅ Created trap: {trap_id} ({mod['desc']})")

#     # ===== SAVE METADATA =====
#     metadata_path = os.path.join(output_folder, "metadata.json")
#     with open(metadata_path, "w") as f:
#         json.dump(variants, f, indent=4)

#     print(f"\n📁 Metadata saved: {metadata_path}")

#     return variants


# # ===============================
# # TEST RUN
# # ===============================
# if __name__ == "__main__":
#     variants = generate_honeypot_variants("test.mp4", "honeypots")

#     print("\n🎯 Generated Honeypot Variants:")
#     for v in variants:
#         print(f"{v['trap_id']} → {v['modification']}")



import cv2
import numpy as np
import uuid
import os
import json
import shutil

# ===============================
# Convert trap ID to binary (32 bits)
# ===============================
def id_to_binary(trap_id):
    numeric = abs(hash(trap_id)) % (2**32)
    return format(numeric, '032b')

# ===============================
# Embed binary into frame (LSB)
# ===============================
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

# ===============================
# Main Honeypot Generator
# ===============================
def generate_honeypot_variants(input_video_path, output_folder):

    # 🔥 Clean old folder
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder, exist_ok=True)

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

        # ✅ FPS FIX
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or fps is None:
            fps = 30

        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_path = f"{output_folder}/{trap_id}_{mod['name']}.avi"

        # ✅ Stable codec
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

        # ✅ Check writer
        if not out.isOpened():
            print("❌ VideoWriter failed")
            return

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame is None:
                continue

            # ===== VISUAL MODIFICATIONS =====
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

            # ===== INVISIBLE WATERMARK =====
            frame = embed_id(frame, binary_id)

            # ===== VISIBLE MICRO TEXT =====
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

    # ===== SAVE METADATA =====
    metadata_path = os.path.join(output_folder, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(variants, f, indent=4)

    print(f"\n📁 Metadata saved: {metadata_path}")

    return variants


# ===============================
# TEST RUN
# ===============================
if __name__ == "__main__":
    variants = generate_honeypot_variants("test.avi", "honeypots")

    print("\n🎯 Generated Honeypot Variants:")
    for v in variants:
        print(f"{v['trap_id']} → {v['modification']}")